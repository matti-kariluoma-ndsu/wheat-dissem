from variety_trials_data.models import Trial_Entry #, Date
from variety_trials_data import models
from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv
from itertools import chain
from operator import attrgetter
import copy

class Row:
	"""
	Contains references to each Cell in this row.
	"""
	def __init__(self):
		self.members = list()
		self.index = 0
	
	def __iter__(self):
		self.index = 0
		return self
	
	def next(self):
		if self.index == len(self.members):
			raise StopIteration
		self.index = self.index + 1
		return self.members[self.index] 
	
	def append(self, value):
		self.members.append(value)
		self.index = self.index + 1
		
	def remove(self): # nulls the index and the member list
		self.members = []
		self.index = 0

class LSD_Row(Row):
	"""
	A row that keeps track of which Table it belongs to.
	"""
	def __init__(self, table):
		super(LSD_Row, self).__init__() # call Row.__init__()
		self.table = table
	
	def populate(self, probability):
		data_1yr = self.table.fetch(years=[0])
		data_2yr = self.table.fetch(years=[0,1])
		data_3yr = self.table.fetch(years=[0,1,2])
		lsd_1yr = self._LSD(data_1yr, probability)
		lsd_2yr = self._LSD(data_2yr, probability)
		lsd_3yr = self._LSD(data_3yr, probability)
		
		lsds = []
		for column in self.table.columns: # I might need to change this.
			lsds.append(column.lsd) 
		
		return ['LSD', lsd_1yr, lsd_2yr, lsd_3yr].extend(lsds)
	
	def _qnorm(self, probability):
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
			
	def _qt(self, probability, degrees_of_freedom):
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
				x = self._qnorm(P*0.5)
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
	
	def _LSD(self, response_to_treatments, probability):
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
		
		Tprob = self._qt(probability, degrees_freedom_of_error)
			
		LSD = Tprob * sqrt(2.0 * mean_squares_of_error / k)

		return LSD
	
class Label_Row(Row):
	"""
	A row that keeps track of which Table it belongs to.
	"""
	def __init__(self, table):
		super(Label_Row, self).__init__() # call Row.__init__()
		self.table = table
		
class Column:
	"""
	Contains references to each Cell in this column.
	"""
	def __init__(self):
		self.members = list()
		self.index = 0
	
	def __iter__(self):
		self.index = 0
		return self
	
	def next(self):
		if self.index == len(self.members):
			raise StopIteration
		self.index = self.index + 1
		return self.members[self.index]
	
	def append(self, value):
		self.members.append(value)
		self.index = self.index + 1
		
	def remove(self): # nulls the index and the member list
		self.members = []
		self.index = 0

class Cell:
	"""
	Helper class; Cells for our Table class.
	"""
	
	def __init__(self, row, column, value, year, field):
		row.append(self)
		column.append(self)
		
		self.row = row
		self.column = column
		self.value = value
		self.year = year 
		self.field = field

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
		
		top_row = [] # The top row for the table object: 'Varities', 1-yr, 2-yr, 3-yr, Loc1, Loc2, etc.
		row_labels_column = [] # Contains the varieties' names.
		year_columns = {} # Contains year(s) average values for the given varieties.
		location_columns = {} # The variety value(s) for a location(s).
		value_count = 0 # The sum of values used to calculate the mean average for a year.
		collated_table = {} 
		
		header = Row()._iter_()
		varieties = Column()._iter_()
		year = Column()._iter_() 
		location = Column()._iter_()
		
		
		def __init__(self, entries):
			self.entries = entries
			
			
		def collate_table(self, top_row, row_labels_column, year_columns, location_columns): 
			collated_table = {top_row, row_labels_column, year_columns, location_columns} # If only it were this simple. I have to balance the data, and make sure the columns align nicely.
			
			return collated_table
			
		def header_row(self, y_columns, l_columns): # This method requires populated year- and location columns.
			"""
			Prefixes to top_row 'Varieties', calculates the sum of year lists and appends
			the appropriate amount of year headers, i.e. 1-yr, 2-yr, etc.,
			appends the sorted location names, and then returns top_row.
			
			The final output should look like this:
			
			['Varieties', 'someYear', 'someYear', 'someYear, 'Casselton', 'Prosper', 'SomePlace']
			"""
			top_row = ['Varieties']
			
			for y, j in y_columns.iteritems():
				top_row = y
			
			for l, j in l_columns.iteritems():
				top_row = l
			
			return top_row
			
		def populate_year_average_columns(self, years, varieties): 
			"""
			Appends the variety values for the given years.
			
			[(minYear, value ),...,(maxYear, value)] The 'year' key will be numeric. 
			"""
			
			year_columns = {}
			max_year = max(years)
			y_temp = sorted(years, reverse=true) 
			
			if len(y_temp) > 3:
				t = y_temp[:2] # Reduce the number of year lists to 3.
				y_temp = t
			
			v_temp = sorted(varieties, key=attrgetter('name'))
			
			for entry in self.entries.iteritems(): # Yay for n^3.
				for y in y_temp:
					for  v in v_temp:
						if y == entry.harvest_date.year and v == entry.variety.name:
							try:
								year_columns = {y, [v, entry.test_weight]} # I'm not sure if this test weight is already the mean value.
							except AttributeError:
								year_columns = {y, [v, 'none']}
						else:
							year_columns = {y, [v, 'none']}
							
			return year_columns
			
		def populate_location_columns(self, locations, varieties): 
			"""
			Prefixes the location name to l_column, then appends the
			location value for each variety.
			
			The final output from l_column should look like this:
			
			[(Name, Casselton), (variety, 60.4), (variety, 60.3), (variety, 57.0)]
			"""
			columns = {} # The dictionary of columns that will return. {Location, {Variety=name, value}}
			
			l_temp = sorted(locations, key=attrgetter('name'))
			
			v_temp = sorted(varieties, key=attrgetter('name'))
			
			for entry in self.entries.iteritems(): # Yay for n^3
				for l in l_temp:
					for v in v_temp:
						if l == entry.location.name and v == entry.variety.name:
							try:
								location_columns = {l, [v, entry.test_weight]}
							except AttributeError:
								location_columns = {l, [v, 'none']}
						else:
							location_columns = {l, ['none', 'none']}
													
			return location_columns
			
		def populate_row_labels_column(self, varieties):
			"""
			Returns a list containing the labels for each row in the Table object.
			
			['Agawam', 'Albany',...'WB-Mayville']
			"""
			
			v_temp = sorted(varieties, key=attrgetter('name'))
			
			row_labels_column = set(v_temp) # Removes duplicate variety row labels.
			
			return row_labels_column 
			
		def get_year_column(self, year, collated_table):
			"""
			Returns the specified year's column from a Table object's years_columns field
			as a list. This function also appends the LSD for the given year to the list.
			"""
			
			column = []
			return column
			
		def get_location_column(self, location, collated_table): 
			"""
			Returns the specified location's column from a table object's 
			location_columns field as a list. This functions also appends
			the LSD for the given location and year.
			"""
			
			column = []
			return column
			
		def set_value_count_for_column(self, column, year): 
			"""
			Sets the sum of values used to calculate the mean averages in 
			a year column.
			"""
			
			return value_count
