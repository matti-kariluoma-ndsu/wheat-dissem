class Cell:
	"""
	Helper class; Cells for our Table class.
	"""
	
	def __init__(self, trial, year, fieldname):
		self.clear()
		self.year = year
		self.fieldname = fieldname
	
	def __unicode__(self):
		value = self.get_rounded(self.year, self.fieldname)
		if value is None:
			unicode_repr = unicode('--')
		else:
			unicode_repr = unicode(value)
		return unicode_repr
		
	def __str__(self):
		return str(unicode(self))
	
	def get(self, year, fieldname):
		this_year = []
		for entry in self.members:
			if entry.harvest_date.date.year == year:
				this_year.append(entry)
				
		if not this_year:
			return None
		if len(this_year) > 1:
			print 'error'
		
		entry = this_year[0]
		try:
			value = getattr(entry, fieldname)
		except AttributeError:
			value = None
		
		return value
	
	def get_rounded(self, year, fieldname, digits=1):
		value = self.get(year, fieldname)
		if value is not None:
			value = round(value, digits)
		return value
	
	def clear(self):
		self.year = 0
		self.fieldname = "no_field"
		self.members = []

class Aggregate_Cell(Cell):
	"""
	A cell whose value is dependent upon its row
	"""
	def __init__(self, year, fieldname, row):
		self.clear()
		Cell.__init__(self, year, fieldname)
		self.row = row
		
	def clear(self):
		Cell.clear(self)
		self.row = None
