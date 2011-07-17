from wheat_data.models import Trial_Entry #, Date

class Trial_x_Location_x_Year:
	""" 
	Organizational class for our Trial_Entry x Location x Year data.
	Pass in a django queryset and the fields you want to consider for
	averaging.
	"""
	# A dictionary of variety_name to a year dictionary with Trial_Entry 
	# objects and their count.
	# {(name, location): {'year': [count, [trial_entry_objects]]}}
	_varieties = {}
	
	# private iterators
	_names = []
	_locations = []
	_years = []
	_include_fields = []
	
	def __init__(self):
		pass
				
	def __init__(self, trial_set, location_set = None, year_list = None, field_list = None):
		""" 
		Initializes with all elements matching field_list in query_set, or
		all elements if field_list is None. Optional parameters of locations
		and years may be included if known a priori.
		"""
		return self.populate(trial_set, location_set, year_list, field_list)
		
	def populate(self, trial_set, location_set = None, year_list = None, field_list = None):
		""" 
		Adds all elements matching field_list in query_set, or all elements 
		if field_list is None. Optional parameters of locations and years 
		may be included if known a priori.
		
		Calling populate() multiple times is supported, but untested. Your
		mileage may vary.
		"""
		# Bring location_set to a consistent state
		if location_set is None:
			for entry in query_set:
				location = str(entry.location.name)
				if location not in self._locations:
					self._locations.append(location)
		else:
			for entry in location_set:
				location = str(entry.name)
				if location not in self._locations:
					self._locations.append(location)
					
		# Bring year_list to a consistent state
		if year_list is None:
			for entry in query_set:
				year = str(entry.harvest_date.date.year)
				if year not in self._years:
					self._years.append(year)
		else:
			for year in year_list:
				if year not in self._years:
					self._years.append(year)
					
		# Bring field_list to a consistent state
		if field_list is None:
			for field in Trial_Entry._meta.fields:
				if (field.get_internal_type() == 'DecimalField' 
						or field.get_internal_type() == 'PositiveIntegerField' 
						or field.get_internal_type() == 'SmallIntegerField'
						or field.get_internal_type() == 'IntegerField'):
					self._include_fields.append(field) # only consider averageable data
		else:
			for field in field_list:
				if (field.get_internal_type() == 'DecimalField' 
						or field.get_internal_type() == 'PositiveIntegerField' 
						or field.get_internal_type() == 'SmallIntegerField'
						or field.get_internal_type() == 'IntegerField'):
					if field in models.Trial_Entry._meta.fields:
						self._include_fields.append(field) # ensure the user passed in good data
		
		# Initialize our inner data structures
		for entry in trial_set:
			name = str(entry.variety.name) # force evaluation
			location = str(entry.location.name) 
			year = str(entry.harvest_date.date.year)
			
			self._names.append(name)
			
			try:
				self._varieties[name]['count'] += 1
			except KeyError: # initialize and add the first value
				self._varieties[name] = {'count': 1}

			try:
				self._varieties[name][location]['count'] += 1
			except KeyError:
				self._varieties[name][location] = {'count': 1}

			try:
				self._varieties[name][location][year]['count'] += 1
				self._varieties[name][location][year]['entries'].append(entry)
			except KeyError: 
				self._varieties[name][location][year] = {'count': 1, 'entries': [entry]}
		
	def _most_recent_years_with_sufficient_data(self, var_key, loc_key, n_list = None):
		""" 
		Query for the most recent year that has sufficient data to post a 
		result using the variety_name. 
		
		This currently just returns the most recent year in the set, but in 
		the future it may be wise to check if the most recent year adversely
		affects a variety's ranking merely because only one trial result has
		been input insofar.
		
		Raises: KeyError
		"""
		if n_list is None:
			n_list = [1]
		
		return_list = []
		
		for element in self._varieties[var_key][loc_key].keys():
			if (element != 'count') and (element != 'entries'):
				return_list.append(element)

		#TODO: n_list isn't being treated properly, consider n_list=[1,3,4]

		# Returns a list with the first element(s) of a sort-descending list			
		# Remember to `try/except KeyError' when calling this function.
		return sorted(return_list, reverse=True)[:max(n_list):]
	
	def _get(self):
		""" 
		Return all data held in this object.
		"""
		return self._varieties
	
	def _get_recent(self, n_list = None):
		"""
		Return the data matching a list of variety_names in this object that
		is most recent in year, and has sufficient data in that year. If
		n_list is none, the most recent year is returned. If variety_x_location_list is
		None, all recent data are returned. An optional list of field names
		filters by those field names.
		"""
		data = self._get()
		
		recent_dict = {}
		for name in data.keys():
			recent_dict[name] = data[name]
			for location in data[name].keys():
				if location != 'count':
					years = self._most_recent_years_with_sufficient_data(name, location, n_list)
					years.append('count') # don't want to delete the accounting field
					for year in recent_dict[name][location].keys():
						if year not in years:
							del recent_dict[name][location][year]
							recent_dict[name][location]['count'] -= 1
		
		return recent_dict
	
	def _get_recent_ranked(self, n_list = None):
		"""
		Returns a list of dictionaries ranked by number of locations x years
		per variety, filtered first by date such that the n_list most recent
		years are considered.
		"""
		
		data = self._get_recent(n_list)
		#names = self._names
		#locations = self._locations
		#years = self._years
		ranked_list = []
		prev_rank = []
		cur_rank = []
		
		def satisfies_all_locations(name_list, name_to_check):
			# given all names in name_list already have a location in common
			locations = []
			for name in name_list:
				#print(data[name].keys())
				locations.extend(data[name].keys())
			locations = list(set(locations))
			locations.extend(data[name_to_check].keys())
			
			# the key 'count' will be in all, so check for size > 1
			return len(list(set(locations))) > len(name_list)+1
		
		# rank 0, all names share locations with themselves
		for name in data.keys():
			if name != 'count':
				cur_rank.append([name])
		ranked_list.append(cur_rank)
		#print(cur_rank)
		#print(" ")
		# rank 1, which names form a set with another name?
		prev_rank = cur_rank
		cur_rank = []
		for name in data.keys():
			if name != 'count':
				for plist in prev_rank:
					if satisfies_all_locations(plist, name):
						plist.append(name)
						cur_rank.append(plist)
		ranked_list.append(cur_rank)
		#print(cur_rank)
		"""
		# rank 2, which names form a set with two others?		
		prev_rank = cur_rank
		cur_rank = []
		for name in data.keys():
			if name != 'count':
				for plist in prev_rank:
					if satisfies_all_locations(plist, name):
						plist.append(name)
						cur_rank.append(plist)
		ranked_list.append(cur_rank)
		"""
		
		for plist in cur_rank:
			print(len(plist))
		
		
		return ranked_list
	
	def _get_averages(self, n_list = None, field_list = None):
		"""
		Given a list of the number of dates to go back (e.g. [1,2,3] for the
		1-yr, 2-yr, and 3-yr averages), return those averaged data. An 
		optional list of varieties filers by those varieties, and an 
		optional list of fieldnames filters by those fieldnames.

		The returned dictionary tags the keys of the averaged items, 
		prepending `1-yr-avg-' `2-year-avg-' etc. based on the values in 
		n_list.
		"""
		if field_list is None: # paranoia
			field_list = self._include_fields

		averaged = {}
		years = {}
		data = self._get_recent_ranked(n_list)
		
		"""
		for var_loc in data.keys():
			i = 1
			averaged[var_loc] = {}
			all_years = sorted(data[var_loc].keys(), reverse=True)
			# populate years, a dictionary of {'prefix': [2000, 1999, ...], ...}
			for year in all_years: # *must* be done on a per variety basis
				prefix = "%d_yr_avg_" % i
				for prev_data in years.keys():
					years[prev_data].append(year) # append this year to each existing element
				years[prefix] = [year] # make a list containing only this year
				i += 1
			# populate averaged, a dictionary {'name': {'prefix'+'field': float, ...}, ...}
			for year in all_years:
				for prefix in years.keys():
					if year in years[prefix]:
						for entry in data[var_loc][year][1]:
							try:
								if entry not in averaged[var_loc]['entries']:
									averaged[var_loc]['entries'].append(entry)
							except KeyError:
								averaged[var_loc]['entries'] = [entry]
							for field in field_list:
								fieldname = field.name
								key = "%s%s" % (prefix, fieldname)
								value = getattr(entry, fieldname)
								if value != None:
									try:
										averaged[var_loc][key][0] += 1 # count
										averaged[var_loc][key][1] += float(value) # running total
										#averaged[var_loc][key][2] = (averaged[var_loc][key][2] + averaged[var_loc][key][1]) / averaged[var_loc][key][0] # running average
									except KeyError:
										averaged[var_loc][key] = [1,float(value)]
										#averaged[var_loc][key] = [1,float(value),0.0]
			
			#Either we update the average each insertion, or we iterate over the dict again and calculate the averages...
			ranks = []
			for key in averaged[var_loc].keys():
				if key != 'entries':
					averaged[var_loc][key] = round(averaged[var_loc][key][1] / averaged[var_loc][key][0], 2)
		"""
		return averaged

	def fetch(self, n_list = None, field_list = None):
		"""
		Main accessor method for this class. The optional parameters n_list 
		and field_list are used to return multi-year averaged fields, while 
		fields not in field_list are returned as 1 (last) year averages. 
		When n_list is not supplied, a 1 year average is assumed. If no 
		field_list is supplied, results are calculated over all fields.
		
		Returns a ranked list of dictionaries [ {variety_name: { entries: [objects], 1-yr-avg-fieldname: value, ... } }, ... ]
		where the ranking is determined by number of locations for that variety.
		"""
		if field_list is None:
			field_list = []
			exclusion_fields = self._include_fields
		else:
			exclusion_fields = list(set(self._include_fields).difference(set(field_list)))
		
		
		a = self._get_averages([1], exclusion_fields)
		"""
		b = self._get_averages(n_list, variety_x_location_list, field_list)
		
		
		return_list = []
		# TODO: verify robustness of the following: (does all of b get into a? b.keys()?)
		count = {}
		ranks = {}
		names = {}
		locations = {}
		for var_loc in a.keys(): 
			a[var_loc].update(b[var_loc])
			count[var_loc] = len(a[var_loc]['entries'])
			names.append(var_loc[0])
			locations.append(var_loc[1])
		"""
		return [a]
