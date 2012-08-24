from variety_trials_data.models import Trial_Entry, Date
from variety_trials_data import models
from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv
from itertools import chain
from operator import attrgetter
import copy
import datetime

class Cell:
	"""
	Helper class; Cells for our Table class.
	"""
	
	def __init__(self, year, fieldname):
		self.clear()
		self.year = year
		self.fieldname = fieldname
		
	def __iter__(self):
		self.index = 0
		return self
	
	def next(self):
		if self.index == len(self.members):
			raise StopIteration
		value = self.members[self.index]
		self.index = self.index + 1
		return value 
	
	def append(self, value):
		self.members.append(value)
	
	def delete_row(self):
		self.row = None
	
	def delete_column(self):
		self.column = None
	
	def clear(self):
		self.delete_row()
		self.delete_column()
		self.members = []
		self.index = 0
	
	def get(self, year, fieldname):
		this_year = []
		for entry in self.members:
			if entry.harvest_date.date.year == year:
				this_year.append(entry)
		#print this_year
		
		values = []
		for entry in this_year:
			try:
				value = getattr(entry, fieldname)
			except AttributeError:
				value = None
			if value is not None:
				values.append(value)

		mean = None
		if len(values) > 0:
			mean = round(float(sum(values)) / float(len(values)), 1)
		
		return mean
		
	def __unicode__(self):
		unicode_repr = self.get(self.year, self.fieldname)
		if unicode_repr is None:
			unicode_repr = u'-!-'
		else:
			unicode_repr = unicode(str(unicode_repr))
		return unicode_repr
		
class Row:
	"""
	Contains references to each Cell in this row.
	"""
	def __init__(self, variety):
		self.variety = variety
		self.members = {}
		self.clear()
	
	def __iter__(self):
		if self.key_order is None:
			self.keys = self.members.keys()
		else:
			self.keys = self.key_order
		self.key_index = 0
		return self
		
	def next(self):
		if self.key_index == len(self.keys):
			raise StopIteration
			
		try:
			key = self.keys[self.key_index]
		except IndexError:
			raise StopIteration
		
		try:
			cell = self.members[key]
		except KeyError:
			self.key_index = self.key_index + 1
			return None

		self.key_index = self.key_index + 1
		return cell
	
	def append(self, value):
		try:
			self.members[value.column.location] = value
		except AttributeError:
			col = self.members[None] = value
		
	def set_key_order(self, key_order):
		self.key_order = key_order

	def clear(self):
		for m in self.members:
			if isinstance(m, Cell):
				m.delete_row()
		self.members = {}
		self.key_order = None
		self.keys = None
		self.key_index = 0
		self.value_index = 0

class Fake_Variety:
	def __init__(self, name):
		self.name = name
		self.id = -1
		self.pk = -1

