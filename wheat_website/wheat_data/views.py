from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from wheat_data import models
from wheat_data import wheat_forms
from wheat_data.wheat_util import Trial_x_Location_x_Year
from math import pi, sin, cos, asin, atan2, degrees, radians
import datetime

# Create your views here.
def select_location(request):
	if request.method == 'POST':
		form = wheat_forms.SelectLocationForm(request.POST)
		if form.is_valid():
			zipcode = models.Zipcode.objects.filter(zipcode=form.cleaned_data['zipcode'])
			radius = float(form.cleaned_data['search_radius'])
			lat2_list = []
			lon2_list = []
			locations = []
			today = datetime.date.today()
			year_list = [today.year,today.year-1,today.year-2,today.year-3] # Only ever use 3 years of data. But how do we know whether this year's data is in or not?
			try:
				lat1 = float(zipcode.get().latitude) # should only be one result
				lon1 = float(zipcode.get().longitude) # alternatively, we can call zipcode[0].longitude, but this might throw an IndexError
				lat1 = radians(lat1)
				lon1 = radians(lon1)
				R = 6378137.0 # Earth's median radius, in meters
				d = radius * 1609.344	 # in meters 
				# TODO: Search the max distance, then have the user decide what threshold to filter at after _all_ results returned.
				# TODO: have the Location objects grab default lat/long, not user entered
				bearing_list = [ 0.0, pi/2.0, pi, 3.0*pi/2.0 ] # cardinal directions
				for theta in bearing_list:
					lat2 = asin(sin(lat1)*cos(d/R) + cos(lat1)*sin(d/R)*cos(theta))
					lat2_list.append( degrees(lat2) )
					lon2 = lon1 + atan2(sin(theta)*sin(d/R)*cos(lat1), cos(d/R)-sin(lat1)*sin(lat2))
					lon2_list.append( degrees(lon2) )
					lon2 = (lon2+3.0*pi)%(2.0*pi) - pi	# normalise to -180...+180
				lat2_list = lat2_list[0::2] # discard non-moved points
				lon2_list = lon2_list[1::2] # both should contain two values, {min, max} lat/long
				
				locations = models.Location.objects.filter(
						zipcode__latitude__range=(str(min(lat2_list)), str(max(lat2_list)))
					).filter(
						zipcode__longitude__range=(str(min(lon2_list)), str(max(lon2_list)))
					)
				#TODO: We just searched a square, now discard searches that are > x miles away.
			
			except models.Zipcode.DoesNotExist:
				return render_to_response(
					'select_location.html', 
					{ 
						'form': form,
						'error_list': ['Sorry, the zipcode: ' + form.cleaned_data['zipcode'] + ' doesn\'t match any records']
					},
					context_instance=RequestContext(request)
				)
			
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
          
			ranked_entries_list = Trial_x_Location_x_Year(query_set=entries, location_set=locations, year_list=year_list).fetch(n_list=[1,2,3], field_list=[field])

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
					'radius' : radius,
					'lat_list': lat2_list,
					'lon_list': lon2_list
				}
			)
			
	else:
		form = wheat_forms.SelectLocationForm()

	return render_to_response(
		'select_location.html', 
		{ 'form': form },
		context_instance=RequestContext(request)
	)
	return render_to_response('base.html')

def select_variety(request):
	if request.method == 'POST':
		form = wheat_forms.SelectVarietyForm(request.POST)
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
		form = wheat_forms.SelectVarietyForm()

	return render_to_response(
		'select_variety.html', 
		{ 'form': form },
		context_instance=RequestContext(request)
	)
	return render_to_response('base.html')


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
		form = wheat_forms.UploadCSVForm(request.POST, request.FILES)
		if form.is_valid():
			success, errors = wheat_forms.handle_csv_file(request.FILES['csv_file'])
			if success:
				return HttpResponseRedirect('/success/')
			else:
				form = wheat_forms.UploadCSVForm()
	else:	
		form = wheat_forms.UploadCSVForm()

	return render_to_response(
		'add_from_csv_template.html', 
		{'form': form, 'format_errors': errors},
		context_instance=RequestContext(request)
	)
