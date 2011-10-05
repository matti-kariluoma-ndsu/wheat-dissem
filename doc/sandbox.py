#!/usr/bin/python
# coding=utf8
#
# Sandbox for testing the LSD module
#
# Matti Kariluoma Sep 2011 <matti.kariluoma@gmail.com>

from LSD import LSD

def main():
	
	barnes =    [90.5,	86.9,	89.9,	96.9,	85.4,	86.3,	83.8,	92.7]
	crookston = [73.1,	78.4,	78.0,	92.1,	84.7,	90.2,	77.6,	71.4]
	dickey =    [61.7,	76.9,	56.4,	61.1,	56.3,	69.6,	67.2,	62.0]
	fergus =    [81.5,	72.1,	71.7,	96.8,	84.3,	85.0,	84.2,	82.1]
	nelson =    [76.8,	69.1,	74.5,	82.9,	78.2,	69.1,	70.2,	63.0]
	oklee =     [78.0,	99.8,	83.1,	105.6,77.4,	110.2,94.3,	81.0]
	perley =    [70.3,	62.3,	68.1,	75.6,	74.5,	67.7,	75.3,	72.3]
	avgs =      [75.99,77.93,74.53,87.29,77.26,82.59,78.94,74.93]

	trt = [barnes, crookston, dickey, fergus, nelson, oklee, perley]
	
	print LSD(trt, 0.05)
	
	
if __name__ == '__main__':
	main()
