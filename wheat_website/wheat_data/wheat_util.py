from wheat_data.models import Trial_Entry #, Date

class Trial_x_Variety_x_Year:
  """ 
  Organizational class for our Trial_Entry x Variety x Year data.
  Pass in a django queryset and the fields you want to consider for
  averaging.
  """
  # A dictionary of variety_name to a year dictionary with Trial_Entry 
  # objects and their count.
  # {(name, location): {'year': [count, [trial_entry_objects]]}}
  _variety_x_location = {}
  _include_fields = []
  
  def __init__(self):
    pass
        
  def __init__(self, query_set, field_list = None):
    """ 
    Initializes with all elements matching field_list in query_set, or
    all elements if field_list is None.
    """
    return self.populate(query_set, field_list)
    
  def populate(self, query_set, field_list = None):
		""" 
		Adds all elements matching field_list in query_set, or all elements 
		if field_list is None.

		TODO: Verify the fields that are passed in are actual fields
		"""
    # Bring field_list to a consistent state
		if field_list is None:
			field_list = []
			for field in Trial_Entry._meta.fields:
				if (field.get_internal_type() == 'DecimalField' 
						or field.get_internal_type() == 'PositiveIntegerField' 
						or field.get_internal_type() == 'SmallIntegerField'
						or field.get_internal_type() == 'IntegerField'):
					field_list.append(field) # only consider averageable data
			self._include_fields = field_list
		else:
			for field in field_list:
				if (field.get_internal_type() == 'DecimalField' 
						or field.get_internal_type() == 'PositiveIntegerField' 
						or field.get_internal_type() == 'SmallIntegerField'
						or field.get_internal_type() == 'IntegerField'):
					if field in models.Trial_Entry._meta.fields:
						self._include_fields.append(field) # ensure the user passed in good data
    
    # Initialize our inner data structures
		for entry in query_set:
			name = str(entry.variety.name) # force evaluation
			location = str(entry.location.name) 
			year = str(entry.harvest_date.date.year)
			try:
				self._variety_x_location[(name, location)][year][0] += 1
				self._variety_x_location[(name, location)][year][1].append(entry)
			except KeyError:  # initialize and add the first value
				try:
					self._variety_x_location[(name, location)][year] = [1, [entry]]
				except KeyError:
					self._variety_x_location[(name, location)] = {}
					self._variety_x_location[(name, location)][year] = [1, [entry]]

    
  def _most_recent_years_with_sufficient_data(self, var_loc_key, n_list = None):
    """ 
    Query for the most recent year that has sufficient data to post a 
    result using the variety_name. 
    
    This currently just returns the most recent year in the set, but in 
    the future it may be wise to check if the most recent year adversely
    affects a variety's ranking merely because only one trial result has
    been input insofar.
    """
    if n_list is None:
      n_list = [1]
      
    # Returns a list with the first element(s) of a sort-descending list      
    # Remember to `try/except KeyError' when calling this function.
    return sorted(self._variety_x_location[var_loc_key].keys(), reverse=True)[:max(n_list):]
  
  def _get(self, variety_x_location_list = None):
    """ 
    Return all data held in this object matching variety_x_location_list. If
    variety_x_location_list is None all data is returned. If a name appears
    in variety_x_location_list that isn't in our data, that fetch for non-existent
    data silently fails and we continue on. An optional list of field
    names filters by those field names.
    
    TODO: Raise a custom exception to be caught outside this function.
    """
    if variety_x_location_list is None:
			return self._variety_x_location

    inclusion_dict = {}
    for key in variety_x_location_list:
      try:
        inclusion_dict[key] = self._variety_x_location[key]
      except KeyError:
        pass # Silently fail
    
    return inclusion_dict
  
  def _get_recent(self, n_list = None, variety_x_location_list = None):
    """
    Return the data matching a list of variety_names in this object that
    is most recent in year, and has sufficient data in that year. If
    n_list is none, the most recent year is returned. If variety_x_location_list is
    None, all recent data are returned. An optional list of field names
    filters by those field names.
    """
    data = self._get(variety_x_location_list)
    
    recent_dict = {}
    for var_loc in data.keys():
      years = self._most_recent_years_with_sufficient_data(var_loc, n_list)
      for year in years:
				try:
					recent_dict[var_loc][year] = data[var_loc][year]
				except KeyError:
					recent_dict[var_loc] = {}
					recent_dict[var_loc][year] = data[var_loc][year]
    
    return recent_dict
    
  def _get_averages(self, n_list = None, variety_x_location_list = None, field_list = None):
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
		data = self._get_recent(n_list, variety_x_location_list)
    
    
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
					
		return averaged

  def fetch(self, n_list = None, variety_x_location_list = None, field_list = None):
		"""
		Main accessor method for this data. The optional fields n_list and 
		field_list are used to return a multi-year averaged field, while 
		fields not in field_list are returned as 1 (last) year averages. 
		When n_list is not supplied, a 1 year average is assumed. If no 
		field_list is supplied, results are calculated over all fields. An 
		optional list of variety names filters which varities are returned.
		
		returns a ranked list of dictionaries [ {variety_name: { entries: [objects], 1-yr-avg-fieldname: value, ... } }, ... ]
		where the ranking is determined by number of locations for that variety.
		"""
		if field_list is None:
			field_list = []
			exclusion_fields = self._include_fields
		else:
			exclusion_fields = list(set(self._include_fields).difference(set(field_list)))
			
		a = self._get_averages([1], variety_x_location_list, exclusion_fields)
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
		
		return [a]
