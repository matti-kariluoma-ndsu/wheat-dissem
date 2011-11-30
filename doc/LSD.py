#!/usr/bin/python
# coding=utf8
#
# Python routines to caclulate the LSD of a balanced data set.
#
# Taken line-by-line from the agricolae project
# (http://cran.r-project.org/web/packages/agricolae/index.html ,
#  http://tarwi.lamolina.edu.pe/~fmendiburu) for R 
# (http://r-project.org)
#
# Matti Kariluoma Sep 2011 <matti.kariluoma@gmail.com>

from math import sqrt, pi, cos, sin, exp
from scipy.special import erfinv

def LSD(response_to_treatments, probability):
	"""
	A stripped-down reimplementation of LSD.test from the agricoloae
	package. (http://cran.r-project.org/web/packages/agricolae/index.html)
	
	Calculates the Least Significant Difference of a multiple comparisons
	trial, over a balanced dataset.
	"""
		
	def qnorm(probability):
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
			
	def qt(probability, degrees_of_freedom):
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
				x = qnorm(P*0.5)
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

	trt = response_to_treatments
	#model = aov(y~trt)
	#df = df.residual(model)
	# df is the residual Degrees of Freedom
	# n are factors, k is responses per factor
	n = len(trt)
	k = len(trt[0]) # == len(trt[1]) == ... == len(trt[n])
	degrees_freedom_of_error = (n-1)*(k-1)
	
	# SSE is the Error Sum of Squares
	
	treatment_means = {}
	for i in range(len(trt)):
		total = 0.0
		count = 0
		for j in trt[i]:
			total += float(j)
			count += 1
		treatment_means[i] = total/float(count)
	
	SSE = 0.0
	for i in range(len(trt)):
		for j in trt[i]:
			SSE += (float(j) - treatment_means[i])**2.0
	
	print "SSE: %f\n" % (SSE)
	#TODO: SSE is wrong.
	
	mean_squares_of_error = SSE / degrees_freedom_of_error
	
	print "MSE: %f\n" % (mean_squares_of_error)
	
	Tprob = qt(probability, degrees_freedom_of_error)
	
	print "t-value: %f\n" % (Tprob)
	
	LSD = Tprob * sqrt(2.0 * mean_squares_of_error / k)

	return LSD

	

def main():
	y1 = [1, 3, 1, 2]
	y2 = [1, 3, 1, 2]
	y3 = [1, 3, 1, 2]
	trt = [y1, y2, y3]

	print LSD(trt, 0.05)
	
	
if __name__ == '__main__':
	main()