class LSD_Row(Row):
	"""
	A row that keeps track of which Table it belongs to.
	"""
	def __init__(self, variety, table):
		Row.__init__(self, variety)
		self.table = table
	
	def __iter__(self):
		self.key_order = self.table.visible_locations
		return Row.__iter__(self)
		
	def next(self):
		cell = Row.next(self)
		if isinstance(cell, Aggregate_Cell):
			cell_lsd_input = {} # {year: [[], ...] } # n by m cell matrix
			cell_lsd_input['2010'] = []
			for (variety, row) in self.table.sorted_rows():
				if not isinstance(row, LSD_Row): # prevent infinite recursion!
					row_lsd_input = []
					for cell in row:
						if cell is not None and not isinstance(cell.column, Aggregate_Column):
							row_lsd_input.append(unicode(cell))
					cell_lsd_input['2010'].append(row_lsd_input)
			for row in cell_lsd_input['2010']:
				print row
			print "==="
			return "M-LSD"
		elif isinstance(cell, Cell):
			## Grab a real cell from the column
			for real_cell in cell.column:
				if real_cell is not None:
					break
			lsd = None
			if real_cell is not None:		
				# intentionally use cell.year instead of real_cell.year
				lsd = real_cell.get(cell.year, "hsd_10") # TODO: this will try and average if multiple values datapoints found...
				if lsd is None:
					lsd = real_cell.get(cell.year, "lsd_10")
				if lsd is None:
					lsd = real_cell.get(cell, "lsd_05")
			return lsd
		else:
			return cell
	
	def populate(self, probability):
	
		def _qnorm(probability):
			"""
			A reimplementation of R's qnorm() function.
			
			This function calculates the quantile function of the normal
			distributition.
			(http://en.wikipedia.org/wiki/Normal_distribution#Quantile_function)
			
			Required is the erfinv() function, the inverse error function.
			(http://en.wikipedia.org/wiki/Error_function#Inverse_function)
			"""
			if probability > 1 or probability <= 0:
				raise BaseException # TODO: raise a standard/helpful error
			else:
				return sqrt(2) * erfinv(2*probability - 1)
				
		def _qt(probability, degrees_of_freedom):
			"""
			A reimplementation of R's qt() function.
			
			This function calculates the quantile function of the student's t
			distribution.
			(http://en.wikipedia.org/wiki/Quantile_function#The_Student.27s_t-distribution)
			
			This algorithm has been taken (line-by-line) from Hill, G. W. (1970)
			Algorithm 396: Student's t-quantiles. Communications of the ACM, 
			13(10), 619-620.
			
			Currently unimplemented are the improvements to Algorithm 396 from
			Hill, G. W. (1981) Remark on Algorithm 396, ACM Transactions on 
			Mathematical Software, 7, 250-1.
			"""
			n = degrees_of_freedom
			P = probability
			t = 0
			if (n < 1 or P > 1.0 or P <= 0.0 ):
				raise BaseException #TODO: raise a standard/helpful error
			elif (n == 2):
				t = sqrt(2.0/(P*(2.0-P)) - 2.0)
			elif (n == 1):
				P = P * pi/2
				t = cos(P)/sin(P)
			else:
				a = 1.0/(n-0.5)
				b = 48.0/(a**2.0)
				c = ((20700.0*a/b - 98.0)*a - 16.0)*a + 96.36
				d = ((94.5/(b+c) - 3.0)/b + 1.0)*sqrt(a*pi/2.0)*float(n)
				x = d*P
				y = x**(2.0/float(n))
			
				if (y > 0.05 + a):
					x = _qnorm(P*0.5)
					y = x**2.0
					
					if (n < 5):
						c = c + 0.3*(float(n)-4.5)*(x+0.6)

					c = (((0.05*d*x-5.0)*x-7.0)*x-2.0)*x+b+c
					y = (((((0.4*y+6.3)*y+36.0)*y+94.5)/c-y-3.0)/b+1.0)*x
					y = a*y**2.0
					
					if (y > 0.002):
						y = exp(y) - 1.0
					else:
						y = 0.5*y**2.0 + y

				else:
					y = ((1.0/(((float(n)+6.0)/(float(n)*y)-0.089*d-0.822)*(float(n)+2.0)*3.0)+0.5/(float(n)+4.0))*y-1.0)*(float(n)+1.0)/(float(n)+2.0)+1.0/y
				
				t = sqrt(float(n)*y)
			
			return t
		
		def _LSD(response_to_treatments, probability):
			"""
			A stripped-down reimplementation of LSD.test from the agricoloae
			package. (http://cran.r-project.org/web/packages/agricolae/index.html)
			
			Calculates the Least Significant Difference of a multiple comparisons
			trial, over a balanced dataset.
			"""
			
			trt = response_to_treatments
			#model = aov(y~trt)
			#df = df.residual(model)
			# df is the residual Degrees of Freedom
			# n are factors, k is responses per factor
			n = len(trt)
			k = len(trt[0]) # == len(trt[1]) == ... == len(trt[n])
			degrees_freedom_of_error = (n-1)*(k-1)
			
			treatment_means = {}
			for i in range(n): # n == len(trt)
				total = 0.0
				for j in range(k):
					total += float(trt[i][j])
				treatment_means[i] = total/k
				
			block_means = {}
			for j in range(k):
				total = 0.0
				for i in range(n):
					total += float(trt[i][j])
				block_means[j] = total/n
			
			grand_mean = sum(treatment_means.values()) / float(n)
			
			# SSE is the Error Sum of Squares
			# TODO: what is the difference between type I and type III SS? (http://www.statmethods.net/stats/anova.html)
			SSE = 0.0
			for i in range(n): # n == len(trt)
				for j in range(k):
					SSE += (float(trt[i][j]) - treatment_means[i] - block_means[j] + grand_mean)**2.0
			
			mean_squares_of_error = SSE / degrees_freedom_of_error
			
			Tprob = _qt(probability, degrees_freedom_of_error)
				
			LSD = Tprob * sqrt(2.0 * mean_squares_of_error / k)

			return LSD
		
		y_columns = self.table.year_columns
		years_i = []
		l_columns = self.table.location_columns
		location_lsds = []
		
		years_i = list(y_columns[0].keys())
		
		if len(years_i) == 3:
			data_1yr = years_i[0]
			data_2yr = years_i[1]
			data_3yr = years_i[2]
		elif len(years_i) == 2:
			data_1yr = years_i[0]
			data_2yr = years_i[1]
		elif len(years_i) == 1:
			data_1yr = years_i[0]
		else:
			pass
		
		"""
		if data_1yr != None:	
			lsd_1yr = self._LSD(data_1yr, probability)
		if data_2yr != None:
			lsd_2yr = self._LSD(data_2yr, probability)
		if data_3yr != None:
			lsd_3yr = self._LSD(data_3yr, probability)
		"""	
		lsd_1yr = 0.1
		lsd_2yr = 0.2
		lsd_3yr = 0.3
		"""
		Grab the LSDs for the location columns in the Table object. 
		Search the entries of table in this order: hsd_10, lsd_05, lsd_10.
		"""	
		for entry in self.table.entries:
			for l in l_columns[0].keys():
				if entry.hsd_10 is not None and l.name == entry.location.name:
					location_lsds.append(entry.hsd_10)
				elif entry.lsd_05 is not None and l.name == entry.location.name:
					location_lsds.append(entry.lsd_05)
				elif entry.lsd_10 is not None and l.name == entry.location.name:
					location_lsds.append(entry.lsd_10)
				else:
					location_lsds.append(None)	
				
		lsds = ['LSD', lsd_1yr, lsd_2yr, lsd_3yr]
		
		for l in location_lsds:
			lsds = l
		
		return lsds

	def clear(self):
		Row.clear(self)
		self.table = None

