#!/usr/bin/env python
# coding: ascii

"""
Page contains a collection of models.trial_entry, organized as
cells -> rows, columns -> tables. Each of these objects has
a list-like interface:
	for table in page
	for row in table
	for row in table.rows()
	for column in table.columns()
	for cell in row
	for cell in column
	page.append(table)
	page.extend(tables)
	table.append(cell)
	table.extend(cells)
	row.append(cell)
	row.extend(cells)
	column.append(cell)
	column.extend(cells)
	cell.append(trial_entry)
	cell.extend(trial_entries)
	table_copy = Table(table)
	row_copy = Row(row)
	column_copy = Column(column)

In addition:
	row = table.row(variety)
	column = table.column(location)

"""

from variety_trials_data.models import Trial_Entry, Date
from variety_trials_data import models
from variety_trials_data.page.table.Table import Table
from variety_trials_data.page.table.Row import Row, LSD_Row
from variety_trials_data.page.table.Column import Column, Aggregate_Column
from variety_trials_data.page.table.Cell import Cell, Aggregate_Cell
import datetime

class LSDProbabilityOutOfRange(Exception):
	def __init__(self, message=None):
		if not message:
			message = "The alpha-value for the LSD calculation was out of range."
		Exception.__init__(self, message)

class TooFewDegreesOfFreedom(Exception):
	def __init__(self, message=None):
		if not message:
			message = "Could not calculate the LSD, too few degrees of freedom in the input."
		Exception.__init__(self, message)
		
class NotEnoughDataInYear(Exception):
	def __init__(self, message=None):
		if not message:
			message = "The selected year does not have any data for viewing."
		Exception.__init__(self, message)

