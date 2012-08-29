from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.utils.http import urlencode
from django.core.cache import cache
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from variety_trials_data import handle_csv
from variety_trials_data.Page import Page
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from variety_trials_data.variety_trials_util import LSDProbabilityOutOfRange, TooFewDegreesOfFreedom, NotEnoughDataInYear
from variety_trials_data.variety_trials_util import get_locations
import datetime
try:
	import simplejson as json # Python 2.5
except ImportError:
	import json # Python 2.6

ERROR_MESSAGE = "Request failed. Please use the 'back' button in your browser to visit the previous view."

def index(request, abtest=None):
	zipcode_form = variety_trials_forms.SelectLocationByZipcodeForm()
	
	return render_to_response(
		'main.html', 
		{ 
			'zipcode_form': zipcode_form
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
			'variety': variety,
			'message': message,
		},
		context_instance=RequestContext(request)
	)
	
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
		return HttpResponseRedirect('/')
	else:
		zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeForm(request.GET)
		if not zipcode_radius_form.is_valid():
			# TODO: Have this view point to / , and if successful redirect them
			#   to the proper view with the URL filled out
			# OR: Have a zipcode form on the /view/year/field/ page
			return HttpResponseRedirect('/')
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
					zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeRadiusForm(initial={
							#'radius': zipcode_radius_form.cleaned_data['search_radius'],
						})
					# TODO: return to main page and show error
					return render_to_response(
						'main.html', 
						{
							'zipcode_form': zipcode_form,
							'curyear': datetime.date.today().year,
							'error_list': ['Sorry, the zipcode: "' + zipcode + '" doesn\'t match any records']
						},
						context_instance=RequestContext(request)
					) 
			
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
				
			print cache_key
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
					response = render_to_response(
						'tabbed_object_table_view.html',
						{
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
						},
						context_instance=RequestContext(request)
					)
				except: # We have no expected exceptions for this code block
					page = None
					message = ERROR_MESSAGE
					raise
			
			if response is None:
				response = render_to_response(
						'tabbed_object_table_view.html',
						{
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
		return HttpResponseRedirect('/')
	else:
		zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeForm(request.GET)
		if not zipcode_radius_form.is_valid():
			# TODO: Have this view point to / , and if successful redirect them
			#   to the proper view with the URL filled out
			# OR: Have a zipcode form on the /view/year/field/ page
			return HttpResponseRedirect('/')
		else:
			zipcode = zipcode_radius_form.cleaned_data['zipcode']
			scope = zipcode_radius_form.cleaned_data['scope']
			
			try:
				locations = get_locations(zipcode, scope)
			except models.Zipcode.DoesNotExist:
				zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeRadiusForm(initial={
						'scope': scope,
					})
				# TODO: return to main page and show error
				return render_to_response(
					'main.html', 
					{
						'zipcode_form': zipcode_form,
						'curyear': datetime.date.today().year,
						'error_list': ['Sorry, the zipcode: "' + zipcode + '" doesn\'t match any records']
					},
					context_instance=RequestContext(request)
				)
			
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
	
				
def add_trial_entry_csv_file(request):
	
	errors = {} 
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		form = variety_trials_forms.UploadCSVForm(request.GET, request.FILES)
		if form.is_valid():
			success, errors = handle_csv.checking_for_data(request.FILES['csv_file'])
			if success:
				return HttpResponseRedirect('/success/')
			else:
				form = variety_trials_forms.UploadCSVForm()
	else:	
		form = variety_trials_forms.UploadCSVForm()
	#print errors
	return render_to_response(
		'add_from_csv_template.html', 
		{'form': form, 'format_errors': errors},
		context_instance=RequestContext(request)
	)

def add_form_confirmation(request):
	
	errors = {} 
	givenvalues = {}
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		form = variety_trials_forms.UploadCSVForm(request.GET, request.FILES)
		if form.is_valid():
			success, errors = handle_csv.checking_for_data(request.FILES['csv_file'])
			if not errors:
				return HttpResponseRedirect("/sucess/")
			else:
				form = variety_trials_forms.UploadCSVForm()
				return render_to_response(
					'add_form_confirmation.html', 
					{'form': form, 'format_errors': errors,},
					context_instance=RequestContext(request)
				)
	else:	
		form = variety_trials_forms.UploadCSVForm()
	
def add_information(request):
	
	errors = {}
	givendetail = []
	details = [] 
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		errors = request.POST.getlist("chkError")
		#givendetail = variety_trials_forms.checking_for_data.givenval
		for l in errors:
			split_l = l.split(' ')
			if len(split_l) > 1:
				details.append(split_l[0]+" "+split_l[1]+" "+split_l[2])
				
				
		#print details					
		for detail in details:
			if detail =='Problem with variety' or detail =='Problem with location':
				return render_to_response(
					'add_information.html', 
					{'format_errors': details ,'error_num':errors},
					context_instance=RequestContext(request)
				)
	
def adding_to_database_confirm(request):
	#List for Varieties
	entered_variety_data = []
	description_url = []
	picture_url = []
	agent_origin = []
	year_released = []
	straw_length = []
	maturity = []
	grain_color = [] 
	seed_color = []
	beard = []
	wilt = []
	diseases = []
	susceptibility = []
	#Lists for Location data 
	entered_location_data = []
	extracted_zip = [] 
	errorcheck = []
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
	
		entered_variety_data=request.POST.getlist("varietyname")
		description_url= request.POST.getlist("description_url")
		picture_url=request.POST.getlist("picture_url")
		agent_origin=request.POST.getlist("agent_origin")
		year_released=request.POST.getlist("year_released")
		straw_length=request.POST.getlist("straw_length")
		maturity=request.POST.getlist("maturity")
		grain_color=request.POST.getlist("grain_color")
		seed_color=request.POST.getlist("seed_color")
		beard=request.POST.getlist("beard")
		wilt=request.POST.getlist("wilt")
		diseases=request.POST.getlist("diseases")
		susceptibility=request.POST.getlist("susceptibility")
		entered_location_data=request.POST.getlist("location")
		extracted_zip=request.POST.getlist("zipcode")
		
		
		errorcheck= handle_csv.adding_to_database(entered_variety_data, description_url, picture_url, agent_origin, year_released, straw_length, maturity, grain_color, seed_color, beard, wilt, diseases, susceptibility, entered_location_data, extracted_zip)
		
		return HttpResponseRedirect("/sucess/")

def redirect_sucess(request):

	return render_to_response(
		'success.html'
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
		'masterList':masterList
		}
	)

def debug(request):
	return render_to_response(
		'debug.html',
		{}
		)
def add_variety(request):
	

	return render_to_response(
		'add_v.html'
	)

def add_new_variety(request):
	#List for Varieties
	entered_variety_data = []
	description_url = []
	picture_url = []
	agent_origin = []
	year_released = []
	straw_length = []
	maturity = []
	grain_color = [] 
	seed_color = []
	beard = []
	wilt = []
	diseases = []
	susceptibility = []
	#Lists for Location data 
	entered_location_data = []
	extracted_zip = [] 
	errorcheck = []
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		
		entered_variety_data=request.POST.getlist("varietyname")
		description_url= request.POST.getlist("description_url")
		picture_url=request.POST.getlist("picture_url")
		agent_origin=request.POST.getlist("agent_origin")
		year_released=request.POST.getlist("year_released")
		straw_length=request.POST.getlist("straw_length")
		maturity=request.POST.getlist("maturity")
		grain_color=request.POST.getlist("grain_color")
		seed_color=request.POST.getlist("seed_color")
		beard=request.POST.getlist("beard")
		wilt=request.POST.getlist("wilt")


		
	for l in range(len(entered_variety_data)):
			
		d = models.Variety(
				name=entered_variety_data[l],
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

	return HttpResponseRedirect("/sucess/")
		
def edit_variety(request):
	#List for Varieties
	entered_variety_data = []
	description_url = []
	picture_url = []
	agent_origin = []
	year_released = []
	straw_length = []
	maturity = []
	grain_color = [] 
	seed_color = []
	beard = []
	wilt = []
	id_data=[]

	# a dictionary, keys are strings (source of error), values are strings (message)
	if request.method == 'POST': # If the form has been submitted...
		entered_variety_data=request.POST.getlist("varietyname")
		description_url = models.Variety.objects.all().filter (name=str(entered_variety_data))	
		for element in description_url:
			entered_variety_data = element.name
			id_data = element.id
			description_url = element.description_url
			picture_url = element.picture_url
			agent_origin = element.agent_origin
			year_released = element.year_released
			straw_length = element.straw_length
			maturity = element.maturity
			grain_color = element.grain_color
			seed_color = element.seed_color
			beard = element.beard
			wilt = element. wilt
				
		print description_url		
		return render_to_response(
			'edit_variety.html',
			{
				'id':id_data,
				'entered_variety_data':entered_variety_data.strip( "[,u,],'" ),
				'description_url':str(description_url).strip( "[,u,],'" ),
				'picture_url':str(picture_url).strip( "[,u,],'" ),
				'agent_origin':str(agent_origin).strip( "[,u,],'" ),
				'year_released':str(year_released).strip( "[,u,],'" ),
				'straw_length':str(straw_length).strip( "[,u,],'" ),
				'maturity':str(maturity).strip( "[,u,],'" ),
				'grain_color':str(grain_color).strip( "[,u,],'" ),
				'seed_color':str(seed_color).strip( "[,u,],'" ),
				'beard':str(beard).strip( "[,u,],'" ),
				'wilt':str(wilt).strip( "[,u,],'" ),
			}
			
			)
		
			
				
def edited_variety(request):
	
	#List for Varieties
	entered_variety_data = []
	description_url = []
	picture_url = []
	agent_origin = []
	year_released = []
	straw_length = []
	maturity = []
	grain_color = [] 
	seed_color = []
	beard = []
	wilt = []

	
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		varieties = models.Variety.objects.all().filter (name=str(entered_variety_data))	
		
		entered_variety_data=request.POST.getlist("varietyname")
		description_url= request.POST.getlist("description_url")
		picture_url=request.POST.getlist("picture_url")
		agent_origin=request.POST.getlist("agent_origin")
		year_released=request.POST.getlist("year_released")
		straw_length=request.POST.getlist("straw_length")
		maturity=request.POST.getlist("maturity")
		grain_color=request.POST.getlist("grain_color")
		seed_color=request.POST.getlist("seed_color")
		beard=request.POST.getlist("beard")
		wilt=request.POST.getlist("wilt")

	
		
	for l in range(len(entered_variety_data)):
			
		for variety in varieties:
				variety.name=entered_variety_data[l]
				variety.description_url = description_url[l]
				variety.agent_origin=agent_origin[l]
				variety.year_released=year_released[l]
				variety.straw_length=straw_length[l]
				variety.maturity=maturity[l][l]
				variety.grain_color=grain_color[l]
				variety.seed_color=seed_color[l]
				variety.beard=beard[l]
				variety.wilt=wilt[l]
			 	variety.save()
				
		

	return HttpResponseRedirect("/sucess/")
							
def redirect_sucess(request):

	return render_to_response(
		'success.html'
	)
		    


