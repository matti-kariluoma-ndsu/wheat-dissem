#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django.template import Library
from django.utils.http import urlencode

register = Library()

def get_from_dict(value, arg):
	"""
	Returns value[arg] or None.
	"""
	try:
		result = value[arg]
	except:
		result = None
	return result


register.filter('get_from_dict', get_from_dict)
