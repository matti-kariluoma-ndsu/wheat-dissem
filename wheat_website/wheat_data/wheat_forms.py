from django import forms
from wheat_data import models
#import csv

class SelectLocationForm(forms.Form):
  zipcode = forms.CharField(max_length=5)
  search_radius = forms.CharField(max_length=5)
									#forms.ChoiceField(
                   # widget=forms.RadioSelect(), 
                   # choices=(
                    #  (50,'50 miles'), (100,'100 miles'), (200,'200 miles')
                    #  ),
                    #initial='50'
                  #)

class SelectVarietyForm(forms.Form):
	variety = forms.CharField(max_length=20)

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

	insertion_dict = {}
	reference_dict = {}

	skip = True
	skip_lines = 1
	skip_count = 0

	# Inspect our model, to grab the fields from it

	for field in models.Trial_Entry._meta.fields:
		if (field.get_internal_type() == 'ForeignKey' 
				or field.get_internal_type() == 'ManyToManyField' ):
			reference_dict[field.name] = field.rel.to.objects.all()
		else:
			insertion_dict[field.name] = None
				
	#print reference_dict['variety'][0].id
	
	# Now inspect the uploaded file and attempt to write it all to database
	# TODO: Consider not save() -ing each line, maybe do batches of ~100?
	skip = True
	skip_lines = 2
	line_number = 0
	headers = []
	errors = []
	
	for line in uploaded_file:
		line_number += 1
		if (skip):
			if (line_number + 1 > skip_lines):
				headers = str(line).replace('"','').split(',') # assume the headers are the second row
				skip = False
		else:
			column_number = 0
			for column in str(line).split(','):
				try:
					name = headers[column_number].strip()
					if name in insertion_dict.keys():
						insertion_dict[headers[column_number]] = column
					else:
						if name in reference_dict.keys():
							pass
						else:
							errors.append("Heading name \"%s\" not found in database." % name)
				except IndexError:
					errors.append("Found more data columns than there are headings. Line: %d, Column: %d" % (line_number, column_number))
				column_number += 1
			model_instance = models.Trial_Entry()
			for name in insertion_dict.keys():
				setattr(model_instance, name, insertion_dict[name])
			#model_instance.save() # ARE YOU BRAVE ENOUGH?
			
			
	return False, {'file': 'not in csv format', 'variety': 'not an id'}
