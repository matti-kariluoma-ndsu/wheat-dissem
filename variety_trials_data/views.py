from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.core import serializers
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from variety_trials_data.Page import Page
from variety_trials_data.variety_trials_util import Locations_from_Zipcode_x_Radius, Filter_by_Field, LSD_Calculator
import datetime
try:
	import simplejson as json # Python 2.5
except ImportError:
	import json # Python 2.6


def index(request, abtest=None):
	zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeRadiusForm()
	varieties_form = variety_trials_forms.SelectVarietiesForm()
	variety_list = models.Variety.objects.all()
	curyear = datetime.date.today().year - 1
	

	return render_to_response(
		'main.html', 
		{ 
			'zipcode_radius_form': zipcode_radius_form,
			'varieties_form': varieties_form,
			'variety_list': variety_list,
			'curyear': curyear
		},
		context_instance=RequestContext(request)
	)

def variety_info(request, variety_name):	
	variety=models.Variety.objects.filter(name=variety_name)
	"""
	year_released = variety.values('year_released')[0]['year_released']
	index = variety.values('id')[0]['id']
	name=variety.values('name')[0]['name']
	description_url = variety.values('description_url')[0]['description_url']
	"""
	for v in variety:
		index=v.id
		name=v.name
		year_released=v.year_released
		picture_url=v.picture_url
		
	
	return render_to_response(
		'variety_info.html', 
		{ 
			'index': index,
			'variety_name': name
		},
		context_instance=RequestContext(request)
	)
	
