from variety_trials_data.models import Trial_Entry, Date
from variety_trials_data import models
from variety_trials_data.variety_trials_util import LSDProbabilityOutOfRange, TooFewDegreesOfFreedom, NotEnoughDataInYear
from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv
from itertools import chain, cycle
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
		self.year = 0
		self.fieldname = "no_field"
	
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
			mean = float(sum(values)) / float(len(values))
		
		return mean
	
	def get_rounded(self, year, fieldname, digits=1):
		value = self.get(year, fieldname)
		if value is not None:
			value = round(value, digits)
		return value
	
	def __unicode__(self):
		unicode_repr = self.get_rounded(self.year, self.fieldname)
		if unicode_repr is None:
			unicode_repr = u'--'
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
			cell = None

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
			lsd = self.get_lsd(cell)
			return lsd
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
	
	def get_lsd(self, cell, digits=1):
	
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
				raise LSDProbabilityOutOfRange("Alpha-value out of range: '%s'" % (P))
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
			if n < 1:
				raise TooFewDegreesOfFreedom("Not enough degrees of freedom: '%s' to calculate LSD." % (n))
			elif P > 1.0 or P <= 0.0:
				raise LSDProbabilityOutOfRange("Alpha-value out of range: '%s'" % (P))
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
		
		cur_year = cell.year
		balanced_cells = {} # {year: [[], ...] } # n by m cell matrix
		for year_diff in cell.column.years_range:
			year = cur_year - year_diff
			balanced_cells[year] = []
			cells_append = balanced_cells[year].append
			for (variety, row) in self.table.sorted_rows():
				if not isinstance(row, LSD_Row): # prevent infinite recursion!
					balanced_cells_row = []
					row_append = balanced_cells_row.append
					for row_cell in row:
						if row_cell is not None and not isinstance(row_cell.column, Aggregate_Column):
							row_append(row_cell.get_rounded(year, row_cell.fieldname, digits=5))
					cells_append(balanced_cells_row)
		"""
		for table in balanced_cells:
			for row in balanced_cells[table]:
				print row
			print "==="
		#"""
		
		#
		## delete rows that are all None
		#
		delete_rows = [] # indexes of rows to delete
		for year in balanced_cells:
			for (r, row) in enumerate(balanced_cells[year]):
				delete_row = True
				for cell in row:
					if cell is not None:
						delete_row = False
						break
				if delete_row:
					delete_rows.append(r)
					
		for index in sorted(list(set(delete_rows)), reverse=True):
			for year in balanced_cells:
				balanced_cells[year].pop(index)
		#
		## delete columns that are all None		
		#
		delete_columns = [] # indexes of columns to delete
		for year in balanced_cells:
			column_length = len(balanced_cells[year])
			delete_column = {} # was `[0] * len(row)' but len(row) != num_columns...?
			for row in balanced_cells[year]: 
				for (c, cell) in enumerate(row):
					if cell is None:
						try:
							delete_column[c] += 1
						except KeyError:
							delete_column[c] = 1
			for index in delete_column:
				if delete_column[index] == column_length:
					delete_columns.append(index)
					
		for index in sorted(list(set(delete_columns)), reverse=True):
			for year in balanced_cells:
				for row in balanced_cells[year]:
					row.pop(index)
		#
		## delete rows with impudence until balanced
		#
		delete_rows = [] # indexes of rows to delete
		for year in balanced_cells:
			for (r, row) in enumerate(balanced_cells[year]):
				delete_row = False
				for cell in row:
					if cell is None:
						delete_row = True
						break
						
				if delete_row:
					delete_rows.append(r)
					
		for index in sorted(list(set(delete_rows)), reverse=True):
			for year in balanced_cells:
				balanced_cells[year].pop(index)
		
		"""
		for table in balanced_cells:
			for row in balanced_cells[table]:
				print row
			print "==="
		#"""
		
		balanced_input = []
		for year in balanced_cells:
			balanced_input.extend(balanced_cells[year])
			
		#print balanced_input
		
		lsd = None
		if len(balanced_input) > 1 and len(balanced_input[0]) > 1:
			try:
				lsd = _LSD(balanced_input, self.table.lsd_probability)
				lsd = round(lsd, digits)
			except (LSDProbabilityOutOfRange, TooFewDegreesOfFreedom):
				lsd = None
			except:
				lsd = None
		
		return lsd

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
		self.index = 0

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
			cell = None
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
	
	def clear(self):
		Cell.clear(self)
		self.decomposition = {}
		self.visible_locations = []
		self.site_years = 0

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
		
	def get_site_years(self):
		return self.site_years
		
	def clear(self):
		Column.clear(self)
		self.site_years = None
		self.years_range = []

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
			self.cells = {} # (variety, location): Cell()
			self.rows = {} # variety: Row(), ...
			self.columns = {} # location: Column(), ...
		
		def clear(self):
			self.locations = []
			self.visible_locations = []
			for cell in self.cells.values():
				cell.clear()
			for row in self.rows.values():
				row.clear()
			for column in self.columns.values():
				column.clear()
			self.cells = {}
			self.rows = {}
			self.columns = {}
		
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
				if isinstance(column, Aggregate_Column) and column.site_years == None:
					for cell in column:
						if cell.site_years > column.site_years:
							column.site_years = cell.site_years
							
				sorted_column_tuples.append( (column, location) )
				
			return sorted_column_tuples
			
		def set_defaults(self, year, fieldname):
			for cell in self.cells.values():
				cell.year = year
				cell.fieldname = fieldname
				
		def mask_locations(self, not_locations):
			"""
			Mask not_locations from this table. This function will unmask any
			locations _not_ found in not_locations, as well.
			
			not_locations: the locations to mask/hide
			"""
			#
			# Note: we cannot reassign self.visible_locations, all of our
			# rows our pointing to its reference.
			#
			locations = list(self.locations)
			
			delete_these = []
			for (index, location) in enumerate(locations):
				if location in not_locations:
					delete_these.append(index)
					
			for index in sorted(delete_these, reverse=True):
				locations.pop(index)
			
			# mutate table.visible_locations by removing locations to be masked
			delete_these = []
			for (index, location) in enumerate(self.visible_locations):
				if location not in locations:
					delete_these.append(index)
					
			for index in sorted(delete_these, reverse=True):
				self.visible_locations.pop(index)
			
			# insert into table.visible_locations locations that have been unmasked
			insert_these = []
			for (index, location) in enumerate(locations):
				if location not in self.visible_locations:
					insert_these.append(index)
					
			for index in insert_these:
				self.visible_locations.insert(index, locations[index])
			
			for column in self.columns.values():
				if isinstance(column, Aggregate_Column):
					for cell in column:
						if isinstance(cell, Aggregate_Cell):
							cell.calculate_site_years()
					column.site_years = None # force recalculation

