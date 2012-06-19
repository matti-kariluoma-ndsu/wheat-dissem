from variety_trials_data.models import Trial_Entry #, Date
from variety_trials_data import models
from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv
from itertools import chain
from operator import attrgetter
import copy

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
	
	def delete_row(self):
		self.row = None
	
	def delete_column(self):
		self.column = None
		
	def delete_value(self):
		self.value = None
		
	def clear(self):
		self.delete_row()
		self.delete_column()
		self.delete_value()

class Row:
	"""
	Contains references to each Cell in this row.
	"""
	def __init__(self, variety):
		self.variety = variety
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
				m.delete_row()
		self.members = []

class LSD_Row(Row):
	"""
	A row that keeps track of which Table it belongs to.
	"""
	def __init__(self, variety, table):
		Row.__init__(self, variety)
		self.table = table
		
	
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
			
		def __init__(self, lsd_probability): # Probability is required for creating the LSD row
			self.lsd_probability = lsd_probability
			self.rows = {}
			self.columns = {}
			
		def get_row(self, variety):
			try:
				row = self.rows[variety]
			except KeyError:
				row = self.rows[variety] = Row(variety)
			return row
							
		
		def get_column(self, location):
			try:
				col = self.columns[location]	
			except KeyError:
				col = self.columns[location] = Column(location)
			return col

class Page:
	def __init__(self, entries, lsd_probability):
		self.entries = entries
		self.tables = []
		table = Table(lsd_probability)
		self.tables.append(table)
		for entry in entries:
			# create a new cell object, which adds itself to the given row & column
			Cell(table.get_row(entry.variety), table.get_column(entry.location), entry)

