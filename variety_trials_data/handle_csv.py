from django.core.exceptions import ValidationError
from django.core.cache import cache
from variety_trials_data import models
from difflib import SequenceMatcher
import re
import time
from datetime import date
try:
	import simplejson as json # Python 2.5
except ImportError:
	import json # Python 2.6

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
				#else: # Let's not try to fuzzy-match a date. Just create a new date.
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
		#print "make new %s called %s" % (field, data)
		try:
			if isinstance(reference_dict[field][0], models.Date):
				str(forms.DateField().clean(data)) # raises a ValidationError
		except IndexError:
			pass
	else: # lookup the existing object 
		for entry in reference_dict[field]: # if field isn't None, then it's a key
			if word == str(entry):
				return_id = entry.id
				#print "found a match for '%s', '%s': %d" % (data, word, return_id)
				break
		
	return return_id

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
len_alphabet = len(alphabet)
def column_number_to_letter(number):
	"""
	Transforms an integer into its spreadsheet column name
	i.e. 1: A, 2: B, ..., 27: AA, ..., etc.
	"""
	j = int(number / (len_alphabet - 1)) - 1
	
	if j >= len_alphabet:
		column_letter = str(number) # just bail if we get in trouble
	elif j >= 0:
		column_letter = "%s%s" % (alphabet[j % len_alphabet], alphabet[number % len_alphabet])
	else:
		column_letter = "%s" % (alphabet[number % len_alphabet])
	return column_letter

def process_cell(line_number, column_number, cell, errors, column_name, trial_entry_fields, trial_entry_foreign_fields):
	if column_name:
		if column_name in trial_entry_foreign_fields:
			try:
				trial_entry_fields[column_name] = handle_reference_field(trial_entry_foreign_fields, column_name, cell)
			except ValidationError:
				errors['Bad Cell'] = "Couldn't read the cell at Row: %d, Column: %s: \"%s\"" % (line_number, column_number_to_letter(column_number), cell)
		elif column_name in trial_entry_fields:
			trial_entry_fields[column_name] = cell
		else:
			errors['Malformed CSV File'] = "Heading name \"%s\" not found in database." % name
	
	return errors

def process_row(row, headers, trial_entry_fields, trial_entry_foreign_fields):
	input_data = {}
	if len(row) == len(headers):
		for (index, column_name) in enumerate(headers):
			if row[index]: # we are only dealing with strings
				if column_name in trial_entry_fields:
					field = trial_entry_fields[column_name]
				elif column_name in trial_entry_foreign_fields:
					field = trial_entry_foreign_fields[column_name]
				else:
					field = None
				if field:
					input_data[field] = row[index]
	return input_data
			

def inspect_trial_entry():
	trial_entry_fields = {} # {column name: field, ...}
	trial_entry_foreign_fields = {} # {column name: field, ...}
	
	# Inspect our model, grab its fields
	for field in models.Trial_Entry._meta.fields:
		if (field.get_internal_type() == 'ForeignKey' 
				or field.get_internal_type() == 'ManyToManyField' ):
			trial_entry_foreign_fields["%s_id" % (field.name)] = field
		else:
			trial_entry_fields[field.name] = field

	return (trial_entry_fields, trial_entry_foreign_fields)

def handle_json(uploaded_data, username):
	(trial_entry_fields, trial_entry_foreign_fields) = inspect_trial_entry()
	headers = []
	
	try:
		table = json.loads(uploaded_data)
	except:
		table = []
	
	trial_entries = []
	for line in table:
		if not headers:
			try:
				maybe_headers = list(line)
			except:
				maybe_headers = []
			if not maybe_headers:
				continue	
			for field in maybe_headers:
				if field not in trial_entry_fields and field not in trial_entry_foreign_fields and field:
					headers = []
					continue
				else:
					if field:
						headers.append(field)
		else:
			row = []
			try:
				json_row = list(line)
			except:
				json_row = []

			for cell in json_row:
				cell = cell.replace('"','')
				cell = cell.replace("'",'')
				cell = cell.strip()
				row.append(cell)
				
			fields = process_row(row, headers, trial_entry_fields, trial_entry_foreign_fields)
			
			if fields: # if not empty
				trial_entries.append(fields)
	
	user_to_confirm = []
	which_row = {}
	unsaved_model_instance = models.Trial_Entry()
	for (row_number, trial_entry) in enumerate(trial_entries):
		for field in trial_entry:
			if '%s_id' % field.name in trial_entry_foreign_fields:
				key = (field, trial_entry[field])
				user_to_confirm.append(key)
				try:
					rows = which_row[key]
				except KeyError:
					rows = which_row[key] = []
				rows.append(row_number)
			elif field.name in trial_entry_fields:
				key = None
				try:
					field.clean(trial_entry[field], unsaved_model_instance)
				except ValidationError: # The 'expected' exception if bad input
					key = (field, trial_entry[field])
				except:
					key = (field, trial_entry[field])
					
				if key:
					user_to_confirm.append(key)
					try:
						rows = which_row[key]
					except KeyError:
						rows = which_row[key] = []
					rows.append(row_number)
			else:
				continue

	# remove duplicates
	user_to_confirm = list(set(user_to_confirm))
	
	user_to_confirm_with_row_numbers = []
	for (field, value) in user_to_confirm:
		try:
			row_number = which_row[(field, value)][0]
		except: # KeyError, IndexError
			row_number = None
		user_to_confirm_with_row_numbers.append(row_number, field, value)
		
	
	return (headers, trial_entries, user_to_confirm_with_row_numbers)

