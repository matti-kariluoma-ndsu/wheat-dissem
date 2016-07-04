#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django import forms
from django.forms.formsets import BaseFormSet
from . import models
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

class NewLocation(forms.ModelForm):
	class Meta:
		model = models.Location
		fields = ('name', 'zipcode', )

class NewVariety(forms.ModelForm):
	class Meta:
		model = models.Variety
		fields = ('name', )
		# exclude any ForeignKey or ManyToMany fields
		exclude = ('diseases',)

class NewPlantingMethod(forms.ModelForm):
	class Meta:
		model = models.PlantingMethod
		fields = ('planting_methods', )
