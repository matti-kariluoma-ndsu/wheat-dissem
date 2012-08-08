from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.core import serializers
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from variety_trials_data import handle_csv
from variety_trials_data.Page import Page
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from variety_trials_data.variety_trials_util import Locations_from_Zipcode_x_Radius, Filter_by_Field, LSD_Calculator
import datetime
try:
	import simplejson as json # Python 2.5
except ImportError:
	import json # Python 2.6


def index(request, abtest=None):
	zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeForm()
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
	variety=models.Variety.objects.filter(name=variety_name)[0]
	index = variety.id
	name=variety.name
	description_url = variety.description_url
	picture_url=variety.picture_url
	agent_origin=variety.agent_origin
	year_released=variety.year_released
	straw_length=variety.straw_length
	maturity=variety.maturity
	grain_color=variety.grain_color
	beard=variety.beard
	wilt=variety.wilt


	return render_to_response(
		'variety_info.html', 
		{ 
			'index': index,
			'variety_name': variety_name,
			'year_released' : year_released,
			'description_url' : description_url,
			'picture_url' : picture_url,
			'agent_origin' : agent_origin,
			'straw_length' : straw_length,
			'maturity' : maturity,
			'grain_color' : grain_color,
			'beard' : beard,
			# 'diseases' : diseases,
			'wilt' : wilt
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

def zipcode_view(request, yearname, fieldname, abtest=None):
	if request.method == 'GET':
		zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeForm(request.GET)
		if zipcode_radius_form.is_valid():
			zipcode = zipcode_radius_form.cleaned_data['zipcode']
			
			try:
				locations = Locations_from_Zipcode_x_Radius(zipcode).fetch()
			except models.Zipcode.DoesNotExist:
				zipcode_radius_form = variety_trials_forms.SelectLocationByZipcodeRadiusForm(initial={
						#'radius': zipcode_radius_form.cleaned_data['search_radius']
					})
				# TODO: return to main page and show error
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
	
			try:
				curyear = int(yearname)
			except ValueError:
				curyear = datetime.date.today().year
			
			for field in models.Trial_Entry._meta.fields:
				if field.name == fieldname:
					break;
			
			year_range = 3
			
			lsd_probability = 0.05
			
			page = Page(locations[0:8], curyear, year_range, fieldname, lsd_probability, break_into_subtables=True)
			
			"""
			import sys
			for table in page.tables:
				for variety, row in table.rows.items():
					sys.stdout.write('['+variety.name+'\n')
					for cell in row:
						sys.stdout.write('\t'+unicode(cell))
					sys.stdout.write(']\n')
				print table.columns
			"""
			
			return render_to_response(
				'tabbed_object_table_view.html',
				{
					'zipcode_get_string': '?zipcode=',
					'zipcode': zipcode,
					'not_location_get_string': '&not_location=',
					'curyear': curyear,
					'page': page,
					'years': [curyear - diff for diff in range(year_range)],
					'blurbs' : unit_blurbs,
					'curfield' : fieldname,
				},
				context_instance=RequestContext(request)
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
	
def zipcode_near_json(request, zipcode):
	locations = Locations_from_Zipcode_x_Radius(
					zipcode, None
				).fetch()
	response = HttpResponse()
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(locations, stream=response)
	return response
	
def location_json(request, id):
	l = models.Location.objects.filter(pk=id)
	response = HttpResponse()
	needed_fields=(
		'name',
	)
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(l, fields=needed_fields, stream=response)
	return response
	
def variety_json(request, id):
	v = models.Variety.objects.filter(pk=id)
	response = HttpResponse()
	needed_fields=(
		'name',
	)
	json_serializer = serializers.get_serializer("json")()
	json_serializer.serialize(v, fields=needed_fields, stream=response)
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

def trial_entry_id_json(request, zipcode):
	min_year=2009
	max_year=2011
	list=[]
	try:
		locations = Locations_from_Zipcode_x_Radius(zipcode,"ALL").fetch()
	except models.Zipcode.DoesNotExist:
		locations=models.Location.objects.all()
	
	d=models.Trial_Entry.objects.select_related(depth=3).filter(
				location__in=locations
			).filter(
				harvest_date__in=models.Date.objects.filter(
					date__range=(datetime.date(min_year,1,1), datetime.date(max_year,12,31))
				)
			)
	for trial in d:
		list.append(trial.pk)
			
			

	response = HttpResponse()
	# json_serializer = serializers.get_serializer("json")()
	json.dump(list, response)
	return response

