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
	def __init__(self, aRowList):
		self.members = aRow
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
		
		columns = self.table.year_columns
		years_i = []
		
		for k in columns.keys():
			years_i = k
		
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
		
		if data_1yr != None:	
			lsd_1yr = self._LSD(data_1yr, probability)
		if data_2yr != None:
			lsd_2yr = self._LSD(data_2yr, probability)
		if data_3yr != None:
			lsd_3yr = self._LSD(data_3yr, probability)
		
		lsds = []
		"""
		for column in self.table.year_columns.keys(): 
			lsds.append(column.lsd) 
		"""
		
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
	def __init__(self, aColumnList):
		self.members = aColumn
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
		year_columns = [] # Contains year(s) average values for the given varieties. Three lists in this list, 
		location_columns = [] # The variety value(s) for a location(s).
		value_count = 0 # The sum of values used to calculate the mean average for a year.
		collated_table = {}
		lsd_row = []
		max_year = 0 
		
			
		def __init__(self, entries, probability): # Probability is required for creating the LSD row in the collate_table function.
			self.entries = entries
			self.populate_year_average_columns(self, years, varieties)
			self.populate_location_columns(self, locations, year_columns)
			self.populate_header_row(self, year_columns, location_columns)
			self.populate_row_labels_column(self, year_columns)
			self.collate_table(self, top_row, row_labels_column, year_columns, location_columns)
			
		def populate_year_average_columns(self, years, varieties): 
			"""
			Appends the variety values for the given years.
			
			[(maxYear, value ),...,(minYear, value)] The 'year' key will be numeric. 
			"""
			
			y1 = {} # The big dictionary with all the information you could possible want, e.g. {Year: {Variety: Value}}.
			y2 = [] # This contains just the variety values, it doesn't have all the annoying keys. 
			y3 = [] # This will be a list of headers, which are grabbed in the populate_header_row function.
			v_temp = sorted(varieties, key=attrgetter('name'))
			y_temp = sorted(years, reverse=true) 
			
			if len(y_temp) > 3:
				t = y_temp[:2] # Reduce the number of years to 3.
				y_temp = t
			
			for entry in self.entries: # Yay for n^3.
				for y in y_temp:
					for  v in v_temp:
						if y == entry.harvest_date.year and v == entry.variety.name:
							try:
								y1 = {y: {v: entry.test_weight}} # I'm not sure if this test weight is already the mean value.
								y2 = entry.test_weight
								y3 = y
							except AttributeError:
								y1 = {y: {v: None}} 
								y2 = None
								y3 = y
						else:
							y1 = {y: {v: None}}
							y2 = None
							y3 = y
							
			year_columns = [y1, y2, y3]
							
			return year_columns
			
		def populate_location_columns(self, locations, year_columns): 
			"""
			Creates a dictionary of locations columns.
			
			The final output from l_column should look like this:
			
			[(Name, Casselton), (variety, 60.4), (variety, 60.3), (variety, 57.0)]
			"""
			
			l_temp = sorted(locations, key=attrgetter('name'))
			l1 = {} # The big dictionary with all the information you could possible want, e.g. {Location: {Variety: Value}}
			l2 = [] # This contains just the variety values, it doesn't have all the annoying keys..
			l3 = [] # This will be a list of headers, which are grabbed in the populate_header_row function.
			
			for y, v in year_columns: # Grabs the varieties from year_columns. This aligns year_columns and location_columns in Table object.
				v_temp = v[0]
			
			for entry in self.entries: # Yay for n^3
				for l in l_temp:
					for v in v_temp:
						if l == entry.location.name and v == entry.variety.name:
							try:
								l1 = {l: {v: entry.test_weight}}
								l2 = entry.test_weight
								l3 = l
							except AttributeError:
								l1 = {l: {v: None}}
								l2 = None
								l3 = l
						else:
							l1 = {l: {v: None}}
							l2 = None
							l3 = l
			
			location_columns = [l1, l2, l3]
													
			return location_columns
			
		def populate_row_labels_column(self, year_columns):
			"""
			Returns a list containing the labels for each row in the Table object.
			
			['Agawam', 'Albany',...'WB-Mayville']
			"""
			
			temp = []
			t = []
			
			try:
				temp = year_columns[0]
			except (IndexError, SyntaxError, KeyError):
				pass
				
			for k in temp.keys():
				t = k # This grabs the variety name, but not the value associated with it.
				
			row_labels_column = set(sorted(t)) # Remove possible duplicates.
					
			return row_labels_column 
			
		def populate_header_row(self, year_columns, location_columns): # This function requires populated year- and location columns.
			"""
			Prefixes to top_row 'Varieties', calculates the sum of year lists and appends
			the appropriate amount of year headers, i.e. 1yr, 2yr, etc.,
			appends the sorted location names, and then returns top_row.
			
			The final output should look like this:
			
			['Varieties', 'someYear', 'someYear', 'someYear, 'Casselton', 'Prosper', 'SomePlace']
			"""
			top_row = ['Varieties']
			
			try:
				top_row = year_columns[2] # There had better be something at these indexes.
				top_row = location_columns[2]
			except (IndexError, SyntaxError, KeyError): 
				pass 
			
			return top_row	
			
			
		def collate_table(self, top_row, row_labels_column, year_columns, location_columns, probability): 
			"""
			This function creates one big dictionary with keys that label each part of a table.
			keys: header; rows; years; locations; lsds.
			"""	
			try:
				collated_table = {'header':top_row, 'rows':row_labels_column, 'years':year_columns[0], 'locations':location_columns[0]} # Hrmm.
			except (IndexError, SyntaxError, KeyError):
				pass
				
			lsdCalc = LSD_Row().init(self)
			lsd_row = lsdCalc.populate(self, probability) # Figure out how this probability will pass to here.
			collated_table = {'lsds':lsd_row}
			
			return collated_table
			
			
		def get_year_column(self, year, year_columns):
			"""
			Returns the specified year's column from a Table object's years_columns field
			as a list.
			"""
			
			try:
				temp = year_columns[0] # Grabs the dictionary of year columns.
			except (IndexError, SyntaxError, KeyError):
				pass
				
			column = temp[year]
			return column
			
		def get_location_column(self, location, location_columns): 
			"""
			Returns the specified location's column from a table object's 
			location_columns field as a list.
			"""
			
			try:
				temp = location_columns[0] # Grabs the dictionary of location columns.
			except (IndexError, SyntaxError, KeyError):
				pass
			
			column = temp[location]
			return column
			
		def set_value_count_for_column(self, year_columns, year): 
			"""
			Sets the count of values used to calculate the mean averages in 
			a year column.
			"""
			
			temp = []
			value_count = 0
			
			if year_columns[year]:
				temp = year_columns[year]
			
			if len(temp) > 0:
				for t in temp.keys():
					for v in temp.keys[t].keys():
						value_count  += 1 
			
			return value_count
			
		def set_table_year(self, year):
			max_year = year
			return max_year
