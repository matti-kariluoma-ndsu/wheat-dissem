from django import forms

class SelectLocationForm(forms.Form):
  zipcode = forms.CharField(max_length=5)
  search_radius = forms.ChoiceField(
                    widget=forms.RadioSelect(), 
                    choices=(
                      (50,'50 miles'), (100,'100 miles'), (200,'200 miles')
                      ),
                    initial='50'
                  )