class Column:
	"""
	Contains references to each Cell in this column.
	"""
	def __init__(self, location):
		self.location = location
		self.members = []
		self.index = 0
	
	def __iter__(self):
		self.index = 0
		return self
	
	def next(self):
		if self.index == len(self.members):
			raise StopIteration
		cell = self.members[self.index]
		self.index = self.index + 1
		return cell
	
	def append(self, value):
		self.members.append(value)
		
	def clear(self):
		for m in self.members:
			if isinstance(m, Cell):
				m.delete_column()
		self.members = []

class Aggregate_Cell(Cell):
	"""
	A cell whose value is based upon its row
	"""
	def __init__(self, year, fieldname, row, column, decomposition, visible_locations):
		"""
		year: passed on to Cell
		fieldname: passed on to Cell
		row: the row this aggregate_cell is in
		column: the column this aggregate_cell is in
		decomposition: a truth table of what data we have
		"""
		Cell.__init__(self, year, fieldname)
		self.row = row
		self.column = column
		# Note we are not making a copy of decomposition; do not mutate
		self.decomposition = decomposition # {year: {variety: {location: bool, ...}, ...}, ...}
		# Note we are not making a copy of visible_locations; do not mutate
		self.visible_locations = visible_locations
		self.calculate_site_years()
		
	def calculate_site_years(self):
		self.site_years = 0
		if not isinstance(self.row, LSD_Row):
			for cell in self.row:
				if cell is not None and not isinstance(cell, Aggregate_Cell):
					break
			if cell is not None and not isinstance(cell, Aggregate_Cell):
				for year_diff in self.column.years_range:
					year = self.year - year_diff
					min_site_years = 10000
					if year in self.decomposition:
						for col_cell in cell.row:
							if col_cell is not None:
								variety = col_cell.row.variety
								if variety in self.decomposition[year]:
									truth_table = self.decomposition[year][variety]
									site_years = len([location for location in self.visible_locations if not isinstance(location, Fake_Location) and truth_table[location]])
									if site_years < min_site_years:
										min_site_years = site_years
					if min_site_years == 10000:
						min_site_years = 0
					self.site_years = self.site_years + min_site_years
	
	def append(self, value):
		return
	
	def get(self, year, fieldname):
		balanced = True
		values = []
		if not isinstance(self.row, LSD_Row):
			for cell in self.row:
				if balanced and cell is not None and not isinstance(cell, Aggregate_Cell):
					for year_diff in self.column.years_range:
						cell_mean = cell.get(year - year_diff, fieldname)
						if cell_mean is None:
							# This subset is not balanced across years!
							pass # we will count the number of means found later
						else:
							values.append(cell_mean)
						
		
		mean = None
		if len(values) > 0 and len(values) >= self.column.site_years:
			mean = round(float(sum(values)) / float(len(values)), 1)
		
		return mean

