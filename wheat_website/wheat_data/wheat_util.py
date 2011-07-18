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
		self._varieties = {}
		self._names = []
		self._locations = []
		self._years = []
		self._include_fields = []
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
		
		rank_list = []
		rank_dict = {}
		
		for name in data.keys():
			try:
				rank_dict[data[name]['count']].update({name: data[name]})
			except KeyError:
				rank_dict[data[name]['count']] = {name: data[name]}
		
		maxrank = max(rank_dict.keys())
		rank_list = range(maxrank)
		
		for i in rank_list:
			rank_list[i] = {} # ensure empty dictionaries 
		
		for i in rank_dict.keys():
			#rank_list[i-1] = rank_dict[i] # smallest rank first
			rank_list[maxrank - i] = rank_dict[i] # largest rank first
		"""
		first_dict = {}
		rank_dict = {}
		last_dict = {}
		
		# rank 0, each name with their locations
		for name in data.keys():
			print("%s: %d" % (name, data[name]['count']))
			if name != 'count':
				first_dict[name] = set()
				for location in data[name].keys():
					if location != 'count':
						for year in data[name][location].keys():
							if year != 'count':
								first_dict[name].add((location,year))
		rank_dict = first_dict
		rank_list.append(rank_dict)

		# rank 1, pairs of names with their common locations
		last_dict = first_dict
		rank_dict = {}
		for name in last_dict.keys():
			for oname in first_dict.keys():
				if oname != name:
					locations = last_dict[name].union(first_dict[oname])
					if len(list(locations)) > 0:
						nlist = [name,oname]
						nlist.sort()
						rank_dict[tuple(nlist)] = locations
		rank_list.append(rank_dict)
		
		# rank 2
		last_dict = rank_dict
		rank_dict = {}
		for nametuple in last_dict.keys():
			for oname in first_dict.keys():
				if oname not in nametuple:
					locations = last_dict[nametuple].union(first_dict[oname])
					if len(list(locations)) > 0:
						nlist = list(nametuple)
						nlist.append(oname)
						nlist.sort()
						rank_dict[tuple(nlist)] = locations
		rank_list.append(rank_dict)
		
		# rank 3
		last_dict = rank_dict
		rank_dict = {}
		for nametuple in last_dict.keys():
			for oname in first_dict.keys():
				if oname not in nametuple:
					locations = last_dict[nametuple].union(first_dict[oname])
					if len(list(locations)) > 0:
						nlist = list(nametuple)
						nlist.append(oname)
						nlist.sort()
						rank_dict[tuple(nlist)] = locations
		rank_list.append(rank_dict)
		
		# rank 4
		last_dict = rank_dict
		rank_dict = {}
		for nametuple in last_dict.keys():
			for oname in first_dict.keys():
				if oname not in nametuple:
					locations = last_dict[nametuple].union(first_dict[oname])
					if len(list(locations)) > 0:
						nlist = list(nametuple)
						nlist.append(oname)
						nlist.sort()
						rank_dict[tuple(nlist)] = locations
		rank_list.append(rank_dict)
		"""

		return rank_list
	
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

		data_list = self._get_recent_ranked(n_list)
		averaged = range(len(data_list))
		
		j = 0
		for rank_dict in data_list:
			avg_dict = {}
			for name in rank_dict.keys():
				avg_dict[name] = {}
				all_years = set()
				all_locations = []
				for location in rank_dict[name].keys():
					if location != 'count':
						all_locations.append(location) # TODO: this is a candidate to be stored on populate()
						for year in rank_dict[name][location].keys():
							if year != 'count':
								all_years.add(year) # TODO: this is a candidate to be stored on populate()
				all_years = sorted(list(all_years))
				
				# populate years, a dictionary of {'prefix': [2000, 1999, ...], ...}
				years = {}
				i = 0
				for year in all_years: # *must* be done on a per variety basis
					prefix = "%d_yr_avg_" % (len(all_years) - i)
					for prev_prefixes in years.keys():
						years[prev_prefixes].append(year) # append this year to each existing element
					years[prefix] = [year] # make a list containing only this year
					i += 1

				# populate avg_dict, a dictionary {'name': {'prefix'+'field': float, ...}, ...}
				for location in all_locations:
					for year in all_years:
						for prefix in years.keys():
							if year in years[prefix]:
								try:
									entries = rank_dict[name][location][year]['entries']
								except KeyError:
									continue # skip to next iteration of `for prefix in years.keys()'
								for entry in entries:
									try:
										if entry not in avg_dict[name]['entries']:
											avg_dict[name]['entries'].append(entry)
									except KeyError:
										avg_dict[name]['entries'] = [entry]
									for field in field_list:
										fieldname = field.name
										key = "%s%s" % (prefix, fieldname)
										value = getattr(entry, fieldname)
										if value != None:
											try:
												avg_dict[name][key][0] += 1 # count
												avg_dict[name][key][1] += float(value) # running total
												#avg_dict[name][key][2] = (avg_dict[name][key][2] + avg_dict[name][key][1]) / avg_dict[name][key][0] # running average
											except KeyError:
												avg_dict[name][key] = [1,float(value)]
												#avg_dict[name][key] = [1,float(value),0.0]
										
				#Either we update the average each insertion, or we iterate over the dict again and calculate the averages...
				for key in avg_dict[name].keys():
					if key != 'entries':
						avg_dict[name][key] = round(avg_dict[name][key][1] / avg_dict[name][key][0], 2)
				
				avg_dict['count'] = rank_dict[name]['count']
			
			averaged[j] = avg_dict
			j += 1
		
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
		b = self._get_averages(n_list, field_list)
		
		for i in range(len(a)):
			for key in a[i].keys():
				try:
					access = b[i]
				except IndexError:
					continue
				try:
					a[i][key].update(b[i][key])
				except KeyError:
					pass
				except AttributeError: # raised when trying to access prefix_count
					pass
					
		return a
