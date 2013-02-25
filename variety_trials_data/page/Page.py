from variety_trials_data.models import Trial_Entry, Date
from variety_trials_data import models
from variety_trials_data.page import Table, Aggregate_Cell, Cell, Column, Row, LSD_Row
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
	def get_entries(self, min_year, max_year, locations, number_locations, variety_names):
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
	
	def __init__(self, locations, number_locations, not_locations, 
			default_year, year_range, default_fieldname, lsd_probability, 
			break_into_subtables=False, varieties=[], show_appendix_tables=False,
			number_of_tables=3, all_varieties_in_subtables=False):
		self.tables = []
		decomposition = self.decomposition = {}# {year: {variety: {location: bool, ...}, ...}, ...}
		self.clear()
		cells = {} # variety: {location: Cell() }
		(locations, entries) = self.get_entries(
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
				cell = cells[variety][location]
			except KeyError:
				try:
					d = cells[variety]
				except KeyError:
					d = cells[variety] = {}
				cell = d[location] = Cell(default_year, default_fieldname)
					
			cell.append(entry)
			
			try:
				d = decomposition[year][variety]
			except KeyError:
				try:
					d = decomposition[year][variety] = dict([(l, False) for l in locations])
				except KeyError:
					decomposition[year] = {}
					d = decomposition[year][variety] = dict([(l, False) for l in locations])
					
			try:
				d[location] = True
			except KeyError:
				pass
		
		if default_year not in decomposition:
			years = decomposition.keys()
			if len(years) > 0:
				default_year = sorted(years, reverse=True)[0]
			else:
				raise NotEnoughDataInYear("Not enough data in year %s" % (default_year))
		
		# hide user's deselections.
		visible_locations = list(locations) # make a copy
		
		if len(not_locations) > 0:
			delete_these = []
			for (index, location) in enumerate(visible_locations):
				if location in not_locations:
					delete_these.append(index)
					
			for index in sorted(delete_these, reverse=True):
				visible_locations.pop(index)
		
		#
		## Make tables from cells
		#
		if break_into_subtables:
			# Sort/split the tables
			
			# Sort the varieties by number of locations they appear in.
			variety_order = sorted(decomposition[default_year], key = lambda variety: decomposition[default_year][variety], reverse=True)
			
			if len(variety_order) < 1:
				break_into_subtables = False
			else:
				prev = variety_order[0]
				
				# Move balanced varieties to their own tables
				table = Table(locations, visible_locations, lsd_probability, default_year, default_year - year_range, default_fieldname)
				self.data_tables.append(table)
				for variety in variety_order:
					if not isinstance(table, Appendix_Table) and decomposition[default_year][variety] != decomposition[default_year][prev]:
						prev = variety
						if len([location for location in decomposition[default_year][prev] if decomposition[default_year][prev][location]]) >= len(visible_locations) / 2:
							table = Table(locations, visible_locations, lsd_probability, default_year, default_year - year_range, default_fieldname)
							self.data_tables.append(table)
						else:
							table = Appendix_Table(locations, visible_locations, lsd_probability, default_year, default_year - year_range, default_fieldname)
							self.appendix_tables.append(table)
					
					for (location, cell) in cells[variety].items():
						table.add_cell(variety, location, cell)
		
		if not break_into_subtables:
			table = Table(locations, visible_locations, lsd_probability, default_year, default_year - year_range, default_fieldname)
			self.data_tables.append(table)
			for variety in cells:
				for location in cells[variety]:
					cell = cells[variety][location]
					table.add_cell(variety, location, cell)
		
		# {Add,add to} appendix tables
		if len(self.appendix_tables) > 0:
			table = self.appendix_tables[-1] # grab the last one
		else:
			table = Appendix_Table(locations, visible_locations, lsd_probability, default_year, default_year - year_range, default_fieldname)
			self.appendix_tables.append(table)
		
		for variety in models.Variety.objects.all():
			if variety not in cells:
				table.add_cell(variety)
		
		for extra_table in self.extra_tables:
			for variety in extra_table.rows.keys():
				table.add_cell(variety)

		self.tables.extend(self.data_tables)
		self.tables.extend(self.appendix_tables) # why do we do this?
		
		# Decorate the tables
		for table in self.tables:
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
					cell = Aggregate_Cell(default_year, default_fieldname, row, column, decomposition, table.visible_locations)
					table.add_cell(row.variety, location_key, cell)
					
		# sort descending by site-years tuple, i.e. [(8, 12, 16), ...]
		self.data_tables = sorted(self.data_tables, key=lambda (table): table.get_site_years(), reverse=True)
		# truncate number of tables
		self.extra_tables = self.data_tables[number_of_tables:]
		self.data_tables = self.data_tables[:number_of_tables]
		
		# add data from higher-order tables to lower-order ones (ordering is by site-years)
		if all_varieties_in_subtables:
			prev_table = None
			for table in self.data_tables:
				if prev_table is None:
					prev_table = table
					continue
				for ((variety, location), cell) in prev_table.cells.items():
					# continue if a decorative element
					if isinstance(location, Fake_Location) or isinstance(variety, Fake_Variety):
						continue
					# if we have no data, insert a blank cell
					try:
						column = table.columns[location]
						c = column.members[0]
					except (KeyError, IndexError) as error:
						c = None
					if c is None or c.get(default_year, default_fieldname) is None:
						table.add_cell(variety, location, Cell(default_year, default_fieldname))
					else:
						table.add_cell(variety, location, cell)
		
	def set_defaults(self, year, fieldname):
		for table in self.tables:
			table.set_defaults(year, fieldname)
			
	def clear(self):
		for table in self.tables:
			table.clear()
		self.tables = []	
		self.data_tables = []	
		self.extra_tables = []	
		self.appendix_tables = []	
		for year in self.decomposition:
			for variety in self.decomposition[year]:
				self.decomposition[year][variety] = {}
			self.decomposition[year] = {}
		self.decomposition = {} # {year: {variety: {location: bool, ...}, ...}, ...}

