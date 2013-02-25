from variety_trials_data.page import Cell, Column, Row

class Table:
	"""
	Creates an object with lists for fields that are suitable for a
	tabular layout. The header dictionary contains the year(s)'- and 
	location(s)' column headers.  The last list is a list of all the 
	LSD calculations for the given entry.
	
	Year Loc1 Loc2 Loc3 ...
	Var1 *    *    *    ...
	Var2 *    *    *    ...
	...  ...  ...  ...  ...
	"""
	
	# Probability is required for creating the LSD row
	def __init__(self, locations, visible_locations, lsd_probability, max_year, min_year, default_fieldname): 
		self.lsd_probability = lsd_probability
		self.locations = list(locations) # create a copy
		self.visible_locations = list(visible_locations) # create a copy
		self.min_year = min_year
		self.max_year = max_year
		self.default_year = max_year
		self.default_fieldname = default_fieldname
		self.cells = {} # (variety, location): Cell()
		self.rows = {} # variety: Row(), ...
		self.columns = {} # location: Column(), ...
	
	def clear(self):
		self.min_year = None
		self.max_year = None
		self.locations = []
		self.visible_locations = []
		for cell in self.cells.values():
			cell.clear()
		for row in self.rows.values():
			row.clear()
		for column in self.columns.values():
			column.clear()
		self.cells = {}
		self.rows = {}
		self.columns = {}
	
	def get_row(self, variety):
		try:
			row = self.rows[variety]
		except KeyError:
			row = self.rows[variety] = Row(variety)
			row.set_key_order(self.visible_locations) # pass by reference
		return row	
	
	def get_column(self, location):
		try:
			col = self.columns[location]	
		except KeyError:
			col = self.columns[location] = Column(location)
		return col
		
	def add_cell(self, variety, location, cell):
		row = self.get_row(variety)
		column = self.get_column(location)
		cell.row = row
		cell.column = column
		row.append(cell)
		column.append(cell)
		self.cells[(variety, location)] = cell
	
	def sorted_rows(self):
		alpha_sorted = sorted(self.rows.items(), key=lambda (variety, row): variety.name) # sort by variety.name
		
		## Move the LSD row to the end of the list
		lsd_row = None
		for variety in self.rows:
			if variety.name == "LSD":
				lsd_row = (variety, self.rows[variety])
				break
		if lsd_row is not None:
			alpha_sorted.remove(lsd_row) # remove it from its alphabetical position
			alpha_sorted.append(lsd_row) # append it to the end of the list
			
		return alpha_sorted
	
	def sorted_visible_columns(self):
		sorted_column_tuples = []
		for location in self.visible_locations:
			column = self.get_column(location)
			if isinstance(column, Aggregate_Column) and column.site_years == None:
				for cell in column:
					if cell.site_years > column.site_years:
						column.site_years = cell.site_years
						
			sorted_column_tuples.append( (column, location) )
			
		return sorted_column_tuples
	
	def get_site_years(self):
		site_years = {} # i.e. {1: 8, 2: 12, 3: 16}
		for location in self.visible_locations:
			column = self.get_column(location)
			if isinstance(column, Aggregate_Column):
				# init variable if None
				if column.site_years == None:
					for cell in column:
						if cell.site_years > column.site_years:
							column.site_years = cell.site_years
				site_years[len(column.years_range)] = column.site_years 
		result = []
		for key in sorted(site_years.keys()):
			result.append(site_years[key])
		return tuple(result) # i.e. (8, 12, 16)
	
	def set_defaults(self, year, fieldname):
		for cell in self.cells.values():
			cell.year = year
			cell.fieldname = fieldname
			
	def mask_locations(self, not_locations):
		"""
		Mask not_locations from this table. This function will unmask any
		locations _not_ found in not_locations, as well.
		
		not_locations: the locations to mask/hide
		"""
		#
		# Note: we cannot reassign self.visible_locations, all of our
		# rows our pointing to its reference.
		#
		locations = list(self.locations)
		
		delete_these = []
		for (index, location) in enumerate(locations):
			if location in not_locations:
				delete_these.append(index)
				
		for index in sorted(delete_these, reverse=True):
			locations.pop(index)
		
		# mutate table.visible_locations by removing locations to be masked
		delete_these = []
		for (index, location) in enumerate(self.visible_locations):
			if location not in locations:
				delete_these.append(index)
				
		for index in sorted(delete_these, reverse=True):
			self.visible_locations.pop(index)
		
		# insert into table.visible_locations locations that have been unmasked
		insert_these = []
		for (index, location) in enumerate(locations):
			if location not in self.visible_locations:
				insert_these.append(index)
				
		for index in insert_these:
			self.visible_locations.insert(index, locations[index])
		
		for column in self.columns.values():
			if isinstance(column, Aggregate_Column):
				for cell in column:
					if isinstance(cell, Aggregate_Cell):
						cell.calculate_site_years()
				column.site_years = None # force recalculation
				
	def __unicode__(self):
		tables = []
		for year in range(self.min_year, self.max_year+1):
			self.set_defaults(year, self.default_fieldname)
			table = []
			row = [unicode(year)]
			for (column, location) in self.sorted_visible_columns():
				row.append(unicode(location))
			table.append(unicode(" ").join(row))
			for (variety, row) in self.sorted_rows():
				table.append(unicode(row))
			tables.append(unicode("\n").join(table))
		return unicode("\n\n").join(tables)
		
class Appendix_Table(Table):
	def __init__(self, locations, visible_locations, lsd_probability, max_year, min_year, default_fieldname):
		"""
		location: a Location (or Fake_Location) object
		year_num: an integer denoting the number of years to go back for averaging i.e. 3
		"""
		Table.__init__(self, locations, visible_locations, lsd_probability, max_year, min_year, default_fieldname)
	
	def add_cell(self, variety, location=None, cell=None):
		row = self.get_row(variety)
		row.set_key_order(None)
	
	def sorted_visible_columns(self):
		return []
