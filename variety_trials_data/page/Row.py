#!/usr/bin/env python
# coding: ascii

"""
Row contains a list of cells, and has a list-like interface:
	for cell in row
	row.append(cell)
	row.extend(cells)
	row_copy = Row(row)

:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

class Fake_Variety:
	"""
	Creates a simulacrum of models.Variety
	"""
	def __init__(self, name):
		self.name = name
		self.id = -1
		self.pk = -1
		
	def __unicode__(self):
		return unicode(self.name)
		
	def __str__(self):
		return str(unicode(self))

class Row:
	"""
	Contains references to each Cell in this row.
	The ordering of the cells comes from the page, through table.
	"""
	def __init__(self, row=None):
		self.clear()
		if row:
			self.extend([cell for cell in row])
		
	def __unicode__(self):
		header = unicode(self.variety)
		if len(header) > 7:
			row = [unicode('%s\t' % header)]
		else:
			row = [unicode('%s\t\t' % header)]
		row.extend([unicode(cell) for cell in self])
		return unicode("\t").join(row)
	
	def __str__(self):
		return str(unicode(self))
		
	def __iter__(self):
		"""
		Does not conform to Python 2.3:
		``The intention of the protocol is that once an iterator's next() 
		method raises StopIteration, it will continue to do so on 
		subsequent calls. Implementations that do not obey this property 
		are deemed broken.''
		http://docs.python.org/2/library/stdtypes.html#iterator-types
		"""
		index = 0
		iter_dict = self._cells
		iter_order = self.table.page.column_order
		#iter_show_missing = True
		
		while True:
			try:
				key = iter_order[index]
				index += 1
			except IndexError:
				raise StopIteration
			try:
				cell = iter_dict[key]
			except KeyError:
				cell = None
			
			#if cell is None and not iter_show_missing: continue
			
			yield cell
	
	def append(self, cell):
		if self.variety is None:
			self.variety = cell.variety
		self._cells[cell.location] = cell
	
	def extend(self, cells):
		if self.variety is None:
			try:
				cell = cells[0]
			except IndexError:
				return
			self.variety = cell.variety
		for cell in cells:
			self._cells[cell.location] = cell
	
	def clear(self):
		self._cells = {} # location: cell
		self.variety = None
		self.table = None

class Aggregate_Row(Row):
	"""
	A row containing aggregate_cells.
	"""
	def __init__(self, row=None):
		Row.__init__(self, row)
	
	def clear(self):
		Row.clear(self)
