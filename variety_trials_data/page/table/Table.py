from variety_trials_data.page.table.Row import Row, LSD_Row
from variety_trials_data.page.table.Column import Column, Aggregate_Column
from variety_trials_data.page.table.Cell import Cell, Aggregate_Cell

class Table:
	"""
	Creates an object with lists for fields that are suitable for a
	tabular layout. The header dictionary contains the year(s)'- and 
	location(s)' column headers.  The last list is a list of all the 
	LSD calculations for the given entry.
	
	Year Loc1 Loc2 Loc3 ...
	Var1 *    *    *    ...
	Var2 *    *    *    ...
	...  ...  ...  ...  ...
	"""
	
	# Probability is required for creating the LSD row
	def __init__(self, page):
		self.clear()
		self.page = page
				
	def __unicode__(self):
		return unicode("table")
	
	def __str__(self):
		return str("table")
		
	def __iter__(self):
		return self
		
	def next(self):
		cell = None
		return cell
	
	def rows(self):
		return self
		
	def columns(self):
		return self
		
	def site_years(self):
		return tuple([8,12,16]) # i.e. (8, 12, 16)
	
	def clear(self):
		self.page = None
		self.rows = {} # variety: Row(), ...
		self.columns = {} # location: Column(), ...
		
class Appendix_Table(Table):
	def __init__(self):
		"""
		location: a Location (or Fake_Location) object
		year_num: an integer denoting the number of years to go back for averaging i.e. 3
		"""
		Table.__init__(self):
	
	def columns(self):
		return []
