from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from variety_trials_data.variety_trials_util import Locations_from_Zipcode_x_Radius, Filter_by_Field, LSD_Calculator
import datetime

def get_entries(locations, year_list):
	# We do a depth=2 so we can access entry.variety.name
	# We do a depth=3 so we can access entry.harvest_date.date.year
	#TODO: Somehow reduce this to depth=1
	return models.Trial_Entry.objects.select_related(depth=3).filter(
				location__in=locations
			).filter(
				harvest_date__in=models.Date.objects.filter(
					date__range=(datetime.date(min(year_list),1,1), datetime.date(max(year_list),12,31))
				)
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
	
	# TODO: respect/update the cur_year value.
	try:
		sorted_list = LSD_Calculator(get_entries(locations, year_list), locations, varieties, year_list, curyear, field).fetch(reduce_to_one_subset=one_subset)
	except TypeError:
		# TODO: we can do more for the user than redirect to /
		return HttpResponseRedirect("/")
	
	# New idea, return a list of tables instead of a list of rows
	tables = []
	header_rows = [sorted_list[0]]
	lsd_rows = []
	rows = []
	i = 0;
			
	for row in sorted_list[1::]:
		if len(row) > 0:
			if row[0][0] == 'Variety':
				tables.append(rows)
				rows = []
				header_rows.append(row)
			elif row[0] == 'LSD':
				lsd_rows.append(row)
			else:
				rows.append(row)
				
	tables.append(rows)

	dict_tables = []
	for h in header_rows:
		dict_tables.append(dict(header=h))
	for l, i in zip(lsd_rows, range(len(lsd_rows))):
		dict_tables[i]['lsd'] = l
	for r, i in zip(tables, range(len(tables))):
		dict_tables[i]['rows'] = r
	
	for table in dict_tables:
		order = table['header'][0][1][0]
		#print order
		table['order'] = tuple((order[0], order[0]+order[1], order[0]+order[1]+order[2]))
		table['header'][0] = ('Variety', -1)
	
	remove_incomplete_tables = True
	# remove tables that are incomplete
	if remove_incomplete_tables:
		keep_me = []
		for table in dict_tables:
			full = True
			for row in table['rows']:
				if None in row:
					full = False
			if full:
				keep_me.append(table)
		dict_tables = keep_me
	'''
	for table in dict_tables:
		print table['header']
		for row in table['rows']:
			print row
		print table['lsd']
		print ''
	'''
	
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
	
	# turn the headers from a list of names to a tuple of (location_name, location_id)
	heading_list = []
	
	#TODO: this is very bad for the database...
	try:
		pass
		#curyear = sorted_list[0][0] # we sent a preference for curyear, but what was returned may be different
	except IndexError: # will happen if all locations have been deselected...
		sorted_list = [[curyear]]
		return HttpResponseRedirect("/")
	
	if one_subset: # the variety view
		view = 'variety'
	directHome=0
	for l in sorted_list[1::]:
		if l[1]==l[2]==l[3]==None:
			directHome=1
		else:
			directHome=0
			break
	if directHome==1:
		return HttpResponseRedirect("/")
		
		#iterate through sorted list and send the user to the home page if it's all empty
	else: # the location view
		view = 'location'
	location_get_string=''
	variety_get_string=''
	for v in varieties:
		variety_get_string='&varieties='+str(v.id)
	for l in locations:
		location_get_string='&locations='+str(l.id)
	variety_get_string = '?'+variety_get_string[1::]
	return render_to_response(
		'tabbed_view.html',
		{
			'zipcode': zipcode,
			'search_radius': search_radius,
			'location_get_string': location_get_string,
			'variety_get_string': variety_get_string,
			'locations_form': locations_form,
			'field_list': field_list,
			'location_list': locations,
			'curyear': curyear,
			'heading_list': sorted_list[0][1::],
			'sorted_list': sorted_list[1::],
			'tables': dict_tables,
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
		if varieties_form.is_valid():
			
			varieties = varieties_form.cleaned_data['varieties']
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
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		errors = request.POST.getlist("chkError")
		#givendetail = variety_trials_forms.checking_for_data.givenval
		
		for error in errors:
			if error =='Problem with variety ID' or error =='Problem with location ID':
				return render_to_response(
					'add_information.html', 
					{'format_errors': errors},
					context_instance=RequestContext(request)
				)
			
			
def adding_to_database_confirm(request):
	
	entered_variety_data = []
	entered_location_data = {}
	
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		entered_variety_data.append(request.POST.getlist("varietyname"))
		print entered_variety_data
		
		
		return HttpResponseRedirect("/sucess/")
		

							
def redirect_sucess(request):

	return render_to_response(
		'success.html'
	)
		    

