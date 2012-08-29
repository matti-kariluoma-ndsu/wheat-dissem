from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from variety_trials_data import models
from variety_trials_data import variety_trials_forms
from variety_trials_data import handle_csv

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
			
def add_trial_entry_csv_file(request):
	errors = {}
	
	if request.method == 'POST': # If the form has been submitted...
		form = variety_trials_forms.UploadCSVForm(request.GET, request.FILES)
		if form.is_valid():
			(success, errors) = handle_csv.checking_for_data(request.FILES['csv_file'])
			if success:
				# show entered data
				return HttpResponseRedirect('/success/')
			else:
				form = variety_trials_forms.UploadCSVForm()
	else:
		form = variety_trials_forms.UploadCSVForm()
	
	return render_to_response(
		'add_from_csv_template.html', 
		{
			'form': form, 
			'format_errors': errors,
		},
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
