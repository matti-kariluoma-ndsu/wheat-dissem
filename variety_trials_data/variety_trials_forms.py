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
