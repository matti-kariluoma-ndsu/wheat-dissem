#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django.template import Library

register = Library()

def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

def divide(value, arg):
		"Divides the arg by the value, as ints"
		return int(value) / int(arg)

register.filter('sub', sub)
register.filter('divide', divide)
