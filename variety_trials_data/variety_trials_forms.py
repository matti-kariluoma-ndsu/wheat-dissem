from django import forms
from django.core.exceptions import ValidationError
from variety_trials_data import models
from difflib import SequenceMatcher
import re
import time
import json
from datetime import date
import glob
import os

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

class SelectFieldForm(forms.Form):
	locations = forms.CharField(max_length=5)
	year_list = forms.CharField(max_length=5)
	field = forms.CharField(max_length=5)
	search_radius = forms.CharField(max_length=5)

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
	
	#l = models.Location(name="some name",zipcode = models.Zipcode(zipcode = "1256",city="some state",state,latitude,longitude,timezone,daylight_savings)
	print "hellow"
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
	csv_field = re.compile("'(?:[^']|'')*'|[^,]{1,}|^,|,$") # searches for csv fields
	
	for line in uploaded_file:
		line_number += 1
		if (skip):
			if (line_number + 1 > skip_lines):
				headers = csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" ))) # assume the headers are the second row
				for i in range(len(headers)):
					headers[i] = headers[i].replace('"','') # remove all double quotes
					headers[i] = headers[i].replace("'",'') # remove all single quotes
				print headers
				skip = False
		else:
			column_number = 0
			print line
			#print csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" )))
			for column in csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" ))):
				if column == ',': # a special case caused by '^,|,$'
					column = ''
				column = column.replace('"','')
				column = column.replace("'",'')
				print "column: %s" % (column)
				
				if column.strip() != '':
					try:
						name = headers[column_number].strip()
						print "field: %s" % (name)
						#Making objects to add to database.
						
						if name == "harvest_date_id":
							possible_characters = ('/', ' ', '-', '.')
							datesplit=re.split("[%s]" % ("".join(possible_characters)), column)
							datelist = models.Date.objects.all().filter (date=date(int(datesplit[2]), int(datesplit[0]),int(datesplit[1])))
							if not datelist:
								d = models.Date(date=date(int(datesplit[2]), int(datesplit[0]),int(datesplit[1])))
								d.save()
						
						if name in insertion_dict.keys() and name not in reference_dict.keys():
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
				print "Writing %s as %s" % (name, insertion_dict[name])
				insertion_dict[name] = None
			model_instance.save() # ARE YOU BRAVE ENOUGH? 
			
			
	return (False, errors)
	
def checking_for_data(uploaded_file):
		
		insertion_dict = {}
		reference_dict = {}
		error_counter = 1
		file_counter = 1
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
	
		skip = True
		skip_lines = 2
		line_number = 0
		headers = []
		errors = {}
		givenval = {}
		csv_field = re.compile("'(?:[^']|'')*'|[^,]{1,}|^,|,$") # searches for csv fields
		
		for line in uploaded_file:
			line_number += 1
			if (skip):
				if (line_number + 1 > skip_lines):
					headers = csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" ))) # assume the headers are the second row
					for i in range(len(headers)):
						headers[i] = headers[i].replace('"','') # remove all double quotes
						headers[i] = headers[i].replace("'",'') # remove all single quotes
					skip = False
			else:
				column_number = 0
				print line
				#print csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" )))
				for column in csv_field.findall(re.sub(',(?=,)', ',""', str(line).replace( '"' , "'" ))):
					if column == ',': # a special case caused by '^,|,$'
						column = ''
					column = column.replace('"','')
					column = column.replace("'",'')
					#print "column: %s" % (column)
					
					if column.strip() != '':
						try:
							name = headers[column_number].strip()
							column = column.strip()
							#Checking for objects on database.
							givenval[name] = (str(column))
							
							if name == "harvest_date_id":
								possible_characters = ('/', ' ', '-', '.')
								datesplit=re.split("[%s]" % ("".join(possible_characters)), column)
								datelist = models.Date.objects.all().filter (date=date(int(datesplit[2]), int(datesplit[0]),int(datesplit[1])))
								if not datelist:
									errors["Problem with harvest %s"%error_counter] = "  Are you sure about the given details? %s"%(column)
									error_counter=error_counter+1
									
							if name == "location_id":
								locationlist = models.Location.objects.all().filter (name=str(column))
								if not locationlist:
									errors["Problem with location %s"%error_counter] = "  Are you sure about the given details? %s"%(column)
									error_counter=error_counter+1
							if name == "variety_id":
								varietylist = models.Variety.objects.all().filter (name=str(column))
								
								if not varietylist:
									errors["Problem with variety %s"%error_counter] = "  Are you sure about the given details? %s"%(column)								
									error_counter=error_counter+1
																		
							if name in insertion_dict.keys() and name not in reference_dict.keys():
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
					
				if not errors:
					model_instance = models.Trial_Entry()
					for name in insertion_dict.keys():
						
						setattr(model_instance, name, insertion_dict[name])
						print "Writing %s as %s" % (name, insertion_dict[name])
						insertion_dict[name] = None
					model_instance.save() # ARE YOU BRAVE ENOUGH? 

				else:
					json.dump(givenval,open(str(file_counter)+".txt",'w'))
					file_counter=file_counter+1
					print givenval
				
		return (False, errors)

