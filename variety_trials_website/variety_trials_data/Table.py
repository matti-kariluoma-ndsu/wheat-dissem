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
		return self
	
	def next(self)
		if self.index == len(self.members):
			raise StopIteration
		self.index = self.index + 1
		return self.members[self.index]
	
	def append(self, value):
		self.members.append(value)
		self.index = self.index + 1

class LSD_Row(Row):
	"""
	A row that keeps track of which Table it belongs to.
	"""
	def __init__(self, table):
		super(LSD_Row, self).__init__() # call Row.__init__()
		self.table = table
	
	def populate(self, probability):
		data_1yr = self.table.fetch(years=[1])
		data_2yr = self.table.fetch(years=[1,2])
		data_3yr = self.table.fetch(years=[1,2,3])
		lsd_1yr = self._LSD(data_1yr, probability)
		lsd_2yr = self._LSD(data_2yr, probability)
		lsd_3yr = self._LSD(data_3yr, probability)
		
		lsds = []
		for column in self.table.columns:
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
		return self
	
	def next(self)
		if self.index == len(self.members):
			raise StopIteration
		self.index = self.index + 1
		return self.members[self.index]
	
	def append(self, value):
		self.members.append(value)
		self.index = self.index + 1

class Cell:
	"""
	Helper class; Cells for our Table class.
	"""
	
	def __init__(self, row, column, value):
		row.append(self)
		column.append(self)
		
		self.row = row
		self.column = column
		self.value = value

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
		
		top_row = {} # The top row for the table object: 'Varities', 1-yr, 2-yr, 3-yr, Loc1, Loc2, etc.
		row_labels_column = [] # Contains the varieties' names.
		year_columns = {} # Contains year(s) average values for the given varieties.
		location_columns = {} # The variety value(s) for a location(s).
		lsd_row = {} # Contains the LSDs calculated from an n year period, plus the LSD for each location.
		value_count = 0 # The sum of values used to calculate the mean average for a year.
		
		
		def __init__(lsd = LSD._init_(self, entries, locations, varieties, years, pref_year, field)): 
			return collate_table(lsd)
			
		def collate_table(lsd): # Must pass a table object. If a field of an object is null, so be it.
			collated_table = {}
			return collated_table
			
		def header_row(): # def _init_() must be called first to instantiate a table object, otherwise, this will return nothing.
			"""
			Prefixes to top_row 'Varieties', calculates the sum of year lists and appends
			the appropriate amount of year headers, i.e. 1-yr, 2-yr, etc.,
			appends the sorted location names, and then returns top_row.
			
			The final output should look like this:
			
			[(column1, Variety), (year, 1-yr), (year, 2-yr), (year, 3-yr), (location, Casselton), (location, Prosper), (location, SomePlace)]
			"""
			return top_row
			
		def populate_lsd_row(): # def _init_() must be called first to instantiate a table object, otherwise, this will return nothing.
			"""
			Prefixes to bottom_row 'LSD', then calculates the LSD from the
			location lists by year and appends by minimum year first. Next,
			appends the LSDs from the database for each location.
			
			If the entry is spanning three years and includes three locations, 
			the final output should look like this:
			
			[(column1, LSD), (year, 2.5), (year, 2.6), (year, 2.7), (location, 3), (location, 2.1), (Location, 4.5)]
			"""
			
			return lsd_row
			
		def populate_year_average_columns(): # def _init_() must be called first to instantiate a table object, otherwise, this will return nothing.
			"""
			Prefixes the year from lsd.year, which is the maximum year from
			lsd object's list of years, creates subsequent elements in the
			year_columns dictionary that are lists of the previous year(s)
			values. This function prefixes the maxium year to this dictionary first, 
			but years are appended to this dictionary from smallest to greatest.
			
			[(Name, theMaxYear), (year, theMinYear),...,(year, theMaxYear)]
			"""
			
			return year_columns
			
		def populate_location_columns(): # def _init_() must be called first to instantiate a table object, otherwise, this will return nothing.
			"""
			Prefixes the location name to l_column, then appends the
			location value for each variety. Finally, the last step appends
			the LSD for the given varieties at that location.
			
			The final output from l_column should look like this:
			
			[(Name, Casselton), (variety, 60.4), (variety, 60.3), (variety, 57.0), (lsd, 2.5)]
			"""
			
			return location_columns
			
		def get_year_column(year): # def _init_() must be called first to instantiate a table object, otherwise, this will return nothing.
			"""
			Returns the specified year's column from a Table object's years_columns field
			as a list. This function also appends the LSD for the given year to the list.
			"""
			
			column = []
			return column
			
		def get_location_column(location): # def _init_() must be called first to instantiate a table object, otherwise, this will return nothing.
			"""
			Returns the specified location's column from a table object's 
			location_columns field as a list. This functions also appends
			the LSD for the given location and year.
			"""
			
			column = []
			return column
			
		def set_value_count_for_column(year_columns, year): 
			"""
			Sets the sum of values used to calculate the mean averages in 
			a year column.
			"""
			
			return value_count