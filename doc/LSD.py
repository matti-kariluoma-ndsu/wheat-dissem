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
			c = (((20700.0*a)/b - 98.0)*a - 16.0)*a + 96.36
			d = ((94.5/(b+c) - 3.0)/b + 1.0)*sqrt((a*pi)/2.0)*float(n)
			x = d*P
			y = x**(2.0/float(n))
		
			if (y > 0.05 + a):
				x = qnorm(P*0.5)
				y = x**2.0
				
				if (n < 5):
					c = c + 0.3*(float(n)-4.5)*(x+0.6)

				#c = (((0.05*d*x-5.0)*x-7.0)*x-2.0)*x+b+c
				c1 = (0.05*d*x) - 5.0
				c2 = c1*x - 7.0
				c3 = c2*x - 2.0
				c4 = c3*x + b + c
				c = c4
				#y = (((((0.4*y+6.3)*y+36.0)*y+94.5)/c-y-3.0)/b+1.0)*x
				y1 = (0.4*y+6.3)*y + 36.0
				y2 = y1*y + 94.5
				y3 = y2/c - y - 3.0
				y4 = y3/b + 1.0
				y5 = y4*x
				y = y5
				
				y = a*(y**2.0)
				
				if (y > 0.002):
					y = exp(y) - 1.0
				else:
					y = 0.5*(y**2.0) + y

			else:
				#y = ((1.0/(((float(n)+6.0)/(float(n)*y)-0.089*d-0.822)*(float(n)+2.0)*3.0)+0.5/(float(n)+4.0))*y-1.0)*(float(n)+1.0)/(float(n)+2.0)+1.0/y
				y1 = float(n)+6.0
				y2 = y1/(float(n)*y)
				y3 = y2 - 0.089*d - 0.822
				y4 = y3 * (float(n)+2.0) * 3.0
				y5 = 1.0 / y4
				y6 = y5 + 0.5/(float(n)+4.0)
				y7 = y6*y - 1.0
				y8 = y7 * (float(n)+1.0) 
				y9 = y8 / (float(n)+2.0) 
				y10 = y9 + 1.0/y
				y= y10
			
			t = sqrt(float(n)*y)
		
		return t

	trt = response_to_treatments
	#model = aov(y~trt)
	#df = df.residual(model)
	# df is the residual Degrees of Freedom
	# n are factors, k is responses per factor (treatments)
	n = len(trt) 
	k = len(trt[0]) # == len(trt[1]) == ... == len(trt[n]) iff we have a balanced design
	degrees_freedom_of_error = (n-1)*(k-1)
	
	treatment_means = {}
	for i in range(n): # n == len(trt)
		total = 0.0
		for j in range(k):
			total += float(trt[i][j])
		treatment_means[i] = total/k
		
	print "Calculating the Block Mean"	
	block_means = {}
	for j in range(k):
		total = 0.0
		for i in range(n):
			total += float(trt[i][j])
			print "The total is : " +str(total)
		block_means[j] = total/n
		print "The block mean is : " + str(block_means[j])
	
	grand_mean = sum(treatment_means.values()) / float(n)
	
	# TODO: what is the difference between type I and type III SS? (http://www.statmethods.net/stats/anova.html)
	print "The difference between type I and type III SS"
	SSE = 0.0
	for i in range(n): # n == len(trt)
		for j in range(k):
			SSE += (float(trt[i][j]) - treatment_means[i] - block_means[j] + grand_mean)**2.0
	
			print "Navneet trial"
			print "treatment value for rows and columns is : " + str(trt[i][j])
			print "The treatment mean is: " + str(treatment_means[i])
			print "The block mean is : " + str(block_means[j])
			print "The grand mean is : " + str(grand_mean)
			print "The value of SSE is : " + str(SSE)
			
	#print "SSE: %f\n" % (SSE)
	
	mean_squares_of_error = SSE / degrees_freedom_of_error
	
	print "MSE: %f\n" % (mean_squares_of_error)
	
	Tprob = qt(probability, degrees_freedom_of_error)
	print "The probability is: " + str(probability)
	print "Degrees of freedom: " + str(degrees_freedom_of_error)
	print "T-distribution is: " + str(Tprob)
	#print "t-value: %f\n" % (Tprob)
	
	LSD = Tprob * sqrt(2.0 * mean_squares_of_error / k)

	return LSD

	

def main():
	input1 = [
		[64.5, 62.899999999999999, 48.600000000000001, 76.900000000000006],
		[65.799999999999997, 60.200000000000003, 47.100000000000001, 75.900000000000006],
		[68.900000000000006, 71.400000000000006, 56.700000000000003, 78.099999999999994],
		[60.399999999999999, 48.799999999999997, 36.899999999999999, 77.0],
		[65.400000000000006, 66.599999999999994, 51.0, 76.0]
	]
	result1 = 5.97687782
	
	input2 = [
		[13.300000000000001, 9.1999999999999993],
		[12.5, 7.5999999999999996]
	]
	result2 = 5.08248189

	input3 = [
		[11.6, 7.4000000000000004], 
		[14.0, 10.4]
	]
	result3 = 3.81186142
	
	input4 = [
		[4.5, 5.0999999999999996], 
		[13.5, 8.8000000000000007], 
		[13.9, 4.0999999999999996], 
		[8.4000000000000004, 6.4000000000000004], 
		[6.0999999999999996, 8.1999999999999993], 
		[18.899999999999999, 14.1], 
		[11.0, 8.1999999999999993], 
		[13.0, 8.5], 
		[9.5, 9.6999999999999993], 
		[11.9, 11.800000000000001], 
		[13.4, 10.4], 
		[5.7999999999999998, 6.2999999999999998], 
		[16.5, 15.1], 
		[8.0999999999999996, 2.5]
	]
	result4 = 4.86117238
	
	print "Calculated LSD value is: " + str(LSD(input2, 0.05))
	print result2
	print "==="

	"""
	print LSD(input1, 0.05)
	print result1
	print "==="
	
	print LSD(input1, 0.05)
	print result1
	print "==="
	
	print LSD(input3, 0.05)
	print result3
	print "==="
	
	print LSD(input4, 0.05)
	print result4
	print "==="
	"""
	
if __name__ == '__main__':
	main()
