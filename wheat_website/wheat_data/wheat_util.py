from wheat_data.models import Trial_Entry #, Date

class Trial_x_Variety_x_Year:
  """ 
  Organizational class for our Trial_Entry x Variety x Year data.
  Pass in a django queryset and the fields you want to consider for
  averaging.
  """
  # A dictionary of variety_name to a year dictionary with Trial_Entry 
  # objects and their count.
  # {'name': {'year': [count, [trial_entry_objects]]}}
  _varieties = {}
  _include_fields = []
  
  def __init__(self):
    pass
        
  def __init__(self, query_set, field_list = None):
    """ 
    Initializes with all elements matching field_list in query_set, or
    all elements if field_list is None.
    """
    return populate(self, query_set, field_list)
    
  def populate(self, query_set, field_list = None):
    """ 
    Adds all elements matching field_list in query_set, or all elements 
    if field_list is None.
    
    TODO: Verify the fields that are passed in are actual fields
    """
    # Bring field_list to a consistent state
    if field_list is None:
      field_list = []
      for field in models.Trial_Entry._meta.fields:
				if (field.get_internal_type() == 'DecimalField' 
						or field.get_internal_type() == 'PositiveIntegerField' 
						or field.get_internal_type() == 'SmallIntegerField'
						or field.get_internal_type() == 'IntegerField'):
						field_list.append(field) # only consider averageable data
						
    self._include_fields = field_list
    
    # Initialize our inner data structures
    for entry in query_set:
      name = str(entry.variety.name) # force evaluation
      year = str(entry.harvest_date.date.year)
      try:
        self._varieties[name][year][0] += 1
        self._varieties[name][year][1].append(entry)
      except KeyError:  # initialize and add the first value
        self._varieties[name] = {}
        self._varieties[name][year] = [1, [entry]]
    


  def _most_recent_year_with_sufficient_data(self, variety_name, n_list = None):
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
    return sorted(self._varieties[name].keys(), reverse=True)[:max(n_list):]
  
  def _get(self, variety_list = None, field_list = None):
    """ 
    Return all data held in this object matching variety_list. If
    variety_list is None all data is returned. If a name appears
    in variety_list that isn't in our data, that fetch for non-existent
    data silently fails and we continue on. An optional list of field
    names filters by those field names.
    
    TODO: Raise a custom exception to be caught outside this function.
    """
    if variety_list is None:
			variety_list = self._varieties.keys()
			
    if field_list is None:
      field_list = self._include_fields

    inclusion_dict = {}
    for name in variety_list:
      try:
        inclusion_dict[name] = self._varieties[name]
      except KeyError:
        pass # Silently fail
    
    return inclusion_dict
  
  def _get_recent(self, n_list = None, variety_list = None, field_list = None):
    """
    Return the data matching a list of variety_names in this object that
    is most recent in year, and has sufficient data in that year. If
    n_list is none, the most recent year is returned. If variety_list is
    None, all recent data are returned. An optional list of field names
    filters by those field names.
    """
    data = _get(self, variety_list, field_list)
    
    recent_dict = {}
    for name in data.keys():
      years = _most_recent_years_with_sufficient_data(self, name, n_list)
      for year in years:
				recent_dict[name] = {}
				recent_dict[name][year] = data[name][year]
    
    return recent_dict
    
  def _get_averages(self, n_list = None, variety_list = None, field_list = None):
    """
    Given a list of the number of dates to go back (e.g. [1,2,3] for the
    1-yr, 2-yr, and 3-yr averages), return those averaged data. An 
    optional list of varieties filers by those varieties, and an 
    optional list of fieldnames filters by those fieldnames.
    
    The returned dictionary tags the keys of the averaged items, 
    prepending `1-yr-avg-' `2-year-avg-' etc. based on the values in 
    n_list.
    """
    data = _get_recent(self, n_list, variety_list, field_list)
    
    return data

  def fetch(self, n_list = None, variety_list = None, field_list = None):
    """
    Main accessor method for this data. The optional fields n_list and 
    field_list are used to return a multi-year averaged field, while 
    fields not in field_list are returned as 1 (last) year averages. 
    When n_list is not supplied, a 1 year average is assumed. If no 
    field_list is supplied, results are calculated over all fields. An 
    optional list of variety names filters which varities are returned.
    """
    if field_list is None:
			field_list = []
			exclusion_fields = self._include_fields
		else:
			exclusion_fields = list(set(self._include_fields).difference(set(field_list)))
		
		return _get_averages(self, [1], variety_list, exclusion_fields).update(
			_get_averages(self, n_list, variety_list, field_list)
		)
