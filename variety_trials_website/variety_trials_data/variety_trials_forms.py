from django import forms
from django.core.exceptions import ValidationError
from variety_trials_data import models
from difflib import SequenceMatcher
#import csv

class SelectLocationForm(forms.Form):
	zipcode = forms.CharField(max_length=5)  
	search_radius = forms.ChoiceField(
										widget=forms.RadioSelect(), 
                    choices=(
                      (30,'30 miles'), (60,'60 miles'), (90,'90 miles'), (120,'120 miles')
                      ),
                    initial='50'
                  )
	#search_radius = forms.CharField(max_length=5)

class SelectFieldForm(forms.Form):
	locations = forms.CharField(max_length=5)
	year_list = forms.CharField(max_length=5)
	field = forms.CharField(max_length=5)
	radius = forms.CharField(max_length=5)

class SelectVarietyForm(forms.Form):
	variety = forms.CharField(max_length=20)

class UploadCSVForm(forms.Form):
	csv_file  = forms.FileField()

class fuzzy_spellchecker():
	""" Uses an internal dictionary to check whether a word has a close 
	match or not.	"""
	_words = {}
	
	def __init__(self):
		pass
		
	def __init__(self, word_dict):
		self.set_dictionary(word_dict)
		
	def set_dictionary(self, word_dict):
		self._words = word_dict
		
	def check(self, field, word):
		"""
		Returns either the closest matched word or None in the specified field
		"""
		try:
			self._words[field]
		except KeyError:
			return None
		
		corrected = None
		ratios = {}
		
		for entry in self._words[field]:
			name = str(entry)
			if isinstance(entry, models.Date):
				date = str(forms.DateField().clean(word))# raises a ValidationError
				if  date == name: 
					corrected = name
					break
				#else:
					#m = SequenceMatcher(None, date, name)
					#ratios[name] = m.ratio()
					#print "%s ? %s: %f" % (word, name, m.ratio())
			else:
				if word == name:
					corrected = name
					break
				elif word.lower() == name.lower():
					corrected = name
					break					
				else:
					m = SequenceMatcher(None, word, name)
					ratios[name] = m.ratio()
					#print "%s ? %s: %f" % (word, name, m.ratio())
				
		if corrected is None:
			smax = 0.0
			for key in ratios.keys():
				if ratios[key] > smax:
					smax = ratios[key]
					corrected = key
		
		return corrected

def handle_reference_field(reference_dict, field, data):
	"""
	Given a spellchecker, a dictionary of possible reference values, a 
	requested field to populate, and the data to populate with, find/create
	the field and returns it's id to populate the reference field with.
	"""
	try:
		reference_dict[field]
	except KeyError:
		return None
	
	speller = fuzzy_spellchecker(reference_dict)
	word = speller.check(field, data)
	return_id = None
	
	## TODO: Ask user if the match is good, and whether or not to use an existing/make a new entry
	
	if word is None: # create a new object and save it to the db
		print "make new %s called %s" % (field, data)
		try:
			if isinstance(reference_dict[field][0], models.Date):
				print str(forms.DateField().clean(data)) # raises a ValidationError
		except IndexError:
			pass
	else: # lookup the existing object 
		for entry in reference_dict[field]: # if field isn't None, then it's a key
			if word == str(entry):
				return_id = entry.id
				print "found a match for %s: %s, %d" % (data, word, return_id)
				break
		
	return return_id

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
len_alphabet = len(alphabet)
def letter(number):
	j = int(number / (len_alphabet - 1)) - 1
	
	if j >= len_alphabet:
		column_letter = str(number) # just bail if we get in trouble
	elif j >= 0:
		column_letter = "%s%s" % (alphabet[j % len_alphabet], alphabet[number % len_alphabet])
	else:
		column_letter = "%s" % (alphabet[number % len_alphabet])
	return column_letter

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
			reference_dict["%s_id" % (field.name)] = field.rel.to.objects.all()
		else:
			insertion_dict[field.name] = None
				
	#print reference_dict['variety'][0].id
	
	# Now inspect the uploaded file and attempt to write it all to database
	# TODO: Consider not save() -ing each line, maybe do batches of ~100?
	skip = True
	skip_lines = 2
	line_number = 0
	headers = []
	errors = {}
	
	
	for line in uploaded_file:
		line_number += 1
		if (skip):
			if (line_number + 1 > skip_lines):
				headers = str(line).replace('"','').split(',') # assume the headers are the second row
				skip = False
		else:
			column_number = 0
			for column in str(line).replace('"','').split(','):
				try:
					name = headers[column_number].strip()
					if name in insertion_dict.keys():
						insertion_dict[name] = column.strip()
					else:
						if name in reference_dict.keys():
							try:
								insertion_dict[name] = handle_reference_field(reference_dict, name, column.strip())
							except ValidationError:
								errors['Bad Date'] = "Couldn't read a badly formatted date on Row: %d, Column: %s: \"%s\"" % (line_number, letter(column_number), column.strip())
						else:
							errors['Malformed CSV File'] = "Heading name \"%s\" not found in database." % name
				except IndexError:
					errors['Extra Data'] = "Found more data columns than there are headings. Row: %d, Column: %s" % (line_number, letter(column_number))
				column_number += 1
			model_instance = models.Trial_Entry()
			for name in insertion_dict.keys():
				setattr(model_instance, name, insertion_dict[name])
			#model_instance.save() # ARE YOU BRAVE ENOUGH?
			
	return (False, errors)