def history(request):	
	history=models.Trial_Entry_History.objects.all()
	newlist = []
	
	for element in history:
		newlist.append(element)
		element.created_date
		element.username

	return render_to_response(
		'history.html', 
		{ 
			'history': history,
			'list' : newlist,
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

def locations_view(request, yearname, fieldname, abtest=None):
	if request.method == 'GET':
		zipcode=request.GET.__getitem__("zipcode")
		locations_form = variety_trials_forms.SelectLocationsForm(request.GET)
		zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeRadiusForm(request.GET)
		if locations_form.is_valid():
			zipcode = locations_form.cleaned_data['zipcode']
			locations = locations_form.cleaned_data['locations']
			varieties = locations_form.cleaned_data['varieties']
			return tabbed_view(request, yearname, fieldname, locations, varieties, False, abtest, zipcode)
		else:
			return zipcode_view(request, yearname, fieldname, abtest)
	else:
		return HttpResponseRedirect("/") # send to homepage

def zipcode_view(request, yearname, fieldname, abtest=None):
	if request.method == 'GET':
		zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeRadiusForm(request.GET)
		if zipcode_radius_form.is_valid():
			zipcode = zipcode_radius_form.cleaned_data['zipcode']
			#radius = zipcode_radius_form.cleaned_data['search_radius']
			radius = None
			
			try:
				locations = Locations_from_Zipcode_x_Radius(
					zipcode, radius
				).fetch()
			except models.Zipcode.DoesNotExist:
				zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeRadiusForm(initial={
						#'radius': zipcode_radius_form.cleaned_data['search_radius']
					})
				return render_to_response(
					'main.html', 
					{
						'zipcode_radius_form': zipcode_radius_form,
						'varieties_form': variety_trials_forms.SelectVarietiesForm(),
						'variety_list': models.Variety.objects.all(),
						'curyear': datetime.date.today().year,
						'error_list': ['Sorry, the zipcode: "' + zipcode + '" doesn\'t match any records']
					},
					context_instance=RequestContext(request)
				) 
			
			#sort locations by distance
			print radius
			
			#TODO: there must be a better way to populate the varieties list
			varieties = []
			
			for entry in models.Trial_Entry.objects.select_related(depth=1).filter(location__in=locations):
				varieties.append(entry.variety)
			
			varieties = list(set(varieties)) # remove duplicates
			
			return tabbed_view(request, yearname, fieldname, locations, varieties, False, abtest, zipcode, radius)
			
		else:
			return HttpResponseRedirect("/") # send to homepage

	else:
		# seems an error occured...
		return HttpResponseRedirect("/") # send to homepage

def tabbed_view(request, yearname, fieldname, locations, varieties, one_subset, abtest=None, zipcode=None, search_radius=None):
	# TODO: does this belong in the DB?
	unit_blurbs = {
			'bushels_acre': ['Yield', 'Bushels per Acre', 
				'The average number of bushels that can be expected from each acre of farmed land.',
				'/static/img/button_yield.jpg','/static/img/button_high_yield.jpg'],
			'protein_percent': ['Protein', 'Percent of Mass',
				'The average percentage of protein usable for baking. 12% or greater is required for export to	many countries.',
				'/static/img/button_protein_percent.jpg', '/static/img/button_high_protein_percent.jpg'],
			'test_weight': ['Test Weight','Pounds per Bushel',
				'The average weight of each bushel.', '/static/img/button_test_weight.jpg',
				'/static/img/button_high_test_weight.jpg']#,
			#'kernel_weight': ['Kernel Weight','Grams per 1000','No Description.',
				#'/static/img/button_kernel_weight.jpg', '/static/img/button_high_kernel_weight.jpg'],
			#'plant_height': ['Plant Height','Inches','No Description.', 
				#'/static/img/button_plant_height.jpg', '/static/img/button_high_plant_height.jpg'],
			#'days_to_head': ['Days to Head','Days from Planting','No Description.',
				#'/static/img/button_days_to_head.jpg', '/static/img/button_high_days_to_head.jpg'],
			#'lodging_factor': ['Lodging Factor','Ranking: 1 (No Lodging) to 9 (Heavy Lodging) ',
				#'No Description.', '/static/img/button_lodging_factor.jpg', '/static/img/button_high_lodging_factor.jpg'],
			#'jday_of_head': ['Julian Day of Head','Days from Jan 1','No Description.',
				#'/static/img/button_jday_of_head.jpg', '/static/img/button_high_jday_of_head.jpg'],
			#'winter_survival_rate': ['Winter Survival Rate','Percentage of Population',
				#'No Description.', '/static/img/button_winter_survival_rate.jpg', '/static/img/button_high_winter_survival_rate.jpg'],
			#'shatter': ['Shatter Factor','Ranking: 1 (Least Shatter) to 9 (Most Shatter)',
				#'No Description.', '/static/img/button_shatter.jpg', '/static/img/button_high_shatter.jpg'],
			#'seeds_per_round': ['Seeds per Round','1000 per Round','No Description.',
				#'/static/img/button_seeds_per_round.jpg', '/static/img/button_high_seeds_per_round.jpg'],
			#'canopy_density': ['Canopy Density Factor','Ranking: 1 (Least Dense) to 9 (Most Dense)',
				#'No Description.', '/static/img/button_canopy_density.jpg', '/static/img/button_high_canopy_density.jpg'],
			#'canopy_height': ['Canopy Height','Inches','No Description.',
				#'/static/img/button_canopy_height.jpg', '/static/img/button_high_canopy_height.jpg'],
			#'days_to_flower': ['Days to Flower','Days from Planting','No Description.',
				#'/static/img/button_days_to_flower.jpg', '/static/img/button_high_days_to_flower.jpg'],
			#'seed_oil_percent': ['Seed Oil','Percent of Mass','No Description.',
				#'/static/img/button_seed_oil_percent.jpg', '/static/img/button_high_seed_oil_percent.jpg'],
			#'seeding_rate': ['Seeding Rate','1000 per Foot','No Description.',
				#'/static/img/button_seeding_rate.jpg', '/static/img/button_high_seeding_rate.jpg'],
			#'moisture_basis': ['Moisture Basis','Ranking: 1 (Dry) to 9 (Flooded)',
				#'No Description.', '/static/img/button_moisture_basis.jpg', '/static/img/button_high_moisture_basis.jpg']
	}
	
	#retrieves the list of locations and finds the locations that have been excluded by the user, storing them in neg_locations
	try:
		pos_locations = Locations_from_Zipcode_x_Radius(
				zipcode, search_radius
			).fetch()
	
	except models.Zipcode.DoesNotExist:
		None
		
	neg_locations=[]
	locations=list(locations)
	for e in pos_locations:
		if locations.count(e)==0:
			neg_locations.append(e)
	
	this_year = datetime.date.today().year - 1

	# Only ever use 3 years of data. But how do we know whether this year's data is in or not?
	year_list = [this_year, this_year-1, this_year-2]
	
	try:
		curyear = int(yearname)
	except ValueError:
		curyear = max(year_list)

	
	field_list = []
	for field in models.Trial_Entry._meta.fields:
		if (field.get_internal_type() == 'DecimalField' 
				or field.get_internal_type() == 'PositiveIntegerField' 
				or field.get_internal_type() == 'SmallIntegerField'
				or field.get_internal_type() == 'IntegerField'):
					# Check for empty queries
					# Raw SQL query... here we go!
					count = 0
					for object in models.Trial_Entry.objects.raw(
							"SELECT id FROM variety_trials_data_trial_entry WHERE %s!='' LIMIT 6", #TODO: hardcoded numeric value
							[field.name]
						):
							if getattr(object, field.name):
								count += 1
					if count > 5:  #TODO: hardcoded numeric value
						field_list.append(field.name)
	
	for field in models.Trial_Entry._meta.fields:
		if field.name == fieldname:
			break;
	
	# Remove all fields from `unit_blurbs' that aren't in `field_list'
	"""
	for name in unit_blurbs.keys():
		if name not in field_list:
			del unit_blurbs[name]
	"""
	
	page = Page(locations[0:8], year_list, curyear, fieldname, 0.05)
	
	locations_form = variety_trials_forms.SelectLocationsForm(initial={
			'locations': locations,
			'varieties': varieties,
			'zipcode': zipcode
		})
	
	try:
		ab = int(abtest)
	except ValueError:
		ab = None
	except TypeError:
		ab = None
	
	if one_subset: # the variety view
		view = 'variety'
	else: # the location view
		view = 'location'
	
	location_get_string=''
	variety_get_string=''
	"""
	for v in varieties:
		variety_get_string='&varieties='+str(v.id)
	for l in locations:
		location_get_string='&locations='+str(l.id)
	variety_get_string = '?'+variety_get_string[1::]
	"""
	return render_to_response(
		'tabbed_object_view.html',
		{
			'zipcode': zipcode,
			'search_radius': search_radius,
			'location_get_string': location_get_string,
			'variety_get_string': variety_get_string,
			'locations_form': locations_form,
			'field_list': field_list,
			'location_list': locations,
			'curyear': curyear,
			'page': page,
			'years': year_list,
			'blurbs' : unit_blurbs,
			'curfield' : fieldname,
			'view': view
		},
		context_instance=RequestContext(request)
	)

def varieties_view(request, yearname, fieldname, abtest=None):

	if request.method == 'GET':
		varieties_form = variety_trials_forms.SelectVarietiesForm(request.GET)
		print request.GET
		if varieties_form.is_valid():
			varieties = []
			varieties.append(varieties_form.cleaned_data['varieties'])
			varieties.append(varieties_form.cleaned_data['varieties1'])
			varieties.append(varieties_form.cleaned_data['varieties2'])
			varieties.append(varieties_form.cleaned_data['varieties3'])
			print '1'
			locations = models.Location.objects.all()
			
			return tabbed_view(request, yearname, fieldname, locations, varieties, True, abtest)
			
		else:
			for field in varieties_form:
				print field.errors
				print field.label_tag
			return HttpResponseRedirect("/") # send to homepage
	else:
		return HttpResponseRedirect("/") # send to homepage
def add_trial_entry_csv_file(request):
	
	errors = {} 
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		form = variety_trials_forms.UploadCSVForm(request.GET, request.FILES)
		if form.is_valid():
			success, errors = variety_trials_forms.checking_for_data(request.FILES['csv_file'])
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
			success, errors = variety_trials_forms.checking_for_data(request.FILES['csv_file'])
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
		
		
		errorcheck= variety_trials_forms.adding_to_database(entered_variety_data, description_url, picture_url, agent_origin, year_released, straw_length, maturity, grain_color, seed_color, beard, wilt, diseases, susceptibility, entered_location_data, extracted_zip)
		
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
		print str(min_year)+" "+str(date_count)
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
	
def trial_entry_json(request, id):
	v = models.Trial_Entry.objects.filter(pk=id)
	response = HttpResponse()
	needed_fields = (
		'pk',
		'model',
		'variety',
		'location',
		'name',
		'bushels_acre',
		'protein_percent',
		'test_weight'
		)
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(v,fields=needed_fields, stream=response)
	
	return response
	
def zipcode_json(request, id):
	z = models.Zipcode.objects.filter(pk=id)
	response = HttpResponse()
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(z, stream=response)
	return response
	
def location_json(request, id):
	l = models.Location.objects.filter(pk=id)
	response = HttpResponse()
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(l, stream=response)
	return response
	
def disease_json(request, id):
	d = models.Disease_Entry.objects.filter(pk=id)
	response = HttpResponse()
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(d, stream=response)
	return response

def variety_json_all(request):
	varieties = models.Variety.objects.all()
	response = HttpResponse()
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(varieties, stream=response)
	return response	

def location_json_all(request):
	locations = models.Location.objects.all()
	response = HttpResponse()
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(locations, stream=response)
	return response		

def debug(request):
	return render_to_response(
		'debug.html',
		{}
		)
