from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import urlencode
from django.core.cache import cache
from django.forms.util import ErrorDict, ErrorList
from variety_trials_website.settings import HOME_URL
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from variety_trials_data.Page import Page
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from variety_trials_data.variety_trials_util import LSDProbabilityOutOfRange, TooFewDegreesOfFreedom, NotEnoughDataInYear
from variety_trials_data.variety_trials_util import get_locations
import datetime

ERROR_MESSAGE = "Request failed. Please use the 'back' button in your browser to visit the previous view."

def index(request):
	if 'error' in request.GET:
		#zipcode_form = variety_trials_forms.SelectLocationByZipcodeForm(request.GET)
		zipcode_form = variety_trials_forms.SelectLocationByZipcodeForm()
		if zipcode_form._errors is None:
			zipcode_form._errors = ErrorDict()
		errors = zipcode_form._errors['zipcode'] = ErrorList() # errors for field 'zipcode'
		if request.GET['error'] == 'no_zipcode':
			errors.append(u"Please enter your zipcode.")
		elif request.GET['error'] == 'bad_zipcode':
			errors.append(u"Sorry, that zipcode didn't match any records.")
	else:
		zipcode_form = variety_trials_forms.SelectLocationByZipcodeForm()
	
	return render_to_response(
		'main_ndsu.html', 
		{ 
			'zipcode_form': zipcode_form,
			'home_url': HOME_URL,
		},
		context_instance=RequestContext(request)
	)
	
def about(request):
	
	return render_to_response(
		'about.html', 
		{ 
			'home_url': HOME_URL,
		},
		context_instance=RequestContext(request)
	)
	
def advanced_search(request):
	form = variety_trials_forms.SelectLocationByZipcodeForm()
	
	return render_to_response(
		'advanced_search.html', 
		{ 
			'home_url': HOME_URL,
			'form': form,
			'fieldnames': [field.name for field in models.Trial_Entry._meta.fields],
		},
		context_instance=RequestContext(request)
	)

def howto_api(request):
	
	return render_to_response(
		'using_api.html', 
		{
			'home_url': HOME_URL,
		},
		context_instance=RequestContext(request)
	)
	
def howto_add_data(request):
	
	return render_to_response(
		'adding_data.html', 
		{ 
			'home_url': HOME_URL,
		},
		context_instance=RequestContext(request)
	)
	
def variety_info(request, variety_name):
	try:
		variety = models.Variety.objects.filter(name=variety_name).get()
		message = None
	except models.Variety.DoesNotExist:
		variety = None
		message = " ".join([
				ERROR_MESSAGE, 
				"Variety '%s' not found." % (variety_name),
				"Try replacing any special characters (spaces, apostrophes, etc.) with '+'.",
				"Variety names are case-sensitive."
			])

	return render_to_response(
		'variety_info.html', 
		{ 
			'home_url': HOME_URL,
			'variety': variety,
			'message': message,
		},
		context_instance=RequestContext(request)
	)

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
			
			if locations is None:
				try:
					locations = get_locations(zipcode, scope)
				except models.Zipcode.DoesNotExist:
					zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeForm(initial={
							#'radius': zipcode_radius_form.cleaned_data['search_radius'],
						})
					# TODO: repopulate form
					return HttpResponseRedirect("%s%s" % (HOME_URL, '/?error=bad_zipcode'))
			
			not_location_objects = models.Location.objects.filter(name__in=not_locations)
			
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
			
			for field in models.Trial_Entry._meta.fields:
				if field.name == fieldname:
					break;
			
			if years is None:
				years = [maxyear - diff for diff in range(year_range)]
			
			lsd_probability = 0.05
			
			break_into_subtables = False
			number_locations = len(locations)
			if len(varieties) == 0:
				break_into_subtables = True
				#if scope != variety_trials_forms.ScopeConstants.all:
				if scope == variety_trials_forms.ScopeConstants.near:
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

				try:
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
				except (LSDProbabilityOutOfRange, TooFewDegreesOfFreedom, NotEnoughDataInYear) as error:
					page = None
					message = " ".join([ERROR_MESSAGE, error.message])
					#raise
				except:
					page = None
					message = ERROR_MESSAGE
					#raise
					
				
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
					response = render_to_response(
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
							'home_url' : HOME_URL,
						},
						context_instance=RequestContext(request)
					)
				except: # We have no expected exceptions for this code block
					page = None
					message = ERROR_MESSAGE
					#raise
			
			if response is None:
				response = render_to_response(
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
							'home_url' : HOME_URL,
						},
						context_instance=RequestContext(request)
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
			while result < 1:
				result = models.Trial_Entry.objects.filter(
						location__in = locations
					).filter(
							harvest_date__in = models.Date.objects.filter(
								date__range=(
										datetime.date(curyear,1,1),
										datetime.date(curyear,12,31)
									)
							)
					).count()
				if result < 1: 
					curyear = curyear - 1
				
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

def inspect(request):
	
	
	cur_year = datetime.date.today().year
	year_list=list()
	min_year = datetime.date.today().year
	date_count=1
	while date_count>0:
		min_year-=1
		date_count=models.Date.objects.filter(date__range=(datetime.date(min_year-1,1,1), datetime.date(min_year,12,31))).count()
		#print str(min_year)+" "+str(date_count)
	for year in range(min_year+1,cur_year):
		year_list.append(year)
	varieties = models.Variety.objects.all().order_by("name")
	locations = models.Location.objects.all().order_by("name")
	
	masterDict=dict()
	for year in year_list:
		masterDict[year]=dict()
		masterDict[year]["header"]=list()
		for l in locations:
			masterDict[year]["header"].append(l.name)
		masterDict[year]["rows"]=dict()
		for v in varieties:
			masterDict[year]["rows"][v.name]=dict()
			for l in locations:
				masterDict[year]["rows"][v.name][l.id]=" "
	
	for entry in models.Trial_Entry.objects.select_related(depth=3).filter(
			harvest_date__in=models.Date.objects.filter(
				date__range=(datetime.date(min(year_list),1,1), datetime.date(max(year_list),12,31))
			)
		):
		masterDict[entry.harvest_date.date.year]["rows"][entry.variety.name][entry.location.id]="X"

	masterList=dict()
	for year in year_list:
		masterList[year]=dict()
		masterList[year]["header"]=masterDict[year]["header"]
		masterList[year]["rows"]=list()
		x=0
		for v in varieties:
			dummy_list=list()
			dummy_list.append(v.name)
			masterList[year]["rows"].append(dummy_list)
			
			for l in locations:
				masterList[year]["rows"][x].append(masterDict[year]["rows"][v.name][l.id])
			x+=1
	return render_to_response(
		'inspect.html',
		{
			'home_url': HOME_URL,
			'masterList':masterList,
		}
	)

def debug(request):
	return render_to_response(
			'debug.html',
			{
				'home_url': HOME_URL,
			}
		)