def adding_to_database(varietyname, description_url, picture_url, agent_origin, year_released, straw_length, maturity, grain_color, seed_color, beard, wilt, diseases, susceptibility, entered_location_data, extracted_zip):
	numberoffiles=0
	os.chdir("/home/kalith/summerjob/wheat-dissem")
	for files in glob.glob("*.txt"):
		print files
		numberoffiles=numberoffiles+1
	
  #left with calculating the number of files and deleting them in the end.
    
	
	possible_characters = ('/', ' ', '-', '.')
	for h in range(1,numberoffiles):
		k=0
		print h
		f = open(str(h)+".txt", 'r')
		data = json.load(f)
		#saving verified inputs to the database
		for l in range(len(varietyname)):
			#checking onece more!
			varietylist = models.Variety.objects.all().filter (name=varietyname[l])
			#saving the new variety
			if not varietylist:
				d = models.Variety(
					name=varietyname[l],
					description_url = description_url[l]
					,agent_origin=agent_origin[l],
					year_released=year_released[l],
					straw_length=straw_length[l],
					maturity=maturity[l][l],
					grain_color=grain_color[l],
					seed_color=seed_color[l], 
					beard=beard[l],
					wilt=wilt[l]
					  )
				d.save()
		'''
		for i in range(len(entered_location_data)):
			s = models.Location( 
				name = entered_location_data[i][i],
				zipcode = extracted_zip[i][i],
				)
			s.save()
		'''
						
		model_instance = models.Trial_Entry()
		for name in data.keys():
			if name == 'plant_date_id':
				datesplit=re.split("[%s]" % ("".join(possible_characters)), data[name])
				datelist = models.Date.objects.filter (date=date(int(datesplit[2]), int(datesplit[0]),int(datesplit[1])))
				if not datelist:
					ins_d = models.Date(date=date(int(datesplit[2]), int(datesplit[0]),int(datesplit[1])))
					ins_d.save()
				
				datelist = models.Date.objects.filter (date=date(int(datesplit[2]), int(datesplit[0]),int(datesplit[1])))
						
				dateid = 1
				for element in datelist:
					dateid = element.id
				setattr(model_instance, name,dateid)
			elif name == 'harvest_date_id':
				datesplit=re.split("[%s]" % ("".join(possible_characters)), data[name])
				datelist = models.Date.objects.filter (date=date(int(datesplit[2]), int(datesplit[0]),int(datesplit[1])))
			
				forgineid = 1
				for element in datelist:
					forgineid = element.id
				setattr(model_instance, name,forgineid)
			elif name == 'location_id':
				print entered_location_data[k]
				locationlist = models.Zipcode.objects.all().filter (city=str(entered_location_data[k]),zipcode = extracted_zip[k])
				locationid = 1
				for element in locationlist:
					locationid = element.id
				
				print locationid
				setattr(model_instance, name, locationid)
				k=k+1
			elif name == 'variety_id':
				print data[name]
				varietylist = models.Variety.objects.all().filter (name=data[name])
				varietyid = 1
				for element in varietylist:
					varietyid = element.id
				setattr(model_instance, name,varietyid)	
			else:
				setattr(model_instance, name, data[name])
			
			print "Writing %s as %s" % (name, data[name])
			data[name] = None
		model_instance.save() # ARE YOU BRAVE ENOUGH? 
		
		f.close()

	for filetitle in glob.glob("*.txt"):
		 os.remove("/home/kalith/summerjob/wheat-dissem/"+str(filetitle))
		
	
	return(False,data)
