#!/usr/bin/env python
# coding: ascii

"""
Table contains rows and columns of cells. Table has a list-like 
interface:
	for row in table
	for row in table.rows()
	for column in table.columns()
	table.append(cell)
	table.extend(cells)
	table_copy = Table(table)

In addition:
	row = table.row(variety)
	column = table.column(location)
"""

from variety_trials_data.page.Row import Row
from variety_trials_data.page.Column import Column
from variety_trials_data.page.Cell import Cell, Aggregate_Cell

class Table:
	"""
	References each Row and Column contained in this table.
	The ordering of the rows and columns come from the page.
	"""
	
	# Probability is required for creating the LSD row
	def __init__(self, table=None):
		self._rows = {} 
		self._columns = {} 
		self.clear()
		if table:
			self.extend([cell for row in table for cell in row])
				
	def __unicode__(self):
		return unicode("table")
	
	def __str__(self):
		return str(unicode(self))
		
	def __iter__(self):
		self.index = 0
		if self.iter_rows:
			self.iter_dict = self._rows
			self.iter_order = self.table.row_order
		else:
			self.iter_dict = self._cols
			self.iter_order = self.table.column_order
		return self
		
	def next(self):
		try:
			cell = self.iter_dict[self.iter_order[self.index]]
			self.index += 1
		except IndexError:
			self.iter_rows = True # reset state
			raise StopIteration
		return cell
	
	def rows(self):
		self.iter_rows = True
		return self
		
	def columns(self):
		self.iter_rows = False
		return self
	
	def row(self, variety):
		try:
			row = self._rows[variety]
		except KeyError:
			row = self._rows[variety] = Row()
			row.table = self
		return row
		
	def column(self, location):
		try:
			column = self._columns[location]
		except KeyError:
			column = self._columns[location] = Column()
			column.table = self
		return column
	
	def append(self, cell):
		self.row(cell.variety).append(cell)
		self.column(cell.location).append(cell)
		
	def extend(self, cells):
		for cell in cells:
			self.append(cell)
	
	def site_years(self):
		return tuple([8,12,16]) # i.e. (8, 12, 16)
	
	def clear(self):
		self.page = None
		self.iter_rows = True
		for row in self._rows.values():
			row.clear()
		self._rows = {} # variety: Row(), ...
		for column in self._columns.values():
			column.clear()
		self._columns = {} # location: Column(), ...
		
class Appendix_Table(Table):
	def __init__(self, table=None):
		"""
		"""
		Table.__init__(self, table)
	
	def columns(self):
		return []
		
	def clear(self):
		Table.clear(self)
