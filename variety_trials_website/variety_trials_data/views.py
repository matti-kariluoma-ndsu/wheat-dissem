from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from variety_trials_data.variety_trials_util import Locations_from_Zipcode_x_Radius, Filter_by_Field
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

def index(request):
	location_form = variety_trials_forms.SelectLocationForm()
	varieties_form = variety_trials_forms.SelectVarietiesForm()
	variety_list = models.Variety.objects.all()
	
	return render_to_response(
		'main.html', 
		{ 
			'location_form': location_form,
			'varieties_form': varieties_form,
			'variety_list': variety_list,
			'curyear': datetime.date.today().year 
		},
		context_instance=RequestContext(request)
	)
		
def tabbed_view(request, yearname, fieldname):
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
				'/static/img/button_high_test_weight.jpg'],
			'kernel_weight': ['Kernel Weight','Grams per 1000','No Description.',
				'/static/img/button_kernel_weight.jpg', '/static/img/button_high_kernel_weight.jpg'],
			'plant_height': ['Plant Height','Inches','No Description.', 
				'/static/img/button_plant_height.jpg', '/static/img/button_high_plant_height.jpg'],
			'days_to_head': ['Days to Head','Days from Planting','No Description.',
				'/static/img/button_days_to_head.jpg', '/static/img/button_high_days_to_head.jpg'],
			'lodging_factor': ['Lodging Factor','Ranking: 1 (No Lodging) to 9 (Heavy Lodging) ',
				'No Description.', '/static/img/button_lodging_factor.jpg', '/static/img/button_high_lodging_factor.jpg'],
			'jday_of_head': ['Julian Day of Head','Days from Jan 1','No Description.',
				'/static/img/button_jday_of_head.jpg', '/static/img/button_high_jday_of_head.jpg'],
			'winter_survival_rate': ['Winter Survival Rate','Percentage of Population',
				'No Description.', '/static/img/button_winter_survival_rate.jpg', '/static/img/button_high_winter_survival_rate.jpg'],
			'shatter': ['Shatter Factor','Ranking: 1 (Least Shatter) to 9 (Most Shatter)',
				'No Description.', '/static/img/button_shatter.jpg', '/static/img/button_high_shatter.jpg'],
			'seeds_per_round': ['Seeds per Round','1000 per Round','No Description.',
				'/static/img/button_seeds_per_round.jpg', '/static/img/button_high_seeds_per_round.jpg'],
			'canopy_density': ['Canopy Density Factor','Ranking: 1 (Least Dense) to 9 (Most Dense)',
				'No Description.', '/static/img/button_canopy_density.jpg', '/static/img/button_high_canopy_density.jpg'],
			'canopy_height': ['Canopy Height','Inches','No Description.',
				'/static/img/button_canopy_height.jpg', '/static/img/button_high_canopy_height.jpg'],
			'days_to_flower': ['Days to Flower','Days from Planting','No Description.',
				'/static/img/button_days_to_flower.jpg', '/static/img/button_high_days_to_flower.jpg'],
			'seed_oil_percent': ['Seed Oil','Percent of Mass','No Description.',
				'/static/img/button_seed_oil_percent.jpg', '/static/img/button_high_seed_oil_percent.jpg'],
			'seeding_rate': ['Seeding Rate','1000 per Foot','No Description.',
				'/static/img/button_seeding_rate.jpg', '/static/img/button_high_seeding_rate.jpg'],
			'moisture_basis': ['Moisture Basis','Ranking: 1 (Dry) to 9 (Flooded)',
				'No Description.', '/static/img/button_moisture_basis.jpg', '/static/img/button_high_moisture_basis.jpg']
	}
	
	if request.method == 'POST':
		location_form = variety_trials_forms.SelectLocationForm(request.POST)
		if location_form.is_valid():
			zipcode = location_form.cleaned_data['zipcode']
			radius = location_form.cleaned_data['search_radius']
			
			try:
				locations = Locations_from_Zipcode_x_Radius(
					zipcode, radius
				).fetch()
			except models.Zipcode.DoesNotExist:
				return render_to_response(
					'main.html', 
					{ 
						'location_form': location_form,
						# TODO: set initial fieldname
						'error_list': ['Sorry, the zipcode: ' + location_form.cleaned_data['zipcode'] + ' doesn\'t match any records']
					},
					context_instance=RequestContext(request)
				) 
			
			today = datetime.date.today()
			# Only ever use 3 years of data. But how do we know whether this year's data is in or not?
			year_list = [today.year, today.year-1, today.year-2, today.year-3]
			
			try:
				curyear = int(yearname)
			except ValueError:
				curyear = max(year_list)
				
			years = {}
			for year in year_list:
				years[str(year)] = [
					'/static/img/button_year_%s.jpg' % (str(year)),
					'/static/img/button_high_year_%s.jpg' % (str(year))
					]
				
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
			for name in unit_blurbs.keys():
				if name not in field_list:
					del(unit_blurbs[name])
			
			# TODO: respect/update the cur_year value.
			try:
				sorted_list = Filter_by_Field(get_entries(locations, year_list), field, year_list, curyear, []).fetch()
			except TypeError:
				# TODO: we can do more for the user than redirect to /
				return HttpResponseRedirect("/")
			
			location_form = variety_trials_forms.SelectLocationForm(initial={
					'zipcode': zipcode,
					'search_radius': radius
				})
			
			return render_to_response(
				'tabbed_view.html',
				{ 
					'location_form': location_form,
					'field_list': field_list,
					'location_list': locations,
					'curyear': str(sorted_list[0][0]), # we sent a preference for curyear, but what was returned may be different
					'heading_list': sorted_list[0][1::],
					'sorted_list': sorted_list[1::],
					'years': years,
					'radius' : radius,
					'blurbs' : unit_blurbs,
					'curfield' : fieldname
				},
				context_instance=RequestContext(request)
			)
	else:
		# seems an error occured...
		return HttpResponseRedirect("/") # send to homepage

