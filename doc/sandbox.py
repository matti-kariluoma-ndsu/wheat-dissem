#!/usr/bin/python
# coding=utf8
#
# Sandbox for testing the LSD module
#
# Matti Kariluoma Sep 2011 <matti.kariluoma@gmail.com>

from LSD import LSD

def main():
	
	y1 = [1, 3, 1, 2]
	y2 = [1, 3, 1, 2]
	y3 = [1, 3, 1, 2]
	trt = [y1, y2, y3]
	
	print LSD(trt, 0.05)
	
	
if __name__ == '__main__':
	main()
