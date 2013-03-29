#!/usr/bin/env python
# coding: ascii

"""
Cell contains a list of trial_entry that have the same variety and 
location.

:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from variety_trials_data.page.Row import Aggregate_Row
from variety_trials_data.page.Column import Aggregate_Column
from variety_trials_data.page.LSD_util import LSD_Calculator

class TrialNotMatched(Exception):
	def __init__(self, message=None):
		if not message:
			message = "Attempted to add a trial with a mismatched variety or location."
		Exception.__init__(self, message)

class ExtraneousTrial(Exception):
	def __init__(self, variety, location, year, fieldname):
		message = '''More than one trial found for the given parameters:
	variety:  \t"%s"
	location: \t"%s"
	year:     \t"%s"
	fieldname:\t"%s"\n''' % (variety, location, year, fieldname)
		Exception.__init__(self, message)

class UnbalancedData(Exception):
	def __init__(self, variety, location, year, fieldname):
		message = '''Could not compute an aggregate value for cell with:
	variety:  \t"%s"
	location: \t"%s"
	year:     \t"%s"
	fieldname:\t"%s"\n''' % (variety, location, year, fieldname)
		Exception.__init__(self, message)

class Cell:
	"""
	Helper class; Cells for our Table class.
	"""
	
	def __init__(self, variety, location, default_year, default_fieldname):
		self.clear()
		self.variety = variety
		self.location = location
		self.year = default_year
		self.fieldname = default_fieldname
	
	def __unicode__(self):
		try:
			value = self.get_rounded(self.year, self.fieldname)
		except ExtraneousTrial:
			value = None
		except UnbalancedData:
			value = None
			
		if value is None:
			unicode_repr = unicode('--')
		else:
			unicode_repr = unicode(value)
		return unicode_repr
		
	def __str__(self):
		return str(unicode(self))
	
	def append(self, trial):
		if trial.variety != self.variety or trial.location != self.location:
			raise TrialNotMatched()
		self._members.append(trial)
	
	def extend(self, trials):
		for trial in trials:
			self.append(trial)
	
	def get(self, year, fieldname):
		this_year = []
		for entry in self._members:
			if entry.harvest_date.date.year == year:
				this_year.append(entry)
				
		if not this_year:
			return None
		if len(this_year) > 1:
			raise ExtraneousTrial(self.variety, self.location, year, fieldname)
		
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
	
	def set_defaults(self, year, fieldname):
		self.year = year
		self.fieldname = fieldname
	
	def clear(self):
		self.variety = None
		self.location = None
		self.year = 0
		self.fieldname = "no_field"
		self._members = []
		
class LSD_Cell(Cell):
	"""
	A cell whose value is dependant on the location and year of the trial.
	Displays the LSD for those varieties at that location.
	"""
	def __init__(self, variety, location, default_year, default_fieldname, exemplar_cell):
		Cell.__init__(self, variety, location, default_year, default_fieldname)
		if exemplar_cell:
			self.extend(exemplar_cell._members)
	
	def append(self, trial):
		self._members.append(trial)
	
	def get(self, year, fieldname):
		lsd_fieldnames = ['lsd_05', 'hsd_10', 'lsd_10'] # ordered by predictive power
		for lsd_fieldname in lsd_fieldnames:
			self.fieldname = lsd_fieldname
			value = Cell.get(self, year, lsd_fieldname)
			if value is not None:
				break
		return value
	
	def clear(self):
		Cell.clear(self)

class Aggregate_Cell(Cell):
	"""
	A cell whose value is dependent upon its row
	"""
	def __init__(self, variety, location, default_year, default_fieldname):
		Cell.__init__(self, variety, location, default_year, default_fieldname)
	
	def get(self, year, fieldname):
		if (year in self.precalculated_value and	
				fieldname in self.precalculated_value[year] and	
				self.precalculated_value[year][fieldname] is not None):
			return self.precalculated_value[year][fieldname]
		else:
			values = []
			any_empty = False
			for years_diff in range(self.table.column(self.location).years_back + 1):
				cur_year = year - years_diff
				any_empty = any_empty or len(self.table.column(self.location).balanced_criteria[cur_year]) < 1
			if not any_empty:
				for years_diff in range(self.table.column(self.location).years_back + 1):
					cur_year = year - years_diff
					for cell in self.table.row(self.variety):
						if cell is None or isinstance(cell, Aggregate_Cell) or isinstance(cell, Empty_Cell):
							continue
						if cell.location in self.table.column(self.location).balanced_criteria[cur_year]:
							try:
								value = cell.get(cur_year, fieldname)
							except ExtraneousTrial:
								value = None
							if value is None:
								raise UnbalancedData(self.location, self.variety, year, fieldname)
							values.append(value)
			
		if not values:
			value = None
		else:
			value = sum(values) / len(values)			
			try:
				self.precalculated_value[year][fieldname] = value
			except KeyError:
				self.precalculated_value[year] = {}
				self.precalculated_value[year][fieldname] = value
		return value
						
	def clear(self):
		Cell.clear(self)
		self.precalculated_value = {}
		self.table = None
		
class LSD_Aggregate_Cell(Aggregate_Cell):
	"""
	Displays the LSD for Aggregate cells in it's column.
	"""
	def __init__(self, variety, location, default_year, default_fieldname, lsd_probability):
		Aggregate_Cell.__init__(self, variety, location, default_year, default_fieldname)
		self.lsd_probability = lsd_probability
		
	def get(self, year, fieldname):
		if (year in self.precalculated_value and	
				fieldname in self.precalculated_value[year] and	
				self.precalculated_value[year][fieldname] is not None):
			return self.precalculated_value[year][fieldname]
		else:
			values = {}
			varieties = []
			locations = []
			any_empty = False
			for years_diff in range(self.table.column(self.location).years_back + 1):
				cur_year = year - years_diff
				any_empty = any_empty or len(self.table.column(self.location).balanced_criteria[cur_year]) < 1
			if not any_empty:
				for column in self.table.columns():
					if isinstance(column, Aggregate_Column):
						continue
					locations.append(column.location.name)
				for row in self.table:
					if isinstance(row, Aggregate_Row):
						continue
					varieties.append(row.variety.name)
				for years_diff in range(self.table.column(self.location).years_back + 1):
					cur_year = year - years_diff
					values[cur_year] = this_years_values = []
					for row in self.table:
						if isinstance(row, Aggregate_Row):
							continue
						this_rows_values = []
						this_years_values.append(this_rows_values)
						for cell in row:
							if cell is None:
								this_rows_values.append(None)
								continue
							if isinstance(self.table.column(cell.location), Aggregate_Column):
								continue
							try:
								value = cell.get(cur_year, fieldname)
							except UnbalancedData:
								value = None
							except:
								value = None
							this_rows_values.append(value)
						
		if not values:
			value = None
		else:
			"""
			print '%s %s' % (self.table.site_years, self.location.name)
			for year in values:
				print year
				for row in values[year]:
					print '%d: %s' % (len(row), row)
			print "==="
			#"""
			value = LSD_Calculator().calculate_lsd(
					values, 
					varieties,
					locations,
					self.lsd_probability, 
					internal_implementation=False
				)
			try:
				self.precalculated_value[year][fieldname] = value
			except KeyError:
				self.precalculated_value[year] = {}
				self.precalculated_value[year][fieldname] = value
		return value
	
	def clear(self):
		Aggregate_Cell.clear(self)
		self.lsd_probability = 0.05

class Empty_Cell(Cell):
	"""
	A cell who has no value, is invisible, etc. Used to generate the rows
	in Appendix_Table.
	"""
	def __init__(self, variety, location, default_year=0, default_fieldname=""):
		Cell.__init__(self, variety, location, default_year, default_fieldname)
	
	def get(self, year, fieldname):
		return None	

	def clear(self):
		Cell.clear(self)
