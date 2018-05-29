#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlencode
from django.core.cache import cache
from django.forms.utils import ErrorDict, ErrorList
from variety_trials_website.settings import HOME_URL
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from variety_trials_data.page.Page import NotEnoughDataInYear
from variety_trials_data.page.LSD_util import LSDProbabilityOutOfRange, TooFewDegreesOfFreedom
from variety_trials_data.variety_trials_util import get_page, get_locations
import datetime

ERROR_MESSAGE = "Request failed. Please use the 'back' button in your browser to visit the previous view."

# TODO: does this belong in the DB?
unit_blurbs = {
		'bushels_acre': [
			'Yield', 
			'Bushels per Acre', 
			'The average number of bushels that can be expected from each acre of farmed land.'
			],
		'protein_percent': [
			'Protein', 
			'Percent of Mass',
			'The average percentage of protein usable for baking. 12% or greater is required for export to	many countries.'
			],
		'test_weight': [
			'Test Weight',
			'Pounds per Bushel', 
			'The average weight of each bushel.'
		]
}

def index(request):
	if 'error' in request.GET:
		#zipcode_form = variety_trials_forms.SelectLocationByZipcodeForm(request.GET)
		zipcode_form = variety_trials_forms.SelectLocationByZipcodeForm()
		if zipcode_form._errors is None:
			zipcode_form._errors = ErrorDict()
		errors = zipcode_form._errors['zipcode'] = ErrorList() # errors for field 'zipcode'
		if request.GET['error'] == 'no_zipcode':
			errors.append(u"Please enter your zipcode. The retrieved data are sorted by distance from your zipcode.")
		elif request.GET['error'] == 'bad_zipcode':
			errors.append(u"Sorry, that zipcode didn't match any records.")
	else:
		zipcode_form = variety_trials_forms.SelectLocationByZipcodeForm()
	
	return render(request, 
		'main_ndsu.html', 
		{ 
			'zipcode_form': zipcode_form,
			'home_url': HOME_URL,
		}
	)
	
def about(request):
	
	return render(
		request,
		'about.html', 
		{ 
			'home_url': HOME_URL,
		}
	)
	
def advanced_search(request):
	form = variety_trials_forms.SelectLocationByZipcodeForm()
	
	return render(
		request,
		'advanced_search.html', 
		{ 
			'home_url': HOME_URL,
			'form': form,
			'fieldnames': [field.name for field in models.TrialEntry._meta.fields],
		}
	)

