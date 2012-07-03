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
		self.members = aRowList
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
		#super(LSD_Row, self).__init__(list()) # call Row.__init__()
		self.table = table
		Row.__init__(self, [])
	
	def populate(self, probability):
		
		y_columns = self.table.year_columns
		years_i = []
		l_columns = self.table.location_columns
		location_lsds = []
		
		years_i = list(y_columns[0]) # Grabs the y key, e.g., {y:{v:value}}.
		
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
		
		if data_1yr is not None:	
			lsd_1yr = self._LSD(data_1yr, probability)
		if data_2yr is not None:
			lsd_2yr = self._LSD(data_2yr, probability)
		if data_3yr is not None:
			lsd_3yr = self._LSD(data_3yr, probability)
			
		"""
		lsd_1yr = 0.1
		lsd_2yr = 0.2  # Matti's test values.
		lsd_3yr = 0.3
		"""
		
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
		# model = aov(y~trt)
		# df = df.residual(model)
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
	def __init__():
		pass

class SubTable:
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
		
			
		def __init__(self, entries, probability):
			self.entries = entries
			self.probability = probability
			
		def get(self, years, varieties, locations): # 'Years', 'varieties' and 'locations' are string values passed by the user to parse the database.
			year_columns = self.populate_year_average_columns( years, varieties) 
			location_columns = self.populate_location_columns( locations, year_columns[0])
			top_row = self.populate_header_row( year_columns[0], location_columns[0])
			row_labels_column = self.populate_row_labels_column( year_columns[0])
			self.year_columns = year_columns[0]
			self.location_columns = location_columns[0]
			self.top_row = top_row
			self.row_labels_column = row_labels_column
			return self.collate_table( top_row, row_labels_column, year_columns[0], location_columns[0], self.probability)
			
		def populate_year_average_columns(self, years, varieties): 
			"""
			This function returns a dictionary like so: {year:{variety:test_weight}} 
			"""
			
			year_columns = {} # The big dictionary with all the information you could possible want, e.g. {year: {variety: test_weight}}.
			
			if len(years) >= 3:
				t = years[:2] # Reduce the count of years to 3, and hope that the years are sorted.
				y_temp = t
				# If the following query is confusing, refer to this link: https://docs.djangoproject.com/en/1.4/ref/models/querysets/#values
				# When using the .values() function when creating a query set, it pairs values with the keys that are queried, thus creating dictionaries.
				# The downside of this query is that it doesn't create nested dictionaries.
				for v in varieties:
					query_set_year1 = Trial_Entry.objects.filter(harvest_date__year=y_temp[0].date.year, variety__name=v.test_weight).values(v.name)
					query_set_year2 = Trial_Entry.objects.filter(harvest_date__year=y_temp[1].date.year, variety__name=v.test_weight).values(v.name)
					query_set_year3 = Trial_Entry.objects.filter(harvest_date__year=y_temp[2].date.year, variety__name=v.test_weight).values(v.name)
				
				year_columns = {years[0]:query_set_year1, years[1]:query_set_year2, years[2]:query_set_year3}
				
			elif len(years) == 2:
				t = years[:1]
				y_temp = t
				
				for v in varieties:
					query_set_year1 = Trial_Entry.objects.filter(harvest_date__year=y_temp[0].date.year, variety__name=v.test_weight).values(v.name)
					query_set_year2 = Trial_Entry.objects.filter(harvest_date__year=y_temp[1].date.year, variety__name=v.test_weight).values(v.name)
				
				year_columns = {years[0]:query_set_year1, years[1]:query_set_year2}
				
			elif len(years) == 1:
				t = years[0]
				y_temp = t
				
				for v in varieties:
					query_set_year1 = Trial_Entry.objects.filter(harvest_date__year=y_temp[0].date.year, variety__name=v.test_weight).values(v.name)
				
				year_columns = {years[0]:query_set_year1}
							
			return year_columns
			
		def populate_location_columns(self, years, locations):
			"""
			Creates a dictionary of location columns:
			{location: {variety:test_weight}}
			"""
			
			location_columns = {}
			
			if len(years) >= 3:
				t = years[:2] # Reduce the number of years to 3, and hope that the years are sorted.
				y_temp = t
				
				for l in locations:
					query_set_year1 = Trial_Entry.objects.filter(harvest_date__year=y_temp[0].date.year,location__name=l.name).values(l.name)
					query_set_year2 = Trial_Entry.objects.filter(harvest_date__year=y_temp[1].date.year,location__name=l.name).values(l.name)
					query_set_year3 = Trial_Entry.objects.filter(harvest_date__year=y_temp[2].date.year,location__name=l.name).values(l.name)
				
				location_columns = {y_temp[0]:query_set_year1, y_temp[1]:query_set_year2, y_temp[2]:query_set_year3}
							
			elif len(years) == 2:
				t = years[:1]
				y_temp = t
				
				for l in locations:
					query_set_year1 = Trial_Entry.objects.filter(harvest_date__year=y_temp[0].date.year,location__name=l.name).values(l.name)
					query_set_year2 = Trial_Entry.objects.filter(harvest_date__year=y_temp[1].date.year,location__name=l.name).values(l.name)
			
				location_columns = {y_temp[0]:query_set_year1, y_temp[1]:query_set_year2}
			
			elif len(years) == 1:
				t = years[0]
				y_temp = t
			
				for l in locations:
					query_set_year1 = Trial_Entry.objects.filter(harvest_date__year=y_temp[0].date.year,location__name=l.name).values(l.name)
			
				location_columns = {y_temp[0]:query_set_year1}
			
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
				t.append(k) # This grabs the variety name, but not the value associated with it.
				
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
				for y in year_columns.keys():
					top_row.append(y)
				
				for l in location_columns.keys():
					top_row.append(l)
					
			except (IndexError, SyntaxError, KeyError): 
				pass 
			
			return top_row	
			
		def collate_table(self, top_row, row_labels_column, year_columns, location_columns, probability): 
			"""
			This function creates one big dictionary with keys that label each part of a table.
			keys: header; rows; years; locations; lsds.
			"""	
			try:
				collated_table = {'header':top_row, 'rows':row_labels_column, 'years':year_columns[0], 'locations':location_columns[0]}
			except (IndexError, SyntaxError, KeyError):
				pass
				
			lsdCalc = LSD_Row(self)
			lsd_row = lsdCalc.populate(probability)
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
			Sets the count of values used to calculate the mean average for the LSD calculator in 
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
