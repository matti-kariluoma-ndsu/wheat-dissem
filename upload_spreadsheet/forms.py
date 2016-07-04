#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django import forms
from variety_trials_data import models # TODO: reduce this cross-module coupling
from variety_trials_data import forms as hrsw_forms
from . import progress
import datetime

class Upload(forms.Form):
	data_json = forms.CharField(
			widget = forms.Textarea,
			required = False,
			help_text = 'data from javascript view',
		)
	data = forms.CharField(
			widget = forms.Textarea,
			required = False,
			help_text = 'data from noscript view',
		)

class VerifyHeaders(forms.Form):
	header_type = forms.ChoiceField(
			choices=[
					(progress.HeaderTypes.Data, '--'),
					(progress.HeaderTypes.Locations, progress.HeaderTypes.Locations),
					(progress.HeaderTypes.Varieties, progress.HeaderTypes.Varieties),
					(progress.HeaderTypes.Measures, progress.HeaderTypes.Measures),
				],
			label='type',
		)

class DateForm(forms.Form):
	now = lambda: datetime.datetime.now().year
	year = forms.ChoiceField(
			choices=[(x, x) for x in [now() + (i-18) for i in range(21)]], 
			label='Which year is this data for?',
		)

class VerifyLocation(forms.Form):
	location = forms.ModelChoiceField(
			models.Location.objects.all(),
			empty_label='Not Listed',
		)
	planting_methods = forms.ModelChoiceField(
			models.PlantingMethod.objects.all(),
			empty_label='Not Listed',
			required=False,
		)
	is_not = forms.BooleanField(
			required=False,
			label='This is not a Location',
		)
	is_stat = forms.BooleanField(
			required=False,
			label='This is a statistical measure',
		)

class VerifyVariety(forms.Form):
	variety = forms.ModelChoiceField(
			models.Variety.objects.all(),
			empty_label='Not Listed',
		)
	is_not = forms.BooleanField(
			required=False,
			label='This is not a Variety',
		)
	is_stat = forms.BooleanField(
			required=False,
			label='This is a statistical measure',
		)

class VerifyMeasure(forms.Form):
	mchoices = [(x, x) for x in models.TrialEntry.measures]
	measure = forms.ChoiceField(choices=mchoices)
	is_not = forms.BooleanField(
			required=False,
			label='This is not a Measure',
		)
	is_stat = forms.BooleanField(
			required=False,
			label='This is a statistical (aggregate) measure',
		)

class VerifyStatistic(forms.Form):
	mchoices = [(x, x) for x in models.TrialEntry.measures]
	measure = forms.ChoiceField(
			choices=mchoices,
			label='This statistic compares',
		)
	schoices = [(x, x) for x in models.SignificanceEntry.methods]
	statistic = forms.ChoiceField(choices=schoices)
	lchoices = [(x, x) for x in models.SignificanceEntry.levels]
	alpha = forms.ChoiceField(
			required=False,
			choices=lchoices,
			label='Alpha level',
		)
	is_not = forms.BooleanField(
			required=False,
			label='These data are not one of the listed statistics',
		)

class AddLocation(hrsw_forms.NewLocation):
	is_not = forms.BooleanField(
			required=False,
			label='This is not a Location',
		)
	is_stat = forms.BooleanField(
			required=False,
			label='This is a statistical measure',
		)

class AddVariety(hrsw_forms.NewVariety):
	is_not = forms.BooleanField(
			required=False,
			label='This is not a Variety',
		)
	is_stat = forms.BooleanField(
			required=False,
			label='This is a statistical measure',
		)

class AddPlantingMethod(hrsw_forms.NewPlantingMethod):
	is_not = forms.BooleanField(
			required=False,
			label='There is not a Planting Method in this name',
		)
	is_stat = forms.BooleanField(
			required=False,
			label='This is a statistical measure',
		)
		
class AddStatistic(Upload):
	is_not = forms.BooleanField(
			required=False,
			label='These data are not one of the listed statistics',
		)
