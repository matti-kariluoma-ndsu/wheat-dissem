from django import forms
from wheat_data import models
#import csv

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
	"""
	reader = uploaded_file.chunks()
	
	for row in reader:
		print("!!!"+row+"!!!")
	"""

	insertion_list = []

	skip = True
	skip_lines = 1
	skip_count = 0

	# Inspect our model, to grab the fields from it

	for field in models.Trial_Entry._meta.fields:
		if (skip):
			if (skip_count+1 >= skip_lines):
				skip = False
			else:
				skip_count += 1
		else:
			if (field.get_internal_type() == 'ForeignKey' 
					or field.get_internal_type() == 'ManyToManyField' ):
				#print ("Skipping reference field")
				pass
			else:
				#print(field.name)
				insertion_list.append([field.name, None])

	#Now inspect the uploaded file and attempt to write it all to database
	# TODO: Consider not save() -ing each line, maybe do batches of ~100?
	skip = True
	skip_lines = 2
	skip_count = 0
	
	for line in uploaded_file:
		if (skip):
			if (skip_count+1 >= skip_lines):
				skip = False
			else:
				skip_count += 1
		else:
			#print("!!!"+line+"!!!")
			insert_pos = 0
			for column in str(line).split(','):
				insertion_list[insert_pos][1] = column
				insert_pos += 1
			model_instance = models.Trial_Entry()
			for name_value_list in insertion_list:
				model_instance.__setattr__(name_value_list[0],name_value_list[1])
			#model_instance.save() # ARE YOU BRAVE ENOUGH?
			
			
	return False, {'file': 'not in csv format', 'variety': 'not an id'}
