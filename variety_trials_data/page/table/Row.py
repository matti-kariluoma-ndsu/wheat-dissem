from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv

class Row:
	"""
	Contains references to each Cell in this row.
	"""
	def __init__(self, variety):
		self.variety = variety
		self.members = {}
		self.clear()
	
	def __unicode__(self):
		row = [unicode(self.variety)]
		row.extend([unicode(cell) for cell in self])
		return unicode(" ").join(row)
	
	def __str__(self):
		return str(unicode(self))
		
	def __iter__(self):
		if self.key_order is None:
			self.keys = self.members.keys()
		else:
			self.keys = self.key_order
		self.key_index = 0
		return self
		
	def next(self):
		if self.key_index == len(self.keys):
			raise StopIteration
			
		try:
			key = self.keys[self.key_index]
		except IndexError:
			raise StopIteration
		
		try:
			cell = self.members[key]
		except KeyError:
			cell = None

		self.key_index = self.key_index + 1
		return cell
	
	def append(self, value):
		try:
			self.members[value.column.location] = value
		except AttributeError:
			col = self.members[None] = value
	
	def clear(self):
		self.members = {}
		self.key_order = None
		self.keys = None
		self.key_index = 0
		self.value_index = 0
		
class Fake_Variety:
	def __init__(self, name):
		self.name = name
		self.id = -1
		self.pk = -1

class LSD_Row(Row):
	"""
	A row that keeps track of which Table it belongs to.
	"""
	def __init__(self, variety, table):
		Row.__init__(self, variety)
		self.table = table
	
	def clear(self):
		Row.clear(self)
		self.table = None
