#!/usr/bin/env python
# coding: ascii

"""
Cell contains a list of trial_entry that have the same variety and 
location.
"""

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
				for cell in self.table.row(self.variety):
					if cell is None or isinstance(cell, Aggregate_Cell) or isinstance(cell, Empty_Cell): # Shouldn't see any other types
						continue
					for years_diff in range(self.table.column(self.location).years_back + 1):
						cur_year = year - years_diff
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
			"""2012-2011_55108.csv
			Variety,Saint Paul,Lamberton,Morris,Fergus Falls
			Albany,54.4,43.9,70.3,83.9
			Breaker,39.4,36.6,62.3,72.4
			Brennan,47.3,38.8,64.7,86.8
			Brick,31.6,34.4,60.6,71.7
			Briggs,41.3,43.1,73.6,76.7
			Cromwell,45.2,37,63.1,59.5
			Edge,40.5,30,55.6,71
			Faller,45.1,40.9,56.8,66
			Glenn,36.3,36.4,57.1,63.8
			Jenna,50.9,40.3,72.4,76.7
			Knudson,47.9,40.6,64.1,71
			Marshall,30.4,27.5,40.3,58.1
			Prosper,45.3,41.4,64.3,68.8
			RB07,45.2,40.8,55.8,68.8
			Rollag,37.8,36.6,57.1,71
			SY Soren,48.3,37.7,59.7,74.6
			Sabin,41,36.6,57.8,72.4
			Samson,47.7,38.4,67.1,83.9
			Select,35.7,38.2,67,81
			Vantage,38.7,36.7,53.6,60.2
			Velva,43.1,33.9,48.7,62.4
			WB-Digger,43.7,41.5,62.1,76
			WB-Mayville,48.2,40.9,59.6,82.5
			Albany,73.5,36.4,54.5,72.9
			Breaker,50.3,30.3,52.5,64.2
			Brennan,55.2,31.5,40.9,63.7
			Brick,46.6,31.1,48.9,67
			Briggs,54.7,38.6,54.5,68.4
			Cromwell,60.2,31.1,53.7,66
			Edge,51.6,28.2,44.5,59.3
			Faller,53.9,35.3,55.7,74.7
			Glenn,50.8,29.5,43.3,67.8
			Jenna,62.5,33.8,55.4,71.2
			Knudson,67.5,34.1,56.7,71.4
			Marshall,41,24.4,36.9,48.8
			Prosper,58.7,33.2,53.1,75
			RB07,54.9,31,48.5,63.1
			Rollag,37.3,29.1,44.1,63.6
			SY Soren,48.6,35.2,46.8,66
			Sabin,66.2,31.9,50.1,64.8
			Samson,65.9,33.4,52,73.3
			Select,59.1,39.5,56.4,70.4
			Vantage,58,28.5,47.2,62.4
			Velva,55.6,31.8,47.1,66.2
			WB-Digger,46.9,31.5,50.2,68.3
			WB-Mayville,52.2,31.6,48,65
			"""
			# 2012, LSD is 4.603553
			values[2012] = [
					[54.4,43.9,70.3,83.9],
					[39.4,36.6,62.3,72.4],
					[47.3,38.8,64.7,86.8],
					[31.6,34.4,60.6,71.7],
					[41.3,43.1,73.6,76.7],
					[45.2,37,63.1,59.5],
					[40.5,30,55.6,71],
					[45.1,40.9,56.8,66],
					[36.3,36.4,57.1,63.8],
					[50.9,40.3,72.4,76.7],
					[47.9,40.6,64.1,71],
					[30.4,27.5,40.3,58.1],
					[45.3,41.4,64.3,68.8],
					[45.2,40.8,55.8,68.8],
					[37.8,36.6,57.1,71],
					[48.3,37.7,59.7,74.6],
					[41,36.6,57.8,72.4],
					[47.7,38.4,67.1,83.9],
					[35.7,38.2,67,81],
					[38.7,36.7,53.6,60.2],
					[43.1,33.9,48.7,62.4],
					[43.7,41.5,62.1,76],
					[48.2,40.9,59.6,82.5]
				]
			# 2011, with 2012 LSD is 6.516289
			values[2011] = [
					[73.5,36.4,54.5,72.9],
					[50.3,30.3,52.5,64.2],
					[55.2,31.5,40.9,63.7],
					[46.6,31.1,48.9,67],
					[54.7,38.6,54.5,68.4],
					[60.2,31.1,53.7,66],
					[51.6,28.2,44.5,59.3],
					[53.9,35.3,55.7,74.7],
					[50.8,29.5,43.3,67.8],
					[62.5,33.8,55.4,71.2],
					[67.5,34.1,56.7,71.4],
					[41,24.4,36.9,48.8],
					[58.7,33.2,53.1,75],
					[54.9,31,48.5,63.1],
					[37.3,29.1,44.1,63.6],
					[48.6,35.2,46.8,66],
					[66.2,31.9,50.1,64.8],
					[65.9,33.4,52,73.3],
					[59.1,39.5,56.4,70.4],
					[58,28.5,47.2,62.4],
					[55.6,31.8,47.1,66.2],
					[46.9,31.5,50.2,68.3],
					[52.2,31.6,48,65]
				]
			del values[2011]
		if not values:
			value = None
		else:
			value = LSD_Calculator().calculate_lsd(
					values, 
					['Albany','Breaker','Brennan','Brick','Briggs','Cromwell','Edge','Faller','Glenn','Jenna','Knudson','Marshall','Prosper','RB07','Rollag','SY Soren','Sabin','Samson','Select','Vantage','Velva','WB-Digger','WB-Mayville'], 
					['Saint Paul','Lamberton','Morris','Fergus Falls'], 
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
