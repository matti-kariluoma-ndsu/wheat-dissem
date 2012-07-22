from django import forms
from variety_trials_data import models

class SelectLocationByZipcodeRadiusForm(forms.Form):
	zipcode = forms.CharField(max_length=5, required=True)
		
class SelectVarietiesForm(SelectLocationByZipcodeRadiusForm):
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
