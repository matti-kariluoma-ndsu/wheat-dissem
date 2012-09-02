from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.cache import cache
from variety_trials_website.settings import HOME_URL
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from variety_trials_data import handle_csv
import random
import time
try:
	import simplejson as json # Python 2.5
except ImportError:
	import json # Python 2.6
	
def history(request):	
	history=models.Trial_Entry_History.objects.all()

	return render_to_response(
		'history.html', 
		{ 
			'history': history,
		},
		context_instance=RequestContext(request)
	)
	
def history_delete(request, delete):	
	history=models.Trial_Entry_History.objects.filter(id = delete)
	for element in history:
		trial_Entry=models.Trial_Entry.objects.filter(id = element.trial_entry.id)
		trial_Entry.delete()
	
	return render_to_response(
		'history.html', 
		{ 
			'history': history,
		},
		context_instance=RequestContext(request)
	)

def history_commit(request, id):  
	entries = models.Trial_Entry_History.objects.filter(id = id)
	for entry in entries:
		entry.deletable = False;
		entry.save()

def generate_unique_name():
	username = ''.join([random.choice('abcdef1234567890') for i in range(16)])
	unixtime = str(repr(time.time())).replace('.','')
	while len(unixtime) < 16:
		unixtime = '%s%s' % (unixtime, '0')
	return '%s%s' % (username, unixtime)

def trial_entry_spreadsheet_headers():
	headers = []
	for field in models.Trial_Entry._meta.fields:
		if (field.get_internal_type() == 'ForeignKey' 
				or field.get_internal_type() == 'ManyToManyField' ):
			headers.append(field.name)
		else:
			headers.append(field.name)
	
	ignore_fields = [
			'pk',
			'id',
			'deletable'
		]
	for field in ignore_fields:
		if field in headers:
			headers.remove(field)
	
	return headers

def add_trial_entry_csv_file(request):
	
	if request.method == 'GET':
		try:
			message = request.GET['message']
		except:
			message = None
	
	# create a blank upload form
	username_unique = generate_unique_name()
		
	form = variety_trials_forms.UploadCSVForm(initial={
			'username_unique': username_unique,
		})
	
	# Give the embedded spreadsheet it's column names
	headers = trial_entry_spreadsheet_headers()
	
	return render_to_response(
		'add_from_csv_template.html', 
		{
			'form': form, 
			'headers': headers,
			'message': message,
		},
		context_instance=RequestContext(request)
	)

field_to_form_lookup = {
		models.Trial_Entry.plant_date.field : variety_trials_forms.SelectDateForm,
		models.Trial_Entry.harvest_date.field : variety_trials_forms.SelectDateForm,
		models.Trial_Entry.location.field : variety_trials_forms.SelectLocationForm,
		models.Trial_Entry.variety.field : variety_trials_forms.SelectVarietyForm,
	}

name_to_field_lookup = dict([
		(field.name, field) for field in models.Trial_Entry._meta.fields
	])
	
def add_trial_entry_csv_file_confirm(request):
	message = None
	confirm_forms = []
	invalid_input_forms = []
	headers = []
	username_unique = None
	
	if request.method != 'POST':
		return HttpResponseRedirect(HOME_URL+'/add/trial_entry/')
	else:
		#print request.POST
		try:
			username_unique = request.POST['username_unique']
		except:
			username_unique = None
			message = "There was a problem with your submission. Please try again."
		
		if not username_unique:
			return HttpResponseRedirect(HOME_URL+'/add/trial_entry/?message=%s' % (message))
		
		# If we are visiting this page for the nth time, n > 1
		try:
			trial_entries_json = request.POST['trial_entries_json']
			# convert json representation back to python objects
			trial_entries = json.loads(trial_entries_json)
		except: 
			trial_entries = []
			
		try:
			user_to_confirm_json = request.POST['user_to_confirm_json']
			# convert json representation back to python objects
			user_to_confirm = json.loads(user_to_confirm_json)
		except: 
			user_to_confirm = []
		
		# This is the 1st visit
		if not trial_entries or not user_to_confirm:
			try:
				csv_file = request.FILES['csv_file']
			except:
				csv_file = None
			
			try:
				csv_json = request.POST['csv_json']
			except:
				csv_json = None
				
			if not csv_file and not csv_json:			
				message = "The spreadsheet did not upload correctly. Please Try Again."
				return HttpResponseRedirect(HOME_URL+'/add/trial_entry/?message=%s' % (message))
			else:
				# preprocess the user's initial input
				if csv_file:
					(headers, trial_entries, user_to_confirm) = handle_csv.handle_file(csv_file, username_unique, name_to_field_lookup)
				elif csv_json:
					(headers, trial_entries, user_to_confirm) = handle_csv.handle_json(csv_json, username_unique, name_to_field_lookup)
				else:
					headers = []
					trial_entries = []
					user_to_confirm = []
		else: # Check for user corrections and validate them
			for (index, (row_number, fieldname, user_input)) in enumerate(user_to_confirm):
				row_number += 1 # for user sanity
				try:
					field = name_to_field_lookup[fieldname]
				except:
					field = None
				if field:
					if field in field_to_form_lookup:
						newform = field_to_form_lookup[field](
										request.POST, prefix=str(index)
									)
						if newform.is_valid():					
							confirm_forms.append(
									(row_number, user_input, newform)
								)
					else:
						newform = variety_trials_forms.make_model_field_form(str(fieldname), field.formfield())(
								request.POST, prefix=str(index)
							)
						if newform.is_valid():
							invalid_input_forms.append(
									(row_number, user_input, newform)
								)
			# write records to database
			pass
		# Done processing POST
		
	if not trial_entries or not user_to_confirm:
		#TODO: this is the case if a user does not fill out an entire row
		message = "Encountered a non-recoverable error during processing. Please try again."
		return HttpResponseRedirect(HOME_URL+'/add/trial_entry/?message=%s' % (message))
	
	if not confirm_forms and not invalid_input_forms:
		#http://collingrady.wordpress.com/2008/02/18/editing-multiple-objects-in-django-with-newforms/
		for (index, (row_number, fieldname, user_input)) in enumerate(user_to_confirm):
			row_number += 1 # for user sanity
			try:
				field = name_to_field_lookup[fieldname]
			except:
				field = None
			if field:
				if field in field_to_form_lookup:
					newform = field_to_form_lookup[field](
									prefix=str(index)
								)
					confirm_forms.append(
							(row_number, user_input, newform)
						)
				else:
					newform = variety_trials_forms.make_model_field_form(str(fieldname), field.formfield())(
							prefix=str(index)
						)
					invalid_input_forms.append(
							(row_number, user_input, newform)
						)
	
		
	return render_to_response(
		'add_from_csv_confirm.html', 
		{
			'confirm_forms': confirm_forms,
			'invalid_input_forms': invalid_input_forms,
			'username_unique': username_unique,
			'trial_entries': trial_entries,
			'trial_entries_json': json.dumps(trial_entries),
			'user_to_confirm': user_to_confirm,
			'user_to_confirm_json': json.dumps(user_to_confirm),
			'headers': headers,
			'message': message,
		},
		context_instance=RequestContext(request)
	)

def add_variety(request):
	

	return render_to_response(
		'add_v.html'
	)
