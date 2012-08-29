from django import forms
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
		
class SelectFieldForm(forms.Form):
	locations = forms.CharField(max_length=5)
	year_list = forms.CharField(max_length=5)
	field = forms.CharField(max_length=5)
	search_radius = forms.CharField(max_length=5)

class UploadCSVForm(forms.Form):
	csv_file  = forms.FileField()
