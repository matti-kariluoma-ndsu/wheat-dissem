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
		print this_year
		
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
		#return self.column.location.name
		
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
	def __init__(self, year, fieldname, row, column):
		Cell.__init__(self, year, fieldname)
		self.row = row
		self.column = column
		
	def append(self, value):
		return
	
	def get(self, year, fieldname):
		values = []
		for cell in self.row:
			if cell is not None and not isinstance(cell, Aggregate_Cell):
				for year_diff in self.column.years_range:
					cell_mean = cell.get(year - year_diff, fieldname)
					if cell_mean is None:
						pass # This subset is not balanced across years!
					else:
						values.append(cell_mean)
					
		
		mean = None
		if len(values) > 0:
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
			self.rows = {} # variety: [Row(), ...]
			self.columns = {} # location: [Column(), ...]
			self.cells = {} # (variety, location): Cell()
			
		def get_row(self, variety):
			try:
				row = self.rows[variety]
			except KeyError:
				row = self.rows[variety] = Row(variety)
				row.set_key_order(self.visible_locations)
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
			

class Page:
	def get_entries(self):
		# We do a depth=2 so we can access entry.variety.name
		# We do a depth=3 so we can access entry.harvest_date.date.year
		#TODO: Somehow reduce this to depth=1
		return models.Trial_Entry.objects.select_related(depth=3).filter(
				location__in=self.locations
			).filter(
				harvest_date__in=models.Date.objects.filter(
					date__range=(datetime.date(min(self.years),1,1), datetime.date(max(self.years),12,31))
				)
			)
			
	def __init__(self, locations, years, default_year, default_fieldname, lsd_probability, break_into_subtables=False):
		self.locations = locations
		self.years = years
		self.tables = []
		
		cells = {} # variety: {location: Cell() }
		decomposition = {} # {year: {variety: {location: bool, ...}, ...}, ...}
		for entry in self.get_entries():
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
				
		#print decomposition[default_year]
		
		visible_locations = list(locations) # copy list
		
		if break_into_subtables:
			# Sort/split the tables
			variety_order = sorted(decomposition[default_year], key = lambda variety: decomposition[default_year][variety], reverse=True)
			
			if len(variety_order) > 0:
				prev = variety_order[0]
				
				# delete locations that have no data in the current year
				truth_table = decomposition[default_year][prev]
				delete_these = []
				for (index, location) in enumerate(visible_locations):
					if not truth_table[location]:
						delete_these.append(index)
				for index in sorted(delete_these, reverse=True): # delete, starting from the back of the list
					visible_locations.pop(index)
				
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
			for year_num in sorted(range(len(self.years)), reverse=True):
				year_num = year_num + 1 # we want 1-indexed, not 0-indexed
				location_key = Fake_Location("%s-yr" % (year_num))
				table.locations.insert(0, location_key)
				table.visible_locations.insert(0, location_key)
				column = Aggregate_Column(location_key, year_num)
				table.columns[location_key] = column
				for row in table.rows.values():
					cell = Aggregate_Cell(default_year, default_fieldname, row, column)
					table.add_cell(row.variety, location_key, cell)
				
		
	def set_defaults(self, year, fieldname):
		for table in self.tables:
			table.set_defaults(year, fieldname)
			
	def set_default_year(self, year):
		for table in self.tables:
			table.set_default_year(year)
	
	def set_default_field(self, fieldname):
		for table in self.tables:
			table.set_default_field(fieldname)
			