class Page:
	def _get_entries(self, min_year, max_year, locations, number_locations, variety_names):
		"""
		First calls multiple count() calls to the database, and deletes
		locations from the page that contain no data.
		
		Then, the number of locations is truncated to `number_locations'.
		
		Finally, the truncated locations and trial entry objects are queried 
		for and returned.
		
		min_year: the oldest data to retrieve
		max_year: the newest data to retrieve
		locations: the (previosuly sorted) list of locations to consider
		number_locations: the length to truncate the list of locations to
		variety_names: list of varieties to limit ourselves to
		
		"""
		this_year_dates = models.Date.objects.filter(
				date__range=(datetime.date(max_year,1,1), datetime.date(max_year,12,31))
			)
			
		all_dates = models.Date.objects.filter(
				date__range=(datetime.date(min_year,1,1), datetime.date(max_year,12,31))
			)
		#
		## Only use locations with data in the current year
		#
		locations_with_data = []
		for loc in locations:
			if models.Trial_Entry.objects.filter(
					location=loc
				).filter(
					harvest_date__in=this_year_dates
				).filter(
					hidden=False
				).count() > 0:
					locations_with_data.append(loc)
			if len(locations_with_data) >= number_locations:
				break
		
		result = models.Trial_Entry.objects.select_related(
				'location', 'variety', 'harvest_date__date'
			).filter(
				location__in=locations_with_data
			).filter(
				harvest_date__in=all_dates
			).filter(
				hidden=False
			)
				
		if len(variety_names) > 0:
			result = result.filter(
					variety__in=models.Variety.objects.filter(
							name__in=variety_names
						)
				)
				
		return (locations_with_data, result)
	
	def _process_entries(self, default_year, year_range, locations, number_locations, varieties):
		(locations, entries) = self._get_entries(
				default_year - year_range, 
				default_year, 
				locations, 
				number_locations, 
				varieties
			)
		
		for entry in entries:
			year = entry.harvest_date.date.year
			variety = entry.variety
			location = entry.location
			try:
				cell = self.cells[variety][location]
			except KeyError:
				try:
					d = self.cells[variety]
				except KeyError:
					d = self.cells[variety] = {}
				cell = d[location] = Cell(default_year, default_fieldname)
					
			cell.append(entry)
			
			try:
				d = self.is_data_present[year][variety]
			except KeyError:
				try:
					d = self.is_data_present[year][variety] = dict([(l, False) for l in locations])
				except KeyError:
					self.is_data_present[year] = {}
					d = self.is_data_present[year][variety] = dict([(l, False) for l in locations])
					
			try:
				d[location] = True
			except KeyError:
				pass
			
		# ensure we have enough data for this year
		if default_year not in self.is_data_present:
			years = self.is_data_present.keys()
			if len(years) > 0:
				default_year = sorted(years, reverse=True)[0]
				self.set_defaults(default_year, default_fieldname)
			else:
				raise NotEnoughDataInYear("Not enough data in year %s" % (default_year))
	
	def _mask_locations(self, locations):
		visible_locations = list(locations) # make a copy
		
		if len(not_locations) > 0:
			delete_these = []
			for (index, location) in enumerate(visible_locations):
				if location in not_locations:
					delete_these.append(index)
					
			for index in sorted(delete_these, reverse=True):
				visible_locations.pop(index)
				
		return visible_locations
	
	def _make_appendix(self):
		table = Appendix_Table(self)
		for variety in models.Variety.objects.all():
			if variety not in self.cells:
				table.rows.append(variety)		
		self._tables.append(table)
	
	def _copy_rows_to_remaining_tables(self):
		try:
			prev_table = self._tables[0]
		except IndexError:
			return
			
		for table in self:
			for row in prev_table:
				# continue if a decorative element
				if isinstance(row.variety, Fake_Variety):
					continue
				table.rows.append(Row(row))

	def __init__(self, locations, number_locations, not_locations, 
			default_year, year_range, default_fieldname, lsd_probability, 
			break_into_subtables=False, varieties=[], show_appendix_tables=False,
			number_of_tables=3, all_varieties_in_subtables=False):
		self._tables = []
		self.clear()
		
		# populate self.cells and self.is_data_present
		self._process_entries(default_year, year_range, locations, number_locations, varieties)
				
		# Make tables from self.cells
		if break_into_subtables:
			# Sort/split the tables
			
			# Sort the varieties by number of locations they appear in.
			variety_order = sorted(self.is_data_present[default_year], key = lambda variety: self.is_data_present[default_year][variety], reverse=True)
			
			if len(variety_order) < 1:
				break_into_subtables = False
			else:
				prev = variety_order[0]
				
				# Move balanced varieties to their own tables
				table = Table(locations, visible_locations, lsd_probability, default_year, default_year - year_range, default_fieldname)
				self.append(table)
				for variety in variety_order:
					if not isinstance(table, Appendix_Table) and self.is_data_present[default_year][variety] != self.is_data_present[default_year][prev]:
						prev = variety
						if len([location for location in self.is_data_present[default_year][prev] if self.is_data_present[default_year][prev][location]]) >= len(visible_locations) / 2:
							table = Table(locations, visible_locations, lsd_probability, default_year, default_year - year_range, default_fieldname)
							self.append(table)
						else:
							table = Appendix_Table(locations, visible_locations, lsd_probability, default_year, default_year - year_range, default_fieldname)
							self.append(table)
					
					for (location, cell) in self.cells[variety].items():
						table.add_cell(variety, location, cell)
		
		if not break_into_subtables:
			table = Table(locations, visible_locations, lsd_probability, default_year, default_year - year_range, default_fieldname)
			self.append(table)
			for variety in self.cells:
				for location in self.cells[variety]:
					cell = self.cells[variety][location]
					table.add_cell(variety, location, cell)
		
		
		self._make_appendix()
		
		# Decorate the tables
		for table in self._tables:
			## Add LSD rows
			variety_key = Fake_Variety("LSD")
			row = LSD_Row(variety_key, table)
			table.rows[variety_key] = row
			for column in table.columns.values():
				cell = Cell(default_year, default_fieldname)
				table.add_cell(variety_key, column.location, cell)
			## Add aggregate columns
			for year_num in sorted(range(year_range), reverse=True):
				year_num = year_num + 1 # star counting from 1, not 0
				location_key = Fake_Location("%s-yr" % (year_num))
				table.locations.insert(0, location_key)
				table.visible_locations.insert(0, location_key)
				column = Aggregate_Column(location_key, year_num)
				table.columns[location_key] = column
				for row in table.rows.values():
					cell = Aggregate_Cell(default_year, default_fieldname, row, column, self.is_data_present, table.visible_locations)
					table.add_cell(row.variety, location_key, cell)
					
		# sort descending by site-years tuple, i.e. [(8, 12, 16), ...]
		self.data_tables = sorted(self.data_tables, key=lambda (table): table.get_site_years(), reverse=True)
		# truncate number of tables
		self.extra_tables = self.data_tables[number_of_tables:]
		self.data_tables = self.data_tables[:number_of_tables]
		
		# add data from higher-order tables to lower-order ones (ordering is by site-years)
		if all_varieties_in_subtables:
			self._copy_rows_to_remaining_tables()
	
	def __unicode__(self):
		return unicode("page")
	
	def __str__(self):
		return str(unicode(self))
	
	def __iter__(self):
		return self
		
	def next(self):
		table = None
		return table
	
	def append(self, table):
		table.page = self
		self._tables.append(table)
		
	def extend(self, tables):
		for table in tables:
			self.append(table)
	
	def tables():
		return self
	
	def set_defaults(self, year, fieldname):
		for variety in self.self.cells:
			for cell in self.self.cells[variety].values():
				cell.set_defaults(year, fieldname)
			
	def clear(self):
		for table in self._tables:
			table.clear()
		self._tables = []	
		self.is_data_present = {} # {year: {variety: {location: bool, ...}, ...}, ...}
		self.cells = {} # variety: {location: Cell() }
 
