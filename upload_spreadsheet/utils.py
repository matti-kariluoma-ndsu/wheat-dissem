#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django.utils.text import normalize_newlines
from variety_trials_data import models # TODO: reduce coupling
from fuzzywuzzy import fuzz # pip install fuzzywuzzy
import json

def isfloat(string):
	try:
		_ = float(string)
	except ValueError:
		return False
	except TypeError:
		return False
	return True

def process_upload_form(completed_form):
	data_json = completed_form.cleaned_data['data_json']
	if not data_json:
		data = completed_form.cleaned_data['data']
		data = normalize_newlines(data)
		rows = [
				[item for item in row.split('\t')]
				for row in data.split('\n')
				if any(row.split('\t'))
			]
		data_json = json.dumps({'data': rows})
	try:
		spreadsheet = json.loads(data_json)['data']
	except:
		spreadsheet = None
	if spreadsheet:
		data_present = any([any(row) for row in spreadsheet])
	else:
		data_present = False
	if not data_present:
		return None
	return data_json

def too_similar(names):
	skip_these = []
	for name in names:
		if name in skip_these:
			continue
		for other in names:
			if name == other:
				continue
			ratio = fuzz.partial_ratio(name, other)
			if ratio == 100:
				skip_these.append(other)
	return skip_these

def create_model_cache(models, get_name):
	cache = {}
	for m in models:
		name = get_name(m)
		if name != '':
			name = name[0].lower() + name[1:]
			cache[name] = m
			name = name[0].upper() + name[1:]
		cache[name] = m
	return cache

def create_location_model_cache():
	return create_model_cache(
			models.Location.objects.all(),
			lambda model: model.name,
		)
def create_planting_methods_model_cache():
	return create_model_cache(
			models.PlantingMethod.objects.all(),
			lambda model: model.planting_methods,
		)
def create_variety_model_cache():
	return create_model_cache(
			models.Variety.objects.all(),
			lambda model: model.name,
		)
