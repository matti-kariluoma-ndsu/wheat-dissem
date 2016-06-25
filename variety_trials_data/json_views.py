#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django.core import serializers
from django.http import HttpResponse
from variety_trials_data import models
from variety_trials_data import variety_trials_util
import datetime
try:
	import simplejson as json # Python 2.5
except ImportError:
	import json # Python 2.6
	
# TODO: add cache.get/set calls to these functions?

def json_response(request, iterable_result, needed_fields=None):
	response = HttpResponse()
	if request.method == 'GET':
		try:
			jsonp_callback = request.GET['callback']
		except:
			jsonp_callback = None
			
		if not jsonp_callback:
			try:
				jsonp_callback = request.GET['jsonp']
			except:
				jsonp_callback = None

	if jsonp_callback:
		response.write(jsonp_callback)
		response.write("(")
			
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(
			iterable_result, 
			fields=needed_fields,
			ensure_ascii=False,
			stream=response
		)
		
	if jsonp_callback:
		response.write(")")
		
	return response

def autocomplete_zipcode_json(request, partial_zipcode):
	"""
	if str(partial_zipcode)[0] != 0:
		filter_less_than = 10000
	elif
	""" 
	#TODO: filter properly for zipcodes starting with 0, 00
	#TODO: do any zipcodes start with 000? 0000? does zip 00000 exist? 
	
	z = models.Zipcode.objects.filter(
			zipcode__startswith=partial_zipcode
		).filter(
			zipcode__gt=10000
		)

	return json_response(request, z)

def trial_entry_json(request, id):
	v = models.TrialEntry.objects.filter(pk=id)
	fields = (
		'pk',
		'model',
		'variety',
		'location',
		'name',
		'bushels_acre',
		'protein_percent',
		'test_weight'
		)
	
	return json_response(request, v, needed_fields=fields)
	
def zipcode_json(request, id):
	z = models.Zipcode.objects.filter(pk=id)
	
	return json_response(request, z)
	
def zipcode_near_json(request, zipcode):
	try:
		locations = variety_trials_util.get_locations(zipcode)
	except models.Zipcode.DoesNotExist:
		locations = []

	return json_response(request, locations)
	
def location_json(request, id):
	l = models.Location.objects.filter(pk=id)
	fields=(
		'name',
	)
	return json_response(request, l, needed_fields=fields)
	
def variety_json(request, id):
	v = models.Variety.objects.filter(pk=id)
	fields=(
			'name',
		)
	return json_response(request, v, needed_fields=fields)
	
def disease_json(request, id):
	d = models.Disease_Entry.objects.filter(pk=id)
	
	return json_response(request, d)

def variety_json_all(request):
	varieties = models.Variety.objects.all()
	
	return json_response(request, varieties)

def location_json_all(request):
	locations = models.Location.objects.all()
	
	return json_response(request, locations)

def trial_entry_near_ids_json(request, zipcode):
	min_year=2009
	max_year=2011
	list=[]
	try:
		locations = variety_trials_util.get_locations(zipcode)
	except models.Zipcode.DoesNotExist:
		locations=models.Location.objects.all()
	
	d=models.TrialEntry.objects.select_related(depth=3).filter(
				location__in=locations
			).filter(
				harvest_date__in=models.Date.objects.filter(
					date__range=(datetime.date(min_year,1,1), datetime.date(max_year,12,31))
				)
			).filter(
				hidden=False
			)
	for trial in d:
		list.append(trial.pk)
	
	# TODO: json_response() wasn't flexible enough, so this is copy+pasted. FIX
	response = HttpResponse()
	if request.method == 'GET':
		try:
			jsonp_callback = request.GET['callback']
		except:
			jsonp_callback = None
			
		if not jsonp_callback:
			try:
				jsonp_callback = request.GET['jsonp']
			except:
				jsonp_callback = None

	if jsonp_callback:
		response.write(jsonp_callback)
		response.write("(")
			
	json.dump(list, response)
		
	if jsonp_callback:
		response.write(")")
	
	return response

	
def trial_entry_near_json(request, zipcode):
	#TODO: the logic here should follow views.zipcode_view
	min_year=2009
	max_year=2011
	try:
		locations = variety_trials_util.get_locations(zipcode)
	except models.Zipcode.DoesNotExist:
		locations=models.Location.objects.all()
	
	d=models.TrialEntry.objects.select_related(depth=3).filter(
				location__in=locations[0:8]
			).filter(
				harvest_date__in=models.Date.objects.filter(
					date__range=(datetime.date(min_year,1,1), datetime.date(max_year,12,31))
				)
			).filter(
				hidden=False
			)

	fields = (
		'pk',
		'model',
		'variety',
		'location',
		'name',
		'bushels_acre',
		'protein_percent',
		'test_weight'
		)
	
	
	return json_response(request, d, needed_fields=fields)
