from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from wheat_data import models
from wheat_data import wheat_forms
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
			year_list = [today.year,today.year-1,today.year-2,today.year-3] # maybe set this to date.current.year - 3?
			try:
				lat1 = float(zipcode.get().latitude) # should only be one result
				lon1 = float(zipcode.get().longitude) # alternatively, we can call zipcode[0].longitude, but this might throw an IndexError
				lat1 = radians(lat1)
				lon1 = radians(lon1)
				R = 6378137.0 # Earth's median radius, in meters
				d = radius * 1609.344	 # in meters 
				# TODO: Search the max distance, then have the user decide what threshold to filter at after _all_ results returned.
				bearing_list = [ 0.0, pi/2.0, pi, 3.0*pi/2.0 ] # cardinal directions
				for theta in bearing_list:
					lat2 = asin(sin(lat1)*cos(d/R) + cos(lat1)*sin(d/R)*cos(theta))
					lat2_list.append( degrees(lat2) )
					lon2 = lon1 + atan2(sin(theta)*sin(d/R)*cos(lat1), cos(d/R)-sin(lat1)*sin(lat2))
					lon2_list.append( degrees(lon2) )
					lon2 = (lon2+3.0*pi)%(2.0*pi) - pi	# normalise to -180...+180
				lat2_list = lat2_list[0::2] # discard non-moved points
				lon2_list = lon2_list[1::2] # both should contain two values, {min, max} lat/long
				# locations = models.Location.objects.filter( # TODO: have the Location objects grab default lat/long
				locations = models.Location.objects.filter(
						zipcode__latitude__gte=str(lat2_list[1])
					).exclude(
						zipcode__latitude__gt=str(lat2_list[0])
					).filter(
						zipcode__longitude__gte=str(lon2_list[1])
					).exclude(
						zipcode__longitude__gte=str(lon2_list[0])
					) # doesn't work 100% due to +/- of lat,long numbers...
				#We just searched a square, now discard searches that are > x miles away.
			except models.Zipcode.DoesNotExist:
				return render_to_response(
					'select_location.html', 
					{ 
						'form': form,
						'error_list': ['Sorry, the zipcode: ' + form.cleaned_data['zipcode'] + ' doesn\'t match any records']
					},
					context_instance=RequestContext(request)
				)
				
			entries = [] # this will end up being a 2-dimensional array
			# TODO: Do not make n=4 queries...
			for i in year_list: 
				entries.append(models.Trial_Entry.objects.filter(
					location=locations
				 ).filter(
					harvest_date__in=models.Date.objects.filter(date__year=i)
				 ))
			
			#TODO: At this point, we may want to consider forking the above 
			# code into a script-enabled version, and have the client sort the
			# data.
			
			#Sort the entries 
			entries_dict = {} # a dictionary; keys are the variety names, value is a list of Trial_Entry objects
			for entries_by_year in entries:
				for entry in entries_by_year:
					if entry.variety.name in entries_dict:
						entries_dict[entry.variety.name].append(entry)
					else:
						entries_dict[entry.variety.name] = [entry]
			
			
			sorted_entries = [] # a list of tuples, (TrialEntry, sum of all data)
			#for name in entries_dict.keys():
				#sum = 0.0
				#for entry in entries_dict[name]:
					#sum += 1.0
				#sorted_entries.append((entries_dict[name],))
				
			#TODO: Use HttpResponseRedirect(), somehow passing the variables, so that the user can use the back-button
			# hmm... the back-button works, but it's not obvious it will based on the address bar
			# I'd still like this all to use the address bar to pass the user input
			
			#TODO: I count 5+n queries being made above. Reduce!
			
			return render_to_response(
				'view_location.html',
				{ 
					'location_list': locations,
					'trialentry_list': entries,
					'trialentry_dict': sorted_entries,
					'year_list': year_list,
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
