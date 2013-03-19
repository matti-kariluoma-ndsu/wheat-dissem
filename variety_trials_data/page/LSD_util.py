#!/usr/bin/env python
# coding: ascii

"""
Provides mechanisms to calculate the LSD, usually for multiple trials.
"""

from math import sqrt, pi, exp
from scipy.special import erfinv
import os, sys, signal, tempfile
from subprocess import Popen, STDOUT, PIPE, check_output, call, CalledProcessError
from variety_trials_website import settings

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

class LSD_Calculator():
	"""
	"""
	def __init__(self):
		pass
	
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
			raise LSDProbabilityOutOfRange("Alpha-value out of range: '%s'" % (P))
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
	
	def _R_subprocess(self, response_to_treatments, treatment_factors, blocking_factors, probability):
		"""
		Hey, just stop right there. 
		
		This code isn't meant to be readable or maintainable. 
		
		We're going to create some temporary files,	write some R code to 
		them, run them through /usr/bin/R, then delete them.
		
		This process is difficult to debug, even when the code is properly 
		working. It'd best to comment out the os.unlink/0 commands and send
		the generated scripts to an R programmer for debugging.
		"""
		# collapse into single list
		trt = []
		for row in response_to_treatments:
			trt.extend(row)
		len_blocking_factors = len(blocking_factors)
		len_treatment_factors = len(treatment_factors)
		len_repetitions = int(len(trt) / (len_blocking_factors * len_treatment_factors))
		str_blocking_factors = ','.join(['"%s"'%str(block) for block in blocking_factors])
		str_treatment_factors = ','.join(['"%s"'%str(treat) for treat in treatment_factors])
		
		R_script = tempfile.NamedTemporaryFile(delete=False)
		R_out = tempfile.NamedTemporaryFile(delete=False)
		R_out.close()
		
		R_script.write('.libPaths("%s")\n' % settings.R_LIBRARY)
		R_script.write('yield <- c(%s)\n' % ','.join([str(t) for t in trt]))

		R_script.write('Varieties <- factor(c(\n')
		for _ in range(len_repetitions):
			R_script.write('rep(c(%s), rep(%d,%d)),\n' % (
					str_treatment_factors,
					len_blocking_factors,
					len_treatment_factors
				))
		R_script.write('c()))\n')
		R_script.write('Environments <- factor(c(\n')
		for _ in range(len_repetitions):
			R_script.write('rep(c(%s), %d),\n' % (
					str_blocking_factors,
					len_treatment_factors
				))
		R_script.write('c()))\n')
		R_script.write('''model <- aov(yield ~ Varieties + Environments)
mse <- deviance(model) / df.residual(model) 
require(agricolae)
LSD.test(yield, Varieties, df.residual(model), mse, alpha=%s)
''' % probability)
		R_script.close()
		
		"""
		IS_POSIX = 'posix' in sys.builtin_module_names
		R =  Popen(
			[
				os.sep.join(['usr','bin','R']),
				'CMD',
				'BATCH',
				'--no-restore',
				'--no-timing',
				'--quiet',
				f.name,
				'/dev/stdout'
			], 
			stdout=PIPE, 
			bufsize=1,
			close_fds=IS_POSIX
		)
		#"""
		try:
			call(
					[
						'R', 
						'CMD',
						'BATCH',
						'--no-restore',
						'--no-timing',
						'--quiet',
						R_script.name,
						R_out.name
					]
				);
		except CalledProcessError:
			print R_script.name
			print output.name
			raise
		#"""
		
		os.unlink(R_script.name)
		
		output = None
		
		debug = tempfile.NamedTemporaryFile(delete=False)
		with open(R_out.name, 'r') as f:
			for line in f:
				debug.write(line)
				if line.startswith("Least Significant Difference"):
					output = line
					break
		
		debug.close()
		os.unlink(R_out.name)
		
		if output:
			value = float(output[29:])
		else:
			value = None
		
		return value
	
	def calculate_lsd(self, unbalanced_input, varieties, locations, lsd_probability, digits=1, internal_implementation=True):
		"""
		for table in unbalanced_input:
			for row in unbalanced_input[table]:
				print row
			print "==="
		#"""
		
		#
		## delete rows that are all None
		#
		delete_rows = [] # indexes of rows to delete
		for year in unbalanced_input:
			for (r, row) in enumerate(unbalanced_input[year]):
				delete_row = True
				for cell in row:
					if cell is not None:
						delete_row = False
						break
				if delete_row:
					delete_rows.append(r)
					
		for index in sorted(list(set(delete_rows)), reverse=True):
			for year in unbalanced_input:
				unbalanced_input[year].pop(index)
			varieties.pop(index)
		#
		## delete columns that are all None		
		#
		delete_columns = [] # indexes of columns to delete
		for year in unbalanced_input:
			column_length = len(unbalanced_input[year])
			delete_column = {} # was `[0] * len(row)' but len(row) != num_columns...?
			for row in unbalanced_input[year]: 
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
			for year in unbalanced_input:
				for row in unbalanced_input[year]:
					row.pop(index)
			locations.pop(index)
		#
		## delete rows with impudence until balanced
		#
		delete_rows = [] # indexes of rows to delete
		for year in unbalanced_input:
			for (r, row) in enumerate(unbalanced_input[year]):
				delete_row = False
				for cell in row:
					if cell is None:
						delete_row = True
						break
						
				if delete_row:
					delete_rows.append(r)
					
		for index in sorted(list(set(delete_rows)), reverse=True):
			for year in unbalanced_input:
				unbalanced_input[year].pop(index)
			varieties.pop(index)
		#"""
		print '%d: %s' % (len(locations), locations)
		print '%d: %s' % (len(varieties), varieties)
		for table in unbalanced_input:
			for row in unbalanced_input[table]:
				print '%d: %s' % (len(row), row)
			print "==="
		#"""
		
		balanced_input = []
		for year in unbalanced_input:
			balanced_input.extend(unbalanced_input[year])
			
		#print balanced_input
		
		lsd = None
		if len(balanced_input) > 1 and len(balanced_input[0]) > 1:
			try:
				if internal_implementation:
					lsd = self._LSD(balanced_input, lsd_probability)
				else:
					lsd = self._R_subprocess(balanced_input, varieties, locations, lsd_probability)
				if lsd is not None:
					lsd = round(lsd, digits)
			except (LSDProbabilityOutOfRange, TooFewDegreesOfFreedom):
				lsd = None
		
		return lsd
