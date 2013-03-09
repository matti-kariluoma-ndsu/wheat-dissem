#!/usr/bin/env python
# coding: ascii

"""
Cell contains a list of trial_entry that have the same variety and 
location.
"""

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
	def __init__(self, cell=None):
		if cell:
			Cell.__init__(self, cell.variety, cell.location, cell.year, cell.fieldname)
			self.extend(cell._members)
		else:
			self.clear()
	
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
	
	def __unicode__(self):
		return unicode(self.table.column(self.location).site_years)
	
	def get(self, year, fieldname):
		return None
		print '%s %s %s %s\n' % (self.location, self.variety, year, fieldname)
		if (year in self.precalculated_value and	
				fieldname in self.precalculated_value[year] and	
				self.precalculated_value[year][fieldname] is not None):
			return self.precalculated_value[year][fieldname]
		else:
			values = []
			#print self.table.column(self.location).years_back
			print [unicode(cell) for cell in self.table.row(self.variety) if not isinstance(cell, Aggregate_Cell)]
			for cell in self.table.row(self.variety):
				if isinstance(cell, Aggregate_Cell) or cell is None: # We should not find any other type of cell
					continue
				else:
					#print range(self.table.column(self.location).years_back + 1)
					for years_back in range(self.table.column(self.location).years_back + 1):
						try:
							value = cell.get(year - years_back, fieldname)
						except ExtraneousTrial:
							value = None
						
						if value is not None:
							values.append(value)
						else:
							raise UnbalancedData(self.location, self.variety, year, fieldname)
						
		if not values:
			raise UnbalancedData(self.location, self.variety, year, fieldname)
		else:
			value = sum(values) / len(values)			
			try:
				self.precalculated_value[year][fieldname] = value
			except KeyError:
				self.precalculated_value[year] = {}
				self.precalculated_value[year][fieldname] = value
		print value
		return value
						
	def clear(self):
		Cell.clear(self)
		self.precalculated_value = {}
		self.table = None
		
class LSD_Aggregate_Cell(Aggregate_Cell):
	"""
	Displays the LSD for Aggregate cells in it's column.
	"""
	def __init__(self, variety, location, default_year, default_fieldname):
		Aggregate_Cell.__init__(self, variety, location, default_year, default_fieldname)
	
	def __unicode__(self):
		return u'lsds'
	
	def clear(self):
		Aggregate_Cell.clear(self)
		self.table = None

class Empty_Cell(Cell):
	"""
	A cell who has no value, is invisible, etc. Used to generate the rows
	in Appendix_Table.
	"""
	def __init__(self, variety, location, default_year=0, default_fieldname=""):
		Cell.__init__(self, variety, location, default_year, default_fieldname)
		
	def clear(self):
		Cell.clear(self)
