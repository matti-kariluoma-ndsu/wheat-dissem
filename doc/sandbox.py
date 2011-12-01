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
	
	#print LSD(trt, 0.05)
	
	ada = [96.3,	103.3,	78.5,	83.6,	82.2,	77.8,	85,	95,	68,	64.5,	76.9,	53.6]
	albany = [109.0,	123.7,	69.6,	97.7,	106.0,	83.9,	102,	121,	66,	67.4,	92.6,	64.5]
	barlow = [89.8,	103.1,	83.1,	90.3,	83.7,	86.5,	73,	78,	57,	69.1,	79.3,	57.0]
	blade = [98.7,	109.6,	73.4,	87.1,	89.9,	75.5,	89,	92,	50,	65.8,	75.9,	62.7]
	breaker = [99.0,	112.1,	84.3,	89.7,	71.1,	78.1,	86,	97,	60,	72.4,	82.3,	63.3]
	brennan = [97.4,	108.5,	83.3,	84.1,	86.5,	77.2,	78,	100,	49,	62.3,	73.2,	42.7]
	brick = [98.7,	108.6,	84.7,	71.5,	91.9,	75.7,	78,	83,	54,	64.6,	80.8,	52.3]
	briggs = [93.9,	102.1,	68.7,	84.8,	83.5,	81.8,	70,	72,	53,	67.5,	77.3,	55.3]
	cromwell = [99.2,	110.1,	75.7,	88.1,	87.2,	77.3,	82,	86,	65,	61.9,	77.7,	59.9]
	faller = [111.1,	107.6,	82.0,	106.3,	104.4,	94.3,	92,	106,	69,	73.0,	86.5,	53.6]
	glenn = [91.9,	94.9,	83.4,	75.5,	83.0,	74.6,	70,	69,	46,	67.1,	71.5,	55.7]
	jenna = [97.0,	111.6,	84.2,	92.3,	86.2,	76.7,	83,	100,	61,	65.1,	82.3,	51.0]
	kelby = [98.7,	95.0,	85.5,	73.7,	80.2,	73.1,	79,	95,	51,	63.4,	71.4,	44.9]
	knudson = [97.8,	106.5,	79.4,	93.3,	87.3,	81.7,	87,	92,	59,	68.9,	78.1,	62.3]
	marshall = [93.8,	85.9,	68.0,	82.7,	83.1,	68.7,	70,	94,	65,	60.4,	77.0,	50.0]
	oklee = [91.6,	104.8,	81.6,	84.1,	84.4,	77.2,	79,	87,	51,	65.4,	76.0,	54.3]
	rbo7 = [103.3,	91.2,	88.5,	87.4,	89.1,	79.4,	78,	94,	60,	67.7,	72.9,	55.5]
	sabin = [100.5,	105.1,	75.4,	84.2,	92.3,	78.6,	78,	88,	59,	63.7,	80.0,	48.9]
	samson = [106.9,	106.2,	85.2,	102.8,	87.3,	89.7,	92,	106,	67,	70.8,	82.0,	54.9]
	select = [102.9,	103.3,	72.6,	86.4,	77.2,	85.8,	71,	81,	54,	69.7,	80.2,	49.0]
	tom = [96.9,	101.1,	93.7,	80.1,	84.8,	84.7,	76,	90,	53,	65.0,	77.2,	51.9]
	vantage = [87.1,	96.2,	72.3,	91.1,	82.4,	77.0,	78,	98,	64,	68.0,	80.2,	53.1]
	
	trt = [ada,albany,barlow,blade,breaker,brennan,brick,briggs,
			cromwell,faller,glenn,jenna,kelby,knudson,marshall,oklee,
			rbo7,sabin,samson,select,tom,vantage]
	
	print LSD(trt, 0.05, randomized_block_design=True)
	
	
	
if __name__ == '__main__':
	main()
