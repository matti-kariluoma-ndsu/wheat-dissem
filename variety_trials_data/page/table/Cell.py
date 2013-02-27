class Cell:
	"""
	Helper class; Cells for our Table class.
	"""
	
	def __init__(self, year, fieldname):
		self.clear()
		self.year = year
		self.fieldname = fieldname
		
	def __iter__(self):
		self.index = 0
		return self
	
	def next(self):
		if self.index == len(self.members):
			raise StopIteration
		value = self.members[self.index]
		self.index = self.index + 1
		return value 
	
	def append(self, value):
		self.members.append(value)
	
	def delete_row(self):
		self.row = None
	
	def delete_column(self):
		self.column = None
	
	def clear(self):
		self.delete_row()
		self.delete_column()
		self.members = []
		self.index = 0
		self.year = 0
		self.fieldname = "no_field"
	
	def get(self, year, fieldname):
		this_year = []
		for entry in self.members:
			if entry.harvest_date.date.year == year:
				this_year.append(entry)
		#print this_year
		
		values = []
		for entry in this_year:
			try:
				value = getattr(entry, fieldname)
			except AttributeError:
				value = None
			if value is not None:
				values.append(value)

		mean = None
		if len(values) > 0:
			mean = float(sum(values)) / float(len(values))
		
		return mean
	
	def get_rounded(self, year, fieldname, digits=1):
		value = self.get(year, fieldname)
		if value is not None:
			value = round(value, digits)
		return value
	
	def __unicode__(self):
		unicode_repr = self.get_rounded(self.year, self.fieldname)
		if unicode_repr is None:
			unicode_repr = u'--'
		else:
			unicode_repr = unicode(str(unicode_repr))
		return unicode_repr


class Aggregate_Cell(Cell):
	"""
	A cell whose value is based upon its row
	"""
	def __init__(self, year, fieldname, row, column, decomposition, visible_locations):
		"""
		year: passed on to Cell
		fieldname: passed on to Cell
		row: the row this aggregate_cell is in
		column: the column this aggregate_cell is in
		decomposition: a truth table of what data we have
		"""
		Cell.__init__(self, year, fieldname)
		self.row = row
		self.column = column
		# Note we are not making a copy of decomposition; do not mutate
		self.decomposition = decomposition # {year: {variety: {location: bool, ...}, ...}, ...}
		# Note we are not making a copy of visible_locations; do not mutate
		self.visible_locations = visible_locations
		self.calculate_site_years()
	
	def calculate_site_years(self):
		self.site_years = 0
		if not isinstance(self.row, LSD_Row):
			cell = None
			for cell in self.row:
				if cell is not None and not isinstance(cell, Aggregate_Cell):
					break
			if cell is not None and not isinstance(cell, Aggregate_Cell):
				for year_diff in self.column.years_range:
					year = self.year - year_diff
					min_site_years = 10000
					if year in self.decomposition:
						for col_cell in cell.row:
							if col_cell is not None:
								variety = col_cell.row.variety
								if variety in self.decomposition[year]:
									truth_table = self.decomposition[year][variety]
									site_years = len([location for location in self.visible_locations if not isinstance(location, Fake_Location) and truth_table[location]])
									if site_years < min_site_years:
										min_site_years = site_years
					if min_site_years == 10000:
						min_site_years = 0
					self.site_years = self.site_years + min_site_years
	
	def append(self, value):
		return
	
	def get(self, year, fieldname):
		balanced = True
		values = []
		if not isinstance(self.row, LSD_Row):
			for cell in self.row:
				if balanced and cell is not None and not isinstance(cell, Aggregate_Cell):
					for year_diff in self.column.years_range:
						cell_mean = cell.get(year - year_diff, fieldname)
						if cell_mean is None:
							# This subset is not balanced across years!
							pass # we will count the number of means found later
						else:
							values.append(cell_mean)
						
		
		mean = None
		if len(values) > 0 and len(values) >= self.column.site_years:
			mean = round(float(sum(values)) / float(len(values)), 1)
		
		return mean
	
	def clear(self):
		Cell.clear(self)
		self.decomposition = {}
		self.visible_locations = []
		self.site_years = 0

