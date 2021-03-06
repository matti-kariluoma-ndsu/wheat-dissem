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

:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from variety_trials_data.page.Row import Row, Aggregate_Row, Fake_Variety
from variety_trials_data.page.Column import Column, Aggregate_Column, Fake_Location
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
		table = [unicode(self.site_years)]
		table.extend([unicode(row) for row in self])
		return unicode("\n").join(table)
	
	def __str__(self):
		return str(unicode(self))
	
	def _iter_generator(self, iter_dict, iter_order, iter_show_missing):
		index = 0
		while True:
			try:
				key = iter_order[index]
				index += 1
			except IndexError:
				self.iter_rows = True # reset state
				raise StopIteration

			try:
				collection = iter_dict[key]
			except KeyError:
				collection = None

			if collection is None and not iter_show_missing:
				continue
			
			yield collection
	
	def __iter__(self):
		"""
		Does not conform to Python 2.3:
		``The intention of the protocol is that once an iterator's next() 
		method raises StopIteration, it will continue to do so on 
		subsequent calls. Implementations that do not obey this property 
		are deemed broken.''
		http://docs.python.org/2/library/stdtypes.html#iterator-types
		"""
		# iterate through rows
		iter_dict = self._rows
		iter_order = self.page.row_order
		iter_show_missing = False
		return self._iter_generator(iter_dict, iter_order, iter_show_missing)
	
	def rows(self):
		return self
		
	def columns(self):
		# iterate through columns
		iter_dict = self._columns
		iter_order = self.page.column_order
		iter_show_missing = True
		return self._iter_generator(iter_dict, iter_order, iter_show_missing)
	
	def row(self, variety):
		try:
			row = self._rows[variety]
		except KeyError:
			if not isinstance(variety, Fake_Variety):
				row = self._rows[variety] = Row()
			else:
				row = self._rows[variety] = Aggregate_Row()
			row.table = self
		return row
		
	def column(self, location):
		try:
			column = self._columns[location]
		except KeyError:
			if not isinstance(location, Fake_Location):
				column = self._columns[location] = Column()
			else:
				column = self._columns[location] = Aggregate_Column()
			column.table = self
		return column
	
	def append(self, cell):
		self.row(cell.variety).append(cell)
		self.column(cell.location).append(cell)
		
	def extend(self, cells):
		for cell in cells:
			self.append(cell)
	
	def clear(self):
		self.page = None
		for row in self._rows.values():
			row.clear()
		self._rows = {} # variety: Row(), ...
		for column in self._columns.values():
			column.clear()
		self._columns = {} # location: Column(), ...
		self.site_years = () # a tuple, one for each aggregate column.
		
class Appendix_Table(Table):
	def __init__(self, table=None):
		"""
		"""
		Table.__init__(self, table)
	
	def columns(self):
		return []
		
	def clear(self):
		Table.clear(self)
