#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.utils import simplejson
from django.template import Library

register = Library()

def jsonify(object, relation):
	if isinstance(object, QuerySet):
		return mark_safe(serialize('json', object, relations=relation))
	return mark_safe(simplejson.dumps(object))

jsonify.is_safe = True
register.filter('jsonify', jsonify)

