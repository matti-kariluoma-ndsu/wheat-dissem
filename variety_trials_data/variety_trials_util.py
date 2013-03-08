#!/usr/bin/env python
# coding: ascii

from django.core.cache import cache
from variety_trials_data import models
from variety_trials_data.page.Page import Page
from variety_trials_data.variety_trials_forms import ScopeConstants
from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt

class Locations_from_Zipcode_x_Scope:
	"""
	Utility class to return a list of locations located a specified
	distance from a specified point.
	"""
	
	def __init__(self):
		pass
	
	def __init__(self, zipcode, scope):
		"""
		Initializes internal data structures using the input zipcode and
		radius. 
		"""
		return self.populate(zipcode, scope)
	
	def populate(self, zipcode, scope):
		"""
		Calling populate() multiple times is supported, but untested. YMMV.
		"""
		# test if zipcode is a string or float
		try:
			self.zipcode = str(int(float(zipcode)))
		except ValueError:
			self.zipcode = ''
		
		
		if scope in ScopeConstants().get_list():
			self.scope = scope
		else: 
			self.scope = ScopeConstants.near
	
	def fetch(self):
		"""
		Returns a list of locations within the specified search area.
		raises a `models.Zipcode.DoesNotExist'
		"""
		locations = []
			
		if self.scope == ScopeConstants.near:
			locations = models.Location.objects.all() # TODO: only return N locations? is that faster?
		elif self.scope == ScopeConstants.nd:
			locations = models.Location.objects.select_related(
				depth=2).filter(zipcode__in=models.Zipcode.objects.filter(state__iexact="nd"))
		elif self.scope == ScopeConstants.mn:
			locations = models.Location.objects.select_related(
				depth=2).filter(zipcode__in=models.Zipcode.objects.filter(state__iexact="mn"))
		else: # all
			locations = models.Location.objects.all()
		
		try:
			zipcode_query = models.Zipcode.objects.filter(zipcode=self.zipcode)
			zipcode_object = zipcode_query.get() # should only be one result
		except (ValueError, models.Zipcode.DoesNotExist) as instance:
			raise models.Zipcode.DoesNotExist(instance)

		lat1 = float(zipcode_object.latitude) 
		lon1 = float(zipcode_object.longitude) # alternatively, we can call zipcode[0].longitude, but this might throw an IndexError
		
		"""
		From http://www.movable-type.co.uk/scripts/latlong.html
		Haversine formula:
		"""
		distances = {}
		R = 6378137.0 # Earth's median radius, in meters
		for location in locations: 
			lon2 = float(location.zipcode.longitude)
			lat2 = float(location.zipcode.latitude)
			delta_lon = radians(lon2 - lon1)
			delta_lat = radians(lat2 - lat1)
			lon1r = radians(lon1)
			lat1r = radians(lat1)
			lon2r = radians(lon2)
			lat2r = radians(lat2)
			a = sin(delta_lat / 2.0)**2.0 + cos(lat1r)*cos(lat2r)*sin(delta_lon / 2.0)**2.0
			c = 2*atan2(sqrt(a), sqrt(1.0-a))
			d = R * c
			distances[location] = d
		
		# sort by distance from input zipcode
		sorted_list = []
		for d in sorted(distances.values()):
			for location in locations:
				if d == distances[location]:
					sorted_list.append(location)
					break
		"""
		for l in sorted_list:
			print "%f\t%s" %(distances[l], l.name)
		"""
		return sorted_list
		
def get_locations(zipcode, scope=ScopeConstants.near):
	cache_key = '%s%s' % (zipcode, scope)
	# retrieve from cache, if absent, add to cache.
	locations = cache.get(cache_key)
	if locations is None:
		locations = Locations_from_Zipcode_x_Scope(zipcode, scope).fetch()
		cache.set(cache_key, locations, 300) # expires in 300 seconds (5 minutes)
		
	return locations

def get_page(zipcode, scope, curyear, fieldname, year_url_bit, not_locations=[], varieties=[], year_range=3, locations=None):
	page = None
	
	if locations is None:
		# may throw models.Zipcode.DoesNotExist
		locations = get_locations(zipcode, scope)
			
	not_location_objects = models.Location.objects.filter(name__in=not_locations)
	
	for field in models.Trial_Entry._meta.fields:
		if field.name == fieldname:
			break;
	
	lsd_probability = 0.05
	break_into_subtables = False
	
	number_locations = len(locations)
	if len(varieties) == 0:
		break_into_subtables = True
		#if scope != variety_trials_forms.ScopeConstants.all:
		if scope == ScopeConstants.near:
			number_locations = 8 # TODO: hardcoded constant, should be at least based on page width
	
	cache_key = '%s%s%s%s%s%s%s' % (
			[l.pk for l in sorted(locations, key=lambda location: location.pk)], 
			number_locations,
			year_url_bit,
			year_range, 
			lsd_probability, 
			break_into_subtables, 
			sorted(varieties)
		)
	cache_key = cache_key.replace(' ','')
		
	#print cache_key
	page = cache.get(cache_key)
	if page is not None:
		for table in page.data_tables:
			table.set_defaults(curyear, fieldname)
			table.mask_locations(not_location_objects)
	else:
		# may throw LSDProbabilityOutOfRange, TooFewDegreesOfFreedom, NotEnoughDataInYear
		page = Page(
						locations,
						number_locations,
						not_location_objects,
						curyear, 
						year_range, 
						fieldname, 
						lsd_probability, 
						break_into_subtables=break_into_subtables, 
						varieties=varieties
					)
		cache.set(cache_key, page, 300) # expires after 300 seconds (5 minutes)

	return page
