from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv

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
		
	def __unicode__(self):
		row = [unicode(self.variety)]
		row.extend([unicode(cell) for cell in self])
		return unicode(" ").join(row)

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
					lsd = real_cell.get(cell.year, "lsd_05")
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
		"""
		
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