def historical_zipcode_view(request, startyear, fieldname, abtest=None, years=None, year_url_bit=None, locations=None, year_range=3):
	if request.method != 'GET':
		# Redirect to home if they try to POST
		# TODO: what is the behavior of HEAD?
		return HttpResponseRedirect(HOME_URL)
	else:
		zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeForm(request.GET)
		if not zipcode_radius_form.is_valid():
			# TODO: Have this view point to / , and if successful redirect them
			#   to the proper view with the URL filled out
			# OR: Have a zipcode form on the /view/year/field/ page
			return HttpResponseRedirect("%s%s" % (HOME_URL, '/?error=no_zipcode'))
		else:
			zipcode = zipcode_radius_form.cleaned_data['zipcode']
			scope = zipcode_radius_form.cleaned_data['scope']
			not_locations = zipcode_radius_form.cleaned_data['not_location']
			varieties = zipcode_radius_form.cleaned_data['variety']
			yearname = zipcode_radius_form.cleaned_data['year']
			
			hidden_zipcode_form = variety_trials_forms.SelectLocationByZipcodeForm(
				initial={
					'zipcode': zipcode,
					'scope': scope,
					'not_location': not_locations,
					'year': yearname,
					}
				)
			try:
				maxyear = int(startyear)
			except ValueError:
				maxyear = datetime.date.today().year
				
			try:
				curyear = int(yearname)
			except ValueError:
				# TODO: redirect to /view/curyear/field/?... instead
				curyear = maxyear
			
			if curyear > maxyear:
				curyear = maxyear
			
			if year_url_bit is None:
				year_url_bit = startyear
			
			if years is None:
				years = [maxyear - diff for diff in range(year_range)]
			
			try:
				page = get_page(
						zipcode, 
						scope, 
						curyear, 
						fieldname,
						year_url_bit,
						not_locations=not_locations, 
						varieties=varieties, 
						year_range=year_range, 
						locations=locations
					)
			except models.Zipcode.DoesNotExist:
				zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeForm(initial={
						#'radius': zipcode_radius_form.cleaned_data['search_radius'],
					})
				# TODO: repopulate form
				return HttpResponseRedirect("%s%s" % (HOME_URL, '/?error=bad_zipcode'))
			except (LSDProbabilityOutOfRange, TooFewDegreesOfFreedom, NotEnoughDataInYear) as error:
				page = None
				message = " ".join([ERROR_MESSAGE, error.message])
				raise
			except:
				page = None
				message = ERROR_MESSAGE
				raise
					
				
			"""
			import sys
			for table in page.tables:
				for variety, row in table.rows.items():
					sys.stdout.write('['+variety.name+'\n')
					for cell in row:
						sys.stdout.write('\t'+unicode(cell))
					sys.stdout.write(']\n')
				print table.columns
			#"""
			response = None
			if page is not None:
				try:
					response = render(
						request,
						'tabbed_view_table_ndsu.html',
						{
							'home_url': HOME_URL,
							'hidden_zipcode_form': hidden_zipcode_form,
							'zipcode_get_string': '?%s' % (urlencode( [('zipcode', zipcode)] )),
							'zipcode': zipcode,
							'scope_get_string': '&%s' % (urlencode( [('scope', scope)] )),
							'scope': scope,
							'not_location_get_string': '&%s' % (urlencode([('not_location', l) for l in not_locations])),
							'not_locations': not_locations,
							'variety_get_string': '&%s' % (urlencode([('variety', v) for v in varieties])),
							'varieties': varieties,
							'year_get_string': '&%s' % (urlencode( [('year', curyear)] )),
							'year_url_bit': year_url_bit,
							'curyear': curyear,
							'maxyear': maxyear,
							'page': page,
							'message': None,
							'years': years,
							'blurbs' : unit_blurbs,
							'curfield' : fieldname,
							'show_appendix_tables': False,
						}
					)
				except: # We have no expected exceptions for this code block
					page = None
					message = ERROR_MESSAGE
					#raise
			
			if response is None:
				response = render(
						request,
						'tabbed_view_table_ndsu.html',
						{
							'home_url': HOME_URL,
							'hidden_zipcode_form': hidden_zipcode_form,
							'zipcode_get_string': '?%s' % (urlencode( [('zipcode', zipcode)] )),
							'zipcode': zipcode,
							'scope_get_string': '&%s' % (urlencode( [('scope', scope)] )),
							'scope': scope,
							'not_location_get_string': '&%s' % (urlencode([('not_location', l) for l in not_locations])),
							'not_locations': not_locations,
							'variety_get_string': '&%s' % (urlencode([('variety', v) for v in varieties])),
							'varieties': varieties,
							'year_get_string': '&%s' % (urlencode( [('year', curyear)] )),
							'year_url_bit': year_url_bit,
							'curyear': curyear,
							'maxyear': maxyear,
							'page': page,
							'message': message,
							'years': years,
							'blurbs' : unit_blurbs,
							'curfield' : fieldname,
							'show_appendix_tables': False,
						}
					)
			
			# TODO: is python's refcount/garbage collection enough?
			"""
			if page is not None:
				page.clear() # clear references
				page = None
			#"""
				
			return response

def zipcode_view(request, year_range, fieldname, abtest=None):
	if request.method != 'GET':
		# Redirect to home if they try to POST
		# TODO: what is the behavior of HEAD?
		return HttpResponseRedirect(HOME_URL)
	else:
		zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeForm(request.GET)
		if not zipcode_radius_form.is_valid():
			# TODO: Have this view point to / , and if successful redirect them
			#   to the proper view with the URL filled out
			# OR: Have a zipcode form on the /view/year/field/ page
			return HttpResponseRedirect("%s%s" % (HOME_URL, '/?error=no_zipcode'))
		else:
			zipcode = zipcode_radius_form.cleaned_data['zipcode']
			scope = zipcode_radius_form.cleaned_data['scope']
			
			try:
				locations = get_locations(zipcode, scope)
			except models.Zipcode.DoesNotExist:
				zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeForm(initial={
						'scope': scope,
					})
				# TODO: repopulate form
				return HttpResponseRedirect("%s%s" % (HOME_URL, '/?error=bad_zipcode'))
			
			result = 0;
			curyear = datetime.date.today().year
			while result < 1 and curyear > 1900:
				result = models.TrialEntry.objects.filter(
						location__in = locations
					).filter(
							harvest_date__in = models.Date.objects.filter(
								date__range=(
										datetime.date(curyear,1,1),
										datetime.date(curyear,12,31)
									)
							)
					).filter(
						hidden=False
					).count()
				if result < 1: 
					curyear -= 1
				
			try:
				year_range = int(year_range)
			except ValueError:
				year_range = 3
				
			years = [curyear - diff for diff in range(year_range)]
			
			return historical_zipcode_view(
					request, 
					curyear, 
					fieldname, 
					abtest=abtest, 
					years=years, 
					year_url_bit='last_%d_years' % (year_range), 
					locations=locations, 
					year_range=year_range
				)

