from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from wheat_data import models
from wheat_data import wheat_forms
from math import pi, sin, cos, asin, atan2, degrees, radians

# Create your views here.
def select_location(request):
  if request.method == 'POST':
    form = wheat_forms.SelectLocationForm(request.POST)
    if form.is_valid():
      zipcode = models.Zipcode.objects.filter(zipcode=form.cleaned_data['zipcode'])
      lat2_list = []
      lon2_list = []
      locations = []
      try:
        lat1 = float(zipcode.get().latitude) # should only be one result
        lon1 = float(zipcode.get().longitude) # alternatively, we can call zipcode[0].longitude, but this might throw an IndexError
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        R = 6378137.0 # Earths median radius, in meters
        d = 402336.0   # 250 miles, in meters # TODO: Search the max distance, then have the user decided what threshold to filter at after _all_ results returned.
        bearing_list = [ 0.0, pi/2.0, pi, 3.0*pi/2.0 ] # cardinal directions
        for theta in bearing_list:
          lat2 = asin(sin(lat1)*cos(d/R) + cos(lat1)*sin(d/R)*cos(theta))
          lat2_list.append( degrees(lat2) )
          lon2 = lon1 + atan2(sin(theta)*sin(d/R)*cos(lat1), cos(d/R)-sin(lat1)*sin(lat2))
          lon2_list.append( degrees(lon2) )
          lon2 = (lon2+3.0*pi)%(2.0*pi) - pi  # normalise to -180...+180
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
        #We just searched a square, now discard searches that are > 50 miles away.
        #locations = models.Location.objects.filter(zipcode=zipcode)
      except models.Zipcode.DoesNotExist:
        return render_to_response(
          'select_location.html', 
          { 
            'form': form,
            'error_list': ['Sorry, the zipcode: ' + form.cleaned_data['zipcode'] + ' doesn\'t match any records']
          },
          context_instance=RequestContext(request)
        )
      
      #TODO: Use HttpResponseRedirect(), somehow passing the variables, so that the user can use the back-button
      #hmm... the back-button works, but it's not obvious it will based on the address bar
      return render_to_response(
        'view_location.html',
        { 
          'location_list': locations,
          'trialentry_list': models.Trial_Entry.objects.filter(location=locations),
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