class Fake_Location:
	def __init__(self, name):
		self.name = name
		self.id = -1
		self.pk = -1

class Aggregate_Column(Column):
	"""
	A column whose cells' value is determined by other cells in its row
	"""
	def __init__(self, location, year_num):
		"""
		location: a Location (or Fake_Location) object
		year_num: an integer denoting the number of years to go back for averaging i.e. 3
		"""
		Column.__init__(self, location)
		self.members = []
		self.clear()
		self.years_range = range(year_num)
		self.site_years = 0
	
	def get_site_years(self):
		return self.site_years

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
			
		def __init__(self, locations, visible_locations, lsd_probability): # Probability is required for creating the LSD row
			self.lsd_probability = lsd_probability
			self.locations = list(locations) # create a copy
			self.visible_locations = list(visible_locations) # create a copy
			self.rows = {} # variety: Row(), ...
			self.columns = {} # location: Column(), ...
			self.cells = {} # (variety, location): Cell()
			
		def get_row(self, variety):
			try:
				row = self.rows[variety]
			except KeyError:
				row = self.rows[variety] = Row(variety)
				row.set_key_order(self.visible_locations) # pass by reference
			return row	
		
		def get_column(self, location):
			try:
				col = self.columns[location]	
			except KeyError:
				col = self.columns[location] = Column(location)
			return col
			
		def add_cell(self, variety, location, cell):
			row = self.get_row(variety)
			column = self.get_column(location)
			cell.row = row
			cell.column = column
			row.append(cell)
			column.append(cell)
			self.cells[(variety, location)] = cell
		
		def sorted_rows(self):
			alpha_sorted = sorted(self.rows.items(), key=lambda (variety, row): variety.name) # sort by variety.name
			
			## Move the LSD row to the end of the list
			lsd_row = None
			for variety in self.rows:
				if variety.name == "LSD":
					lsd_row = (variety, self.rows[variety])
					break
			if lsd_row is not None:
				alpha_sorted.remove(lsd_row) # remove it from its alphabetical position
				alpha_sorted.append(lsd_row) # append it to the end of the list
				
			return alpha_sorted
		
		def sorted_visible_columns(self):
			sorted_column_tuples = []
			for location in self.visible_locations:
				column = self.get_column(location)
				if isinstance(column, Aggregate_Column) and column.site_years == 0:
					for cell in column:
						if cell.site_years > column.site_years:
							column.site_years = cell.site_years
							
				sorted_column_tuples.append( (column, location) )
				
			return sorted_column_tuples
			
		def set_defaults(self, year, fieldname):
			for cell in self.cells.values():
				cell.year = year
				cell.fieldname = fieldname

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
			)
				
		if len(variety_names) > 0:
			result = result.filter(
					variety__in=models.Variety.objects.filter(
							name__in=variety_names
						)
				)
				
		return (locations_with_data, result)
	
	def mask_locations(self, not_locations, mutate_existing_tables=True):
		"""
		Returns the last list of locations that have had `not_locations'
		removed from them, or None if there was a problem. 
		`mutate_existing_tables' greatly changes the context of this return 
		value.
		
		not_locations: the locations to mask/hide
		mutate_exisiting_tables: whether or not to iterate over exisiting 
			tables, or to use self.locations
		"""
		def remove_locations(locations, not_locations):
			"""
			Remove `not_locations' from `locations', maintaining input order
			"""
			if len(not_locations) > 0:
				delete_these = []
				for (index, location) in enumerate(locations):
					if location in not_locations:
						delete_these.append(index)
						
				for index in sorted(delete_these, reverse=True):
					locations.pop(index)
			
			# TODO: if we rearrange `decomposition', the table layout will change as the 
			# TODO: user deselects locations. This will also need to be accounted for in
			# TODO: a remove_locations() function if we want to remove not_locations 
			# TODO: from the cache key.
			"""
			# adjust `decomposition' but not `cells' since we are 
			# modifying `visible_locations' but not `locations'
			remove_locations = list(set(locations).difference(set(visible_locations)))
			if len(remove_locations) > 0:
				for year in decomposition:
					decomposition_year = decomposition[year]
					for variety in decomposition_year:
						for location in remove_locations:
							if location in decomposition_year[variety]:
								del decomposition_year[variety][location]
			"""
			return locations
		
		visible_locations = None
		
		if mutate_existing_tables:	
			for table in self.tables:
				visible_locations = table.visible_locations = remove_locations(table.visible_locations, not_locations)
				
				for column in table.columns.values():
					if isinstance(column, Aggregate_Column):
						column.site_years = 0 # force recalculation
						for cell in column:
							if isinstance(cell, Aggregate_Cell):
								cell.calculate_site_years()
		else:
			visible_locations = remove_locations(list(self.locations), not_locations)
		
		return visible_locations
	
	def __init__(self, locations, number_locations, not_locations, default_year, year_range, default_fieldname, lsd_probability, break_into_subtables=False, varieties=[]):
		self.tables = []	
		cells = {} # variety: {location: Cell() }
		decomposition = self.decomposition = {} # {year: {variety: {location: bool, ...}, ...}, ...}
		(self.locations, entries) = self.get_entries(
				default_year - year_range, 
				default_year, 
				locations, 
				number_locations, 
				varieties
			)
				
		locations = self.locations # discard the input locations
		
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
					d = decomposition[year][variety] = dict([(l, False) for l in self.locations])
				except KeyError:
					decomposition[year] = {}
					d = decomposition[year][variety] = dict([(l, False) for l in self.locations])
							
			try:
				d[location] = True
			except KeyError:
				pass
		
		if default_year not in decomposition:
			years = decomposition.keys()
			if len(years) > 0:
				default_year = sorted(years, reverse=True)[0]
			else:
				raise BaseException() # TODO: custom exception so we can tell the user what's up
		
		# hide user's deselections.
		visible_locations = self.mask_locations(not_locations, mutate_existing_tables=False)
			
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
				table = Table(locations, visible_locations, lsd_probability)
				self.tables.append(table)
				for variety in variety_order:
					if decomposition[default_year][variety] != decomposition[default_year][prev]:
						prev = variety
						table = Table(locations, visible_locations, lsd_probability)
						self.tables.append(table)
					for (location, cell) in cells[variety].items():
						table.add_cell(variety, location, cell)
		
		if not break_into_subtables:
			table = Table(locations, visible_locations, lsd_probability)
			self.tables.append(table)
			for variety in cells:
				for location in cells[variety]:
					cell = cells[variety][location]
					table.add_cell(variety, location, cell)
			
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
				year_num = year_num + 1 # we want 1-indexed, not 0-indexed
				location_key = Fake_Location("%s-yr" % (year_num))
				table.locations.insert(0, location_key)
				table.visible_locations.insert(0, location_key)
				column = Aggregate_Column(location_key, year_num)
				table.columns[location_key] = column
				for row in table.rows.values():
					cell = Aggregate_Cell(default_year, default_fieldname, row, column, decomposition, table.visible_locations)
					table.add_cell(row.variety, location_key, cell)				
		
	def set_defaults(self, year, fieldname):
		for table in self.tables:
			table.set_defaults(year, fieldname)

