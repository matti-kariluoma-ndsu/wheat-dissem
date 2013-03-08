#!/usr/bin/env python
# coding: ascii

"""
Row contains a list of cells, and has a list-like interface:
	for cell in row
	row.append(cell)
	row.extend(cells)
	row_copy = Row(row)
"""

class Fake_Variety:
	def __init__(self, name):
		self.name = name
		self.id = -1
		self.pk = -1

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
		row = [unicode(self.variety)]
		row.extend([unicode(cell) for cell in self])
		return unicode(" ").join(row)
	
	def __str__(self):
		return str(unicode(self))
		
	def __iter__(self):
		self.index = 0
		self.iter_dict = self._cells
		self.iter_order = self.table.page.column_order
		self.iter_skip = self.table.masked_locations
		#self.iter_show_missing = True
		return self
		
	def next(self):
		try:
			key = self.iter_order[self.index]
			self.index += 1
		except IndexError:
			raise StopIteration
			
		if key in self.iter_skip:
			cell = None
		else:
			try:
				cell = self.iter_dict[key]
			except KeyError:
				cell = None
		
		return cell
	
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
		

