#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django.template import Library
from django.utils.http import urlencode

register = Library()

def get_urlencode(value, arg):
    "Converts the value to a get parameter using django.utils.http.urlencode"
    return '&%s' % (urlencode([(arg, value)]))


register.filter('get_urlencode', get_urlencode)
