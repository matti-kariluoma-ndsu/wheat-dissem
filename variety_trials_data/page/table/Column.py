class Column:
	"""
	Contains references to each Cell in this column.
	"""
	def __init__(self, location):
		self.location = location
		self.members = []
		self.index = 0
	
	def __iter__(self):
		self.index = 0
		return self
	
	def next(self):
		if self.index == len(self.members):
			raise StopIteration
		cell = self.members[self.index]
		self.index = self.index + 1
		return cell
	
	def append(self, value):
		self.members.append(value)
		
	def clear(self):
		for m in self.members:
			if isinstance(m, Cell):
				m.delete_column()
		self.members = []
		self.index = 0
		
	def __unicode__(self):
		column = [unicode(self.location)]
		column.extend([unicode(cell) for cell in self])
		return unicode(" ").join(column)

class Aggregate_Column(Column):
	"""
	A column whose cells' value is determined by other cells in its row
	"""
	def __init__(self, location, year_num):
		"""
		location: a Location (or Fake_Location) object
		year_num: an integer denoting the number of years to go back for averaging i.e. 3
		"""
		Column.__init__(self, location)
		self.members = []
		self.clear()
		self.years_range = range(year_num)
		
	def get_site_years(self):
		return self.site_years
		
	def clear(self):
		Column.clear(self)
		self.site_years = None
		self.years_range = []

class Fake_Location:
	def __init__(self, name):
		self.name = name
		self.id = -1
		self.pk = -1
