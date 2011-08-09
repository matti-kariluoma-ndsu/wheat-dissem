from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from variety_trials_data.variety_trials_util import Trial_x_Location_x_Year, Locations_from_Zipcode_x_Radius, Filter_by_Field
import datetime

def get_entries(locations, year_list):
	return models.Trial_Entry.objects.select_related(depth=3).filter(
				location__in=locations
			).filter(
				harvest_date__in=models.Date.objects.filter(
					date__range=(datetime.date(min(year_list),1,1), datetime.date(max(year_list),12,31))
				)
			)

# Create your views here.
def index(request):
	location_form = variety_trials_forms.SelectLocationForm()

	return render_to_response(
		'main.html', 
		{ 'location_form': location_form },
		context_instance=RequestContext(request)
	)

def tabbed_view(request, fieldname):
	if request.method == 'POST':
		location_form = variety_trials_forms.SelectLocationForm(request.POST)
		if location_form.is_valid():
			zipcode = location_form.cleaned_data['zipcode']
			radius = location_form.cleaned_data['search_radius']
			
			try:
				locations = Locations_from_Zipcode_x_Radius(
					zipcode, radius
				).fetch()
			except models.Zipcode.DoesNotExist:
				return render_to_response(
					'main.html', 
					{ 
						'location_form': location_form,
						'error_list': ['Sorry, the zipcode: ' + location_form.cleaned_data['zipcode'] + ' doesn\'t match any records']
					},
					context_instance=RequestContext(request)
				)
			today = datetime.date.today()
			# Only ever use 3 years of data. But how do we know whether this year's data is in or not?
			year_list = [today.year, today.year-1, today.year-2, today.year-3] 
			
			for field in models.Trial_Entry._meta.fields:
				if field.name == fieldname:
					break;
			print fieldname
			sorted_list = Filter_by_Field(get_entries(locations, year_list), field, year_list).fetch()
			location_form = variety_trials_forms.SelectLocationForm(initial={
					'zipcode': zipcode,
					'search_radius': radius
				})
			
			return render_to_response(
				'tabbed_view.html',
				{ 
					'location_form': location_form,
					'location_list': locations,
					'current_year': sorted_list[0][0],
					'heading_list': sorted_list[0][1::],
					'sorted_list': sorted_list[1::],
					'year_list': year_list,
					'radius' : radius
				},
				context_instance=RequestContext(request)
			)
	else:
		# seems an error occured...
		location_form = variety_trials_forms.SelectLocationForm()

	return render_to_response(
		'main.html', 
		{ 'location_form': location_form },
		context_instance=RequestContext(request)
	)

def select_location(request):
	if request.method == 'POST':
		form = variety_trials_forms.SelectLocationForm(request.POST)
		if form.is_valid():
			try:
				locations = Locations_from_Zipcode_x_Radius(
					form.cleaned_data['zipcode'],
					form.cleaned_data['search_radius']
				).fetch()
			except models.Zipcode.DoesNotExist:
				return render_to_response(
					'select_location.html', 
					{ 
						'form': form,
						'error_list': ['Sorry, the zipcode: ' + form.cleaned_data['zipcode'] + ' doesn\'t match any records']
					},
					context_instance=RequestContext(request)
				)
				
			today = datetime.date.today()
			year_list = [today.year,today.year-1,today.year-2,today.year-3] # Only ever use 3 years of data. But how do we know whether this year's data is in or not?
			#TODO: reduce this to depth=1, we only need harvest_date.date.year for 3 and variety.name for 2
			entries = models.Trial_Entry.objects.select_related(depth=3).filter(
				location__in=locations
			).filter(
				harvest_date__in=models.Date.objects.filter(
					date__range=(datetime.date(min(year_list),1,1), datetime.date(max(year_list),12,31))
				)
			)
			
			# TODO: At this point, we may want to consider forking the above 
			# TODO: code into a script-enabled version, and have the client sort the
			# TODO: data.
			
			for field in models.Trial_Entry._meta.fields:
				if field.name == 'bushels_acre':
					break;
          
			ranked_entries_list = Trial_x_Location_x_Year(trial_set=entries, location_set=locations, year_list=year_list).fetch(n_list=[1,2,3], field_list=[field])

			# TODO: Use HttpResponseRedirect(), somehow passing the variables, so that the user can use the back-button
			# TODO: hmm... the back-button works, but it's not obvious it will based on the address bar
			# TODO: I'd still like this all to use the address bar to pass the user input
			
			# TODO: I count 5+n queries being made above. Reduce!
			
			return render_to_response(
				'view_location.html',
				{ 
					'location_list': locations,
					'trialentry_list': entries,
					'trialentry_ranked_list': ranked_entries_list,
					'year_list': year_list,
					'radius' : form.cleaned_data['search_radius']
				}
			)
			
	else:
		form = variety_trials_forms.SelectLocationForm()

	return render_to_response(
		'select_location.html', 
		{ 'form': form },
		context_instance=RequestContext(request)
	)

def select_variety(request):
	if request.method == 'POST':
		form = variety_trials_forms.SelectVarietyForm(request.POST)
		if form.is_valid():
			variety = models.Variety.objects.filter(name=form.cleaned_data['variety'])
			try:
				variety.get()
			except models.Variety.DoesNotExist:
				return render_to_response(
					'select_variety.html', 
					{ 
						'form': form,
						'error_list': ['Sorry, the variety name: ' + form.cleaned_data['variety'] + ' doesn\'t match any records']
					},
					context_instance=RequestContext(request)
				)
			
			return render_to_response(
				'view_variety.html',
				{ 
					'variety_list' : variety.values()
				}
			)
			
	else:
		form = variety_trials_forms.SelectVarietyForm()

	return render_to_response(
		'select_variety.html', 
		{ 'form': form },
		context_instance=RequestContext(request)
	)

def add_variety(request):
	DiseaseFormset = inlineformset_factory(models.Variety, models.Disease_Entry)
	
	if request.method == 'POST': # If the form has been submitted...
		form = models.VarietyForm(request.POST)
		if form.is_valid():
			new_variety = form.save()
			formset = DiseaseFormset(request.POST, instance=new_variety)
			if formset.is_valid():
				formset.save()
			return HttpResponseRedirect('/variety/')
		else:
			formset = DiseaseFormset(request.POST)
			
	else:
		form = models.VarietyForm()
		formset = DiseaseFormset()

	return render_to_response(
		'add.html', 
		{'form': form, 'formset': formset},
		context_instance=RequestContext(request)
	)

def add_trial_entry(request):
	if request.method == 'POST': # If the form has been submitted...
		form = models.Trial_EntryForm(request.POST)
		if form.is_valid():
			new_variety = form.save()
			return HttpResponseRedirect('/admin/')
	else:
		form = models.Trial_EntryForm()

	return render_to_response(
		'add.html', 
		{'form': form },
		context_instance=RequestContext(request)
	)

def add_trial_entry_csv_file(request):
	
	errors = {} 
	# a dictionary, keys are strings (sources of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		form = variety_trials_forms.UploadCSVForm(request.POST, request.FILES)
		if form.is_valid():
			success, errors = variety_trials_forms.handle_csv_file(request.FILES['csv_file'])
			if success:
				return HttpResponseRedirect('/success/')
			else:
				form = variety_trials_forms.UploadCSVForm()
	else:	
		form = variety_trials_forms.UploadCSVForm()

	return render_to_response(
		'add_from_csv_template.html', 
		{'form': form, 'format_errors': errors},
		context_instance=RequestContext(request)
	)
