from django import forms

class SelectLocationForm(forms.Form):
  zipcode = forms.CharField(max_length=5)
