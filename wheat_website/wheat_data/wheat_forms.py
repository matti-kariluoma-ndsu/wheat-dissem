from django import forms
import csv

class SelectLocationForm(forms.Form):
  zipcode = forms.CharField(max_length=5)
  search_radius = forms.ChoiceField(
                    widget=forms.RadioSelect(), 
                    choices=(
                      (50,'50 miles'), (100,'100 miles'), (200,'200 miles')
                      ),
                    initial='50'
                  )

class UploadCSVForm(forms.Form):
    csv_file  = forms.FileField()

def handle_csv_file(uploaded_file):
	#reader = csv.reader(open(uploaded_file), dialect='excel')
	# No good, the uploaded_file is an object, not a file or stream...
	reader = uploaded_file.chunks()
	
	for row in reader:
		print(row)
		
	return False, {'file': 'not in csv format', 'variety': 'not an id'}
