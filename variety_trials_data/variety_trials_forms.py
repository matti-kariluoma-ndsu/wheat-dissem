#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django import forms
from django.forms.formsets import BaseFormSet
from variety_trials_data import models
import datetime

class ScopeConstants:
	near = 'NEAR'
	nd = 'ND'
	mn = 'MN'
	all = 'ALL'
	def get_list(self):
		return [
				self.near, 
				self.nd, 
				self.mn, 
				self.all
			]

class PlantingMethodConstants:
	irrigated_yes = 'IRRIGATED'
	irrigated_no = 'DRYLAND'
	irrigated_either = 'ANY'
	irrigatedOrNot = (
			irrigated_yes,
			irrigated_no,
			irrigated_either
		)
	fungicide_yes = 'FUNGICIDE'
	fungicide_no = 'CONVENTIONAL'
	fungicide_either = 'BOTH'
	fungicideOrNot = (
			fungicide_yes,
			fungicide_no,
			fungicide_either
		)

class SelectLocationByZipcodeForm(forms.Form):
	zipcode = forms.CharField(
			max_length=5, 
			required=True,
			help_text=''
		)
	scope = forms.ChoiceField(
			widget=forms.RadioSelect(),
			choices=(
					(ScopeConstants.near,	'Nearby Locations'),
					(ScopeConstants.nd,	'All of ND'),
					(ScopeConstants.mn,	'All of MN'),
					(ScopeConstants.all,	'All Locations')
				),
			initial=ScopeConstants.near,
			help_text=''
		)
	'''
	planting_method = forms.ChoiceField(
			required=False,
			widget=forms.RadioSelect(),
			choices=(
					(PlantingMethodConstants.all,	'All Planting Methods'),
					(PlantingMethodConstants.dryland,	'Dryland'),
					(PlantingMethodConstants.irrigated,	'Irrigated'),
					(PlantingMethodConstants.no_till,	'No-Till / Fallow'),
				),
			initial=PlantingMethodConstants.all,
			help_text=''
		)
	'''
	year = forms.CharField(
			max_length=4, 
			required=False,
			initial=datetime.date.today().year,
			help_text='Format: "YYYY" Select which year'+"'"+'s results to view.'
		)
	not_location = forms.MultipleChoiceField(
			required=False,
			choices=[(location.name, location.name) for location in models.Location.objects.all()],
			help_text='Select locations to exclude from the query.'
		)
	variety = forms.MultipleChoiceField(
			required=False,
			choices=[(variety.name, variety.name) for variety in models.Variety.objects.all()],
			help_text='Select varieties to compare head-to-head.'
		)

class LocationYearPlantingMethodSurveyForm(forms.Form):
	location_id = forms.CharField(
			required=True,
		)
	year = forms.CharField(
			required=True,
			max_length=4, 
		)
	irrigated = forms.ChoiceField(
			required=True,
			widget=forms.RadioSelect(),
			choices=(
					(PlantingMethodConstants.irrigated_either, "Don't know"),
					(PlantingMethodConstants.irrigated_yes,	'Irrigated'),
					(PlantingMethodConstants.irrigated_no,	'Dryland')
				),
			initial=PlantingMethodConstants.irrigated_either,
			help_text='Were these trials irrigated?'
		)
	fungicide = forms.ChoiceField(
			required=True,
			widget=forms.RadioSelect(),
			choices=(
					(PlantingMethodConstants.fungicide_either, "Don't know"),
					(PlantingMethodConstants.fungicide_yes,	'Fungicide'),
					(PlantingMethodConstants.fungicide_no,	'No fungicide')
				),
			initial=PlantingMethodConstants.fungicide_either,
			help_text='Was fungicide applied to these trials?'
		)
	notes = forms.CharField(
			required=False,
			widget=forms.Textarea(attrs={
					'rows': '3',
					'cols': '40',
				}),
			help_text="Anything else we should note?"
		)
		
class UploadCSVForm(forms.Form):
	csv_file = forms.FileField(
			required=False
		)
	csv_json = forms.CharField(
			required=False,
			widget=forms.Textarea(attrs={
					'style': 'display: none;'
				})
		)
	username_unique = forms.CharField(
			required=False,
			widget=forms.TextInput(attrs={
					'style': 'display: none;'
				})
		)

class SelectDateForm(forms.Form):
	def __init__(self, *args, **kwargs):
		name = None
		if 'name' in kwargs:
			name = kwargs.pop('name')
		super(forms.Form, self).__init__(*args, **kwargs)
		if name:
			self.prompt = name.replace('_', ' ')
			
	value = forms.ModelChoiceField(
			queryset = models.Date.objects.all()
		)
	label = 'Date'

class SelectLocationForm(forms.Form):
	def __init__(self, *args, **kwargs):
		name = None
		if 'name' in kwargs:
			name = kwargs.pop('name')
		super(forms.Form, self).__init__(*args, **kwargs)
		if name:
			self.prompt = name.replace('_', ' ')
			
	value = forms.ModelChoiceField(
			queryset = models.Location.objects.all()
		)
	label = 'Location'
		
class SelectVarietyForm(forms.Form):
	def __init__(self, *args, **kwargs):
		name = None
		if 'name' in kwargs:
			name = kwargs.pop('name')
		super(forms.Form, self).__init__(*args, **kwargs)
		if name:
			self.prompt = name.replace('_', ' ')
			
	value = forms.ModelChoiceField(
			queryset = models.Variety.objects.all()
		)
	label = 'Variety'
		
def make_model_field_form(name, field):
	class ModelFieldForm(forms.Form):
		pass
	attrs = {
			'value': field,
			'prompt': name.replace('_', ' '),
		}
	custom_class = type(name+"ModelFieldForm", (ModelFieldForm, ), attrs)
	
	return custom_class
