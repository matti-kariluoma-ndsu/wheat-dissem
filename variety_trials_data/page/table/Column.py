class Column:
	"""
	Contains references to each Cell in this column.
	"""
	def __init__(self, location, page):
		self.clear()
		self.location = location
		self.page = page
	
	def __unicode__(self):
		column = [unicode(self.location)]
		column.extend([unicode(cell) for cell in self])
		return unicode(" ").join(column)
		
	def __str__(self):
		return str(unicode(self))
		
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
		self.members = []
		self.index = 0
		self.site_years = 8
		self.location = None
		self.page = None

class Fake_Location:
	def __init__(self, name):
		self.name = name
		self.id = -1
		self.pk = -1

class Aggregate_Column(Column):
	"""
	A column whose cells' value is determined by other cells in its row
	"""
	def __init__(self, location, years_back):
		"""
		location: a Location (or Fake_Location) object
		year_num: an integer denoting the number of years to go back for averaging i.e. 3
		"""
		Column.__init__(self, location)
		self.years_back = years_back
		
	def clear(self):
		Column.clear(self)
		years_back = 1