def handle_file(uploaded_file, username):
	
	(trial_entry_fields, trial_entry_foreign_fields) = inspect_trial_entry()
	csv_field = re.compile("'(?:[^']|'')*'|[^,]{1,}|^,|,$") # searches for csv fields
	headers = []
	
	trial_entries = []
	for line in uploaded_file:
		if not headers:
			maybe_headers = csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" )))
			for field in maybe_headers:
				if field not in trial_entry_fields and field not in trial_entry_foreign_fields and field:
					headers = []
					break
				else:
					if field:
						headers.append(field)
		else:
			row = []
			csv_row = csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" )))
			for cell in csv_row:
				if cell == ',': # a special case caused by '^,|,$'
					cell = ''
				cell = cell.replace('"','')
				cell = cell.replace("'",'')
				cell = cell.strip()
				row.append(cell)
			fields = process_row(row, headers, trial_entry_fields, trial_entry_foreign_fields)
	
			if fields: # if not empty
				trial_entries.append(fields)
	
	user_to_confirm = []
	unsaved_model_instance = models.Trial_Entry()
	for trial_entry in trial_entries:
		for field in trial_entry:
			if '%s_id' % field.name in trial_entry_foreign_fields:
				user_to_confirm.append((field, trial_entry[field]))
			elif field.name in trial_entry_fields:
				try:
					field.clean(trial_entry[field], unsaved_model_instance)
				except ValidationError: # The 'expected' exception if bad input
					user_to_confirm.append((field, trial_entry[field]))
				except:
					user_to_confirm.append((field, trial_entry[field]))
			else:
				continue

	# remove duplicates
	user_to_confirm = list(set(user_to_confirm))
	
	return (headers, trial_entries, user_to_confirm)
			
def handle_csv_file(uploaded_file):
	
	#reader = csv.reader(open(uploaded_file), dialect='excel')
	# No good, the uploaded_file is an object, not a file or stream...
	"""
	reader = uploaded_file.chunks()
	
	for row in reader:
		print("!!!"+row+"!!!")
	"""

	trial_entry_fields = {} # {column name: value to be written to database}
	trial_entry_foreign_fields = {} # {column name: all possible values currently in database}


	# Inspect our model, to grab the fields from it

	for field in models.Trial_Entry._meta.fields:
		if (field.get_internal_type() == 'ForeignKey' 
				or field.get_internal_type() == 'ManyToManyField' ):
			trial_entry_foreign_fields["%s_id" % (field.name)] = field.rel.to.objects.all()
		else:
			trial_entry_fields[field.name] = None
	
	# Now inspect the uploaded file and attempt to write it all to database
	# TODO: Consider not save() -ing each line, maybe do batches of ~100?
	header_line = 2
	line_number = 0
	headers = []
	errors = {}
	error_extra = 'Extra Data'
	errors[error_extra] = []
	csv_field = re.compile("'(?:[^']|'')*'|[^,]{1,}|^,|,$") # searches for csv fields
	
	for line in uploaded_file:
		line_number += 1
		if line_number < header_line:
			continue
		elif line_number == header_line:
			headers = csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" ))) # assume the headers are the second row
			for i in range(len(headers)):
				headers[i] = headers[i].replace('"','') # remove all double quotes
				headers[i] = headers[i].replace("'",'') # remove all single quotes
			#print headers
		else:
			column_number = 0
			#print line
			#print csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" )))
			for cell in csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" ))):
				if cell == ',': # a special case caused by '^,|,$'
					cell = ''
				cell = cell.replace('"','')
				cell = cell.replace("'",'')
				#print "column: %s" % (column)
				cell = cell.strip()
				
				if cell != '':
					try:
						column_name = headers[column_number].strip()
						#print "field: %s" % (name)
					except IndexError:
						column_name = None
						errors[error_extra].append("Found more data columns than there are headings. Row: %d, Column: %s" % (line_number, column_number_to_letter(column_number)))
					errors = process_cell(line_number, column_number, cell, errors, column_name, trial_entry_fields, trial_entry_foreign_fields)
					
				column_number += 1
				
			model_instance = models.Trial_Entry()
			for column_name in trial_entry_fields:
				setattr(model_instance, column_name, trial_entry_fields[column_name])
				#print "Writing %s as %s" % (name, insertion_dict[column_name])
			model_instance.save() # ARE YOU BRAVE ENOUGH? 
			#models.Trial_Entry_History(trial_entry=model_instance,username="asdasd",created_date = date.today()).save()
			
	return (False, errors)