def varieties_view(request, yearname, fieldname):
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
				'/static/img/button_high_test_weight.jpg'],
			'kernel_weight': ['Kernel Weight','Grams per 1000','No Description.',
				'/static/img/button_kernel_weight.jpg', '/static/img/button_high_kernel_weight.jpg'],
			'plant_height': ['Plant Height','Inches','No Description.', 
				'/static/img/button_plant_height.jpg', '/static/img/button_high_plant_height.jpg'],
			'days_to_head': ['Days to Head','Days from Planting','No Description.',
				'/static/img/button_days_to_head.jpg', '/static/img/button_high_days_to_head.jpg'],
			'lodging_factor': ['Lodging Factor','Ranking: 1 (No Lodging) to 9 (Heavy Lodging) ',
				'No Description.', '/static/img/button_lodging_factor.jpg', '/static/img/button_high_lodging_factor.jpg'],
			'jday_of_head': ['Julian Day of Head','Days from Jan 1','No Description.',
				'/static/img/button_jday_of_head.jpg', '/static/img/button_high_jday_of_head.jpg'],
			'winter_survival_rate': ['Winter Survival Rate','Percentage of Population',
				'No Description.', '/static/img/button_winter_survival_rate.jpg', '/static/img/button_high_winter_survival_rate.jpg'],
			'shatter': ['Shatter Factor','Ranking: 1 (Least Shatter) to 9 (Most Shatter)',
				'No Description.', '/static/img/button_shatter.jpg', '/static/img/button_high_shatter.jpg'],
			'seeds_per_round': ['Seeds per Round','1000 per Round','No Description.',
				'/static/img/button_seeds_per_round.jpg', '/static/img/button_high_seeds_per_round.jpg'],
			'canopy_density': ['Canopy Density Factor','Ranking: 1 (Least Dense) to 9 (Most Dense)',
				'No Description.', '/static/img/button_canopy_density.jpg', '/static/img/button_high_canopy_density.jpg'],
			'canopy_height': ['Canopy Height','Inches','No Description.',
				'/static/img/button_canopy_height.jpg', '/static/img/button_high_canopy_height.jpg'],
			'days_to_flower': ['Days to Flower','Days from Planting','No Description.',
				'/static/img/button_days_to_flower.jpg', '/static/img/button_high_days_to_flower.jpg'],
			'seed_oil_percent': ['Seed Oil','Percent of Mass','No Description.',
				'/static/img/button_seed_oil_percent.jpg', '/static/img/button_high_seed_oil_percent.jpg'],
			'seeding_rate': ['Seeding Rate','1000 per Foot','No Description.',
				'/static/img/button_seeding_rate.jpg', '/static/img/button_high_seeding_rate.jpg'],
			'moisture_basis': ['Moisture Basis','Ranking: 1 (Dry) to 9 (Flooded)',
				'No Description.', '/static/img/button_moisture_basis.jpg', '/static/img/button_high_moisture_basis.jpg']
	}
	
	if request.method == 'POST':
		varieties_form = variety_trials_forms.SelectVarietiesForm(request.POST)
		if varieties_form.is_valid():
			
			varieties = varieties_form.cleaned_data['varieties']
			locations = models.Location.objects.all()
			
			today = datetime.date.today()
			# Only ever use 3 years of data. But how do we know whether this year's data is in or not?
			year_list = [today.year, today.year-1, today.year-2, today.year-3]
			
			try:
				curyear = int(yearname)
			except ValueError:
				curyear = max(year_list)
				
			years = {}
			for year in year_list:
				years[str(year)] = [
					'/static/img/button_year_%s.jpg' % (str(year)),
					'/static/img/button_high_year_%s.jpg' % (str(year))
					]
				
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
			for name in unit_blurbs.keys():
				if name not in field_list:
					del(unit_blurbs[name])
			
			
			variety_list = []
			for variety in varieties:
				variety_list.append(str(variety.name))
				#variety_list.append(variety.name)
				
			
			# TODO: respect/update the cur_year value.
			try:
				sorted_list = Filter_by_Field(get_entries(locations, year_list), field, year_list, curyear, variety_list).fetch()
			except TypeError:
				# TODO: we can do more for the user than redirect to /
				return HttpResponseRedirect("/")
			
			vartieties_form = variety_trials_forms.SelectVarietiesForm(initial={
					'varieties': varieties
				})
			
			return render_to_response(
				'tabbed_view.html',
				{
					'location_form': varieties_form,
					'field_list': field_list,
					'location_list': locations,
					'curyear': str(sorted_list[0][0]), # we sent a preference for curyear, but what was returned may be different
					'heading_list': sorted_list[0][1::],
					'sorted_list': sorted_list[1::],
					'years': years,
					'radius' : 0,
					'blurbs' : unit_blurbs,
					'curfield' : fieldname
				},
				context_instance=RequestContext(request)
			)
	else:
		# seems an error occured...
		return HttpResponseRedirect("/") # send to homepage


def select_variety(request):
	if request.method == 'POST':
		form = variety_trials_forms.SelectVarietyForm(request.POST)
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
		form = variety_trials_forms.SelectVarietyForm()

	return render_to_response(
		'select_variety.html', 
		{ 'form': form },
		context_instance=RequestContext(request)
	)

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
	# a dictionary, keys are strings (source of error), values are strings (message)
	
	if request.method == 'POST': # If the form has been submitted...
		form = variety_trials_forms.UploadCSVForm(request.POST, request.FILES)
		if form.is_valid():
			success, errors = variety_trials_forms.handle_csv_file(request.FILES['csv_file'])
			if success:
				return HttpResponseRedirect('/success/')
			else:
				form = variety_trials_forms.UploadCSVForm()
	else:	
		form = variety_trials_forms.UploadCSVForm()

	return render_to_response(
		'add_from_csv_template.html', 
		{'form': form, 'format_errors': errors},
		context_instance=RequestContext(request)
	)
