from django import forms
from django.forms.formsets import BaseFormSet
from variety_trials_data import models

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
			required=True
		)
	scope = forms.ChoiceField(
			widget=forms.RadioSelect(),
			choices=(
					(ScopeConstants.near,	'Nearby Locations'),
					(ScopeConstants.nd,	'All of ND'),
					(ScopeConstants.mn,	'All of MN'),
					(ScopeConstants.all,	'All Locations')
				),
			initial=ScopeConstants.near
		)
	year = forms.CharField(max_length=4, required=False)
	not_location = forms.MultipleChoiceField(
			required=False,
			choices=[(location.name, location.name) for location in models.Location.objects.all()]
			)
	variety = forms.MultipleChoiceField(
			required=False,
			choices=[(variety.name, variety.name) for variety in models.Variety.objects.all()]
			)
		
class SelectVarietiesForm(SelectLocationByZipcodeForm):
	varieties = forms.ModelMultipleChoiceField(
			widget=forms.Select(),
			queryset=models.Variety.objects.all()
                        )
	varieties_1 = forms.ModelMultipleChoiceField(
			widget=forms.Select(),
			queryset=models.Variety.objects.all()
                        )
	varieties_2 = forms.ModelMultipleChoiceField(
			widget=forms.Select(),
			queryset=models.Variety.objects.all()
                        )
	varieties_3 = forms.ModelMultipleChoiceField(
			widget=forms.Select(),
			queryset=models.Variety.objects.all()
                        )
                        
class SelectLocationsForm(SelectVarietiesForm):
	locations = forms.ModelMultipleChoiceField(
		widget=forms.SelectMultiple(attrs={'size': 20}),
		queryset=models.Location.objects.all()
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
	value = forms.ModelChoiceField(
			queryset = models.Date.objects.all()
		)
	prompt = 'Date'

class SelectLocationForm(forms.Form):
	value = forms.ModelChoiceField(
			queryset = models.Location.objects.all()
		)
	prompt = 'Location'
		
class SelectVarietyForm(forms.Form):
	value = forms.ModelChoiceField(
			queryset = models.Variety.objects.all()
		)
	prompt = 'Variety'
		
def make_model_field_form(name, field):
	class ModelFieldForm(forms.Form):
		pass
	attrs = {
			'value': field,
		}
	custom_class = type(name+"ModelFieldForm", (ModelFieldForm, ), attrs)
	
	return custom_class
