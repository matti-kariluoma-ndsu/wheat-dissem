#!/usr/bin/env python
# coding: ascii

"""
Column contains a list of cells and has a list-like interface:
	for cell in column
	column.append(cell)
	column.extend(cells)
	column_copy = Column(column)
"""

class Fake_Location:
	"""
	Creates a simulacrum of models.Location
	"""
	def __init__(self, name):
		self.name = name
		self.id = -1
		self.pk = -1
		
	def __unicode__(self):
		return unicode(self.name)
		
	def __str__(self):
		return str(unicode(self))
		
class Column:
	"""
	Contains references to each Cell in this column.
	The ordering of the cells comes from the page, through table.
	"""
	def __init__(self, column=None):
		self.clear()
		if column:
			self.extend([cell for cell in column])
	
	def __unicode__(self):
		header = unicode(self.location)
		if len(header) > 7:
			column = [unicode('%s\t' % header)]
		else:
			column = [unicode('%s\t\t' % header)]
		column = [unicode('%s\t\t' % self.location)]
		column.extend([unicode(cell) for cell in self])
		return unicode("\t").join(column)
		
	def __str__(self):
		return str(unicode(self))
		
	def __iter__(self):
		self.index = 0
		self.iter_dict = self._cells
		self.iter_order = self.table.page.row_order
		#self.iter_skip = []
		#self.iter_show_missing = False
		return self
		
	def next(self):
		try:
			key = self.iter_order[self.index]
			self.index += 1
		except IndexError:
			raise StopIteration
		try:
			cell = self.iter_dict[key]
		except KeyError:
			cell = None	
			
		if cell is None: #and not self.iter_show_missing:
			return self.next()
		
		return cell
	
	def append(self, cell):
		if self.location is None:
			self.location = cell.location
		self._cells[cell.variety] = cell
	
	def extend(self, cells):
		if self.location is None:
			try:
				cell = cells[0]
			except IndexError:
				return
			self.location = cell.location
		for cell in cells:
			self._cells[cell.variety] = cell
		
	def clear(self):
		self._cells = {} # variety: cell
		self.location = None
		self.table = None

class Aggregate_Column(Column):
	"""
	A column who contains all aggregate_cells, which in turn are used
	to calculate the running average for a variety.
	"""
	def __init__(self, column=None):
		Column.__init__(self, column)
		
	def site_years(self):
		return self.years_back
	
	def clear(self):
		Column.clear(self)
		self.years_back = 0
		



