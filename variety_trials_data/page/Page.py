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

:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from variety_trials_data.models import Trial_Entry, Date
from variety_trials_data import models
from variety_trials_data.page.Table import Table, Appendix_Table
from variety_trials_data.page.Row import Row, Aggregate_Row, Fake_Variety
from variety_trials_data.page.Column import Column, Aggregate_Column, Fake_Location
from variety_trials_data.page.Cell import Cell, Aggregate_Cell, Empty_Cell, LSD_Aggregate_Cell, LSD_Cell
import datetime
		
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
		
		varieties = models.Variety.objects.filter(
				name__in=variety_names
			)
		#
		## Only use locations with data in the current year
		#
		locations_with_data = []
		query = models.Trial_Entry.objects.filter(
				harvest_date__in=this_year_dates
			).filter(
				hidden=False
			)
		for loc in locations:
			query_loc = query.filter(
					location=loc
				)
			
			if len(variety_names) > 0:
				query_loc = query_loc.filter(
						variety__in=varieties
					)
			
			if query_loc.count() > 0:
				locations_with_data.append(loc)
					
			# number_locations == len(locations) if variety_names is populated, else some lesser number (8 as of writing)
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
					variety__in=varieties
				)
				
		return (locations_with_data, result)
	
	def _process_entries(self, year_range, locations, number_locations, varieties):
		(locations_with_data, entries) = self._get_entries(
				self.year - year_range, 
				self.year, 
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
				cell = d[location] = Cell(variety, location, self.year, self.fieldname)
					
			cell.append(entry)
			
			try:
				d = self.is_data_present[year][variety]
			except KeyError:
				try:
					d = self.is_data_present[year][variety] = dict([(l, False) for l in locations_with_data])
				except KeyError:
					self.is_data_present[year] = {}
					d = self.is_data_present[year][variety] = dict([(l, False) for l in locations_with_data])
					
			try:
				d[location] = True
			except KeyError:
				pass
			
		# ensure we have enough data for this year
		if self.year not in self.is_data_present:
			years = self.is_data_present.keys()
			if len(years) > 0:
				self.year = sorted(years, reverse=True)[0]
				self.set_defaults(self.year, self.fieldname)
			else:
				raise NotEnoughDataInYear("Not enough data in year %s" % (self.year))
		
		return locations_with_data
	
	def _mask_locations(self, locations, not_locations, locations_with_data):
		"""
		locations was externally sorted, so we need to maintain its order.
		We also need to remove any entry in not_locations from locations.
		"""
		self.column_order = list(locations) # make a copy
		delete_these = []
		for (index, location) in enumerate(self.column_order):
			if location in not_locations:
				delete_these.append(index)
			elif location not in locations_with_data:
				delete_these.append(index)
			
		for index in sorted(delete_these, reverse=True):
			self.column_order.pop(index)
		
		# mutate self.is_data_present if not_locations is not None
		for location in not_locations:
			for year in self.is_data_present:
				for variety in self.is_data_present[year]:
					if location in self.is_data_present[year][variety]:
						self.is_data_present[year][variety][location] = False
	
	def _make_appendix(self):
		table = Appendix_Table()
		location = Fake_Location("empty")
		# do not add this location to self.column_order, we want it to be invisible
		for variety in models.Variety.objects.all():
			if variety not in self.cells:
				table.append(Empty_Cell(variety, location))		
		## TODO: for variety in self.dropped_tables: table.append(Empty_Cell(variety, location))
		self.append(table)
	
	def _find_exemplar_variety(self, table, year_range):
		best_score = 0
		for variety in [row.variety for row in table]:
			score = 0
			for years_diff in range(year_range):
				year = self.year - years_diff
				try:
					locations = filter(None, self.is_data_present[year][variety])
				except KeyError:
					locations = []
				score += len(locations)
			if score > best_score:
				exemplar_variety = variety
				best_score = score
		return exemplar_variety
	
	def _add_aggregate_and_lsd_cells(self, year_range, lsd_probability):
		# create fake varieties, locations
		variety = Fake_Variety("LSD")
		self.row_order.append(variety) # displays at end of table
		fake_locations = []
		for years_back in sorted(range(year_range), reverse=True): 
			location = Fake_Location("%s-yr" % (years_back + 1)) # start counting from 1, not 0
			self.column_order.insert(0, location) # prepend to list
			fake_locations.insert(0, (years_back, location)) # reverse the order again
			
		for table in self:
			## Add LSD rows
			for location in self.column_order:
				clone_me = None
				for cell in table.column(location): # assumes this isn't an Aggregate_Column
					if cell is not None:
						clone_me = cell
						break
				cell = LSD_Cell(variety, location, self.year, self.fieldname, clone_me)
				table.append(cell)
			## Add n-yr columns
			years_back_sum = 0
			exemplar_variety = self._find_exemplar_variety(table, year_range)
			for (years_back, location) in fake_locations:
				for row in table.rows():
					if not isinstance(row.variety, Fake_Variety):
						cell = Aggregate_Cell(row.variety, location, self.year, self.fieldname)
						cell.table = table
						table.append(cell)
					else:
						cell = LSD_Aggregate_Cell(row.variety, location, self.year, self.fieldname, lsd_probability)
						cell.table = table
						table.append(cell)
				column = table.column(location)
				column.years_back = years_back
				for years_diff in range(years_back + 1):
					year = self.year - years_diff
					try:
						locations = [location for location in self.is_data_present[year][exemplar_variety] if self.is_data_present[year][exemplar_variety][location]]
					except KeyError:
						locations = []
					column.balanced_criteria[year] = locations
				try:
					site_years = table.site_years[years_back] # here, we use years_back as an index
				except IndexError:
					site_years = 0
				years_back_sum += site_years
				column.site_years = years_back_sum
	
	def _copy_rows_to_remaining_tables(self):
		try:
			prev_table = self._tables[0]
		except IndexError:
			return
			
		for table in self._tables[1:]: # skip first table
			# populate masked_locations, so we can fill in some Empty_Cells
			for row in table:
				first_row = row
				try:
					is_data_present = self.is_data_present[self.year][first_row.variety]
					masked_locations = filter(
						lambda location: not is_data_present[location],
						is_data_present
					)
				except KeyError:
					masked_locations = []
				break
			
			for row in prev_table:
				# continue if a decorative element
				if isinstance(row.variety, Fake_Variety):
					continue
				for cell in row:
					if cell.location in masked_locations:
						cell = Empty_Cell(cell.variety, cell.location)
					elif isinstance(cell, Aggregate_Cell):
						cell = Aggregate_Cell(cell.variety, cell.location, cell.year, cell.fieldname)
						cell.table = table
					table.append(cell)

	def _init_table(self, table, variety=None, year_range=0):
		self.append(table)
		# populate site_years
		site_years = []
		if variety:
			for years_back in range(year_range):
				try:
					site_year = len(filter(None, self.is_data_present[self.year - years_back][variety].values()))
				except KeyError:
					site_year = 0
				site_years.append(site_year)
		table.site_years = tuple(site_years)
		return table

	def __init__(self, locations, number_locations, not_locations, 
			default_year, year_range, default_fieldname, lsd_probability, 
			break_into_subtables=False, varieties=[], show_appendix_tables=False,
			number_of_tables=3, all_varieties_in_subtables=True):
		self._tables = []
		self.cells = {}
		self.clear()
		self.year = default_year
		self.fieldname = default_fieldname
		
		# populate self.cells and self.is_data_present
		locations_with_data = self._process_entries(year_range, locations, number_locations, varieties)
		
		# populate self.row_order
		self.row_order = sorted(list(self.cells.keys()), key=lambda variety: variety.name) # sorted alphanumeric
		
		# populate self.column_order, maybe mutate self.is_data_present
		self._mask_locations(locations, not_locations, locations_with_data) # sorted by distance
		
		# Make tables from self.cells
		if break_into_subtables:
			# Sort/split the tables
			
			# Sort the varieties by number of locations they appear in.
			variety_order = sorted(self.is_data_present[self.year], key = lambda variety: self.is_data_present[self.year][variety], reverse=True)
			
			if not variety_order: # i.e. is an empty list
				break_into_subtables = False
			else:
				prev = variety_order[0]
				
				# Move balanced varieties to their own tables
				table = self._init_table(Table(), prev, year_range)
				for variety in variety_order:
					# if this variety is the first of the next group in our sorted list
					if self.is_data_present[self.year][variety] != self.is_data_present[self.year][prev]:
						prev = variety
						table = self._init_table(Table(), variety, year_range)

					for location in self.cells[variety]:
						cell = self.cells[variety][location]
						table.append(cell)
		
		if not break_into_subtables:
			table = self._init_table(Table())
			for variety in self.cells:
				for location in self.cells[variety]:
					cell = self.cells[variety][location]
					table.append(cell)
		
		# Decorate the tables
		self._add_aggregate_and_lsd_cells(year_range, lsd_probability)
					
		# sort descending by site-years tuple, i.e. [(8, 12, 16), ...]
		self._tables = sorted(self._tables, key=lambda (table): table.site_years, reverse=True)
		
		# remove extra tables
		# TODO: recover the tables and combine them into an appendix table
		self._tables = self._tables[0:number_of_tables]
		
		if show_appendix_tables:
			self._make_appendix()
		
		# add data from higher-order tables to lower-order ones (ordering is by site-years)
		if all_varieties_in_subtables:
			self._copy_rows_to_remaining_tables()
	
	def __unicode__(self):
		header = u'%s\t\t\t%s' % (unicode(self.year), u' '.join([unicode(location.name).replace(u' ', u'_') for location in self.column_order]))
		page = [header]
		page.extend([unicode(table) for table in self])
		return unicode("\n\n").join(page)
	
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
		while True:
			try:
				table = self._tables[index]
				index += 1
			except IndexError:
				raise StopIteration
			yield table
	
	def append(self, table):
		table.page = self
		self._tables.append(table)
		
	def extend(self, tables):
		for table in tables:
			self.append(table)
	
	def tables():
		return self
	
	def set_defaults(self, year, fieldname):
		for variety in self.cells:
			for cell in self.cells[variety].values():
				cell.set_defaults(year, fieldname)
			
	def clear(self):
		for table in self._tables:
			table.clear()
		self._tables = []
		for cell in [self.cells[variety][location] for variety in self.cells for location in self.cells[variety]]:
			cell.clear()
		self.year = 0
		self.fieldname = "no_field"
		self.cells = {} # variety: {location: Cell() }
		self.is_data_present = {} # {year: {variety: {location: bool, ...}, ...}, ...}
		self.row_order = [] # [variety, ...]
		self.column_order = [] # [location, ...]
		
 