class Appendix_Table(Table):
	def __init__(self, locations, visible_locations, lsd_probability):
		"""
		location: a Location (or Fake_Location) object
		year_num: an integer denoting the number of years to go back for averaging i.e. 3
		"""
		Table.__init__(self, locations, visible_locations, lsd_probability)
	
	def add_cell(self, variety, location=None, cell=None):
		row = self.get_row(variety)
		row.set_key_order(None)
	
	def sorted_visible_columns(self):
		return []

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
	
	def __init__(self, locations, number_locations, not_locations, default_year, year_range, default_fieldname, lsd_probability, break_into_subtables=False, varieties=[]):
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
				table = Table(locations, visible_locations, lsd_probability)
				self.data_tables.append(table)
				for variety in variety_order:
					if not isinstance(table, Appendix_Table) and decomposition[default_year][variety] != decomposition[default_year][prev]:
						prev = variety
						if len([location for location in decomposition[default_year][prev] if decomposition[default_year][prev][location]]) >= len(visible_locations) / 2:
							table = Table(locations, visible_locations, lsd_probability)
							self.data_tables.append(table)
						else:
							table = Appendix_Table(locations, visible_locations, lsd_probability)
							self.appendix_tables.append(table)
					
					for (location, cell) in cells[variety].items():
						table.add_cell(variety, location, cell)
		
		if not break_into_subtables:
			table = Table(locations, visible_locations, lsd_probability)
			self.data_tables.append(table)
			for variety in cells:
				for location in cells[variety]:
					cell = cells[variety][location]
					table.add_cell(variety, location, cell)
			
		
		# {Add,add to} appendix tables
		if len(self.appendix_tables) > 0:
			table = self.appendix_tables[-1] # grab the last one
		else:
			table = Appendix_Table(locations, visible_locations, lsd_probability)
			self.appendix_tables.append(table)
			
		for variety in models.Variety.objects.all():
			if variety not in cells:
				table.add_cell(variety)
		
		self.tables.extend(self.data_tables)
		self.tables.extend(self.appendix_tables)
		
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
			
	def clear(self):
		for table in self.tables:
			table.clear()
		self.tables = []	
		self.data_tables = []	
		self.appendix_tables = []	
		for year in self.decomposition:
			for variety in self.decomposition[year]:
				self.decomposition[year][variety] = {}
			self.decomposition[year] = {}
		self.decomposition = {} # {year: {variety: {location: bool, ...}, ...}, ...}

