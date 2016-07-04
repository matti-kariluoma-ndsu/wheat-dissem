#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import Template, loader, RequestContext
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django import forms as django_forms
from common.util import restricted
from . import forms, models, utils
from progress import Progress, HeaderTypes, HeaderGuess
import json, datetime

@restricted
def index(request):
	context = {}
	uploads = models.UploadProgress.objects.filter(user=request.user)
	in_progress = uploads.filter(submitted=False)
	submitted = sorted(uploads.filter(submitted=True), key=lambda item: item.created)
	if request.method == 'POST':
		completed_form = forms.Upload(request.POST)
		if not completed_form.is_valid():
			return HttpResponse("There was a problem with your submission. Please go back and try again.")
		data_json = utils.process_upload_form(completed_form)
		if not data_json:
			return HttpResponse("You submitted an empty spreadsheet. Please go back and try again.")
		try:
			username = getattr(request.user, request.user.USERNAME_FIELD)
		except:
			username = 'None'
		path = '{username}_{count}.json'.format(username=username, count=uploads.count())
		path = default_storage.save(path, ContentFile(data_json))
		new_progress = models.UploadProgress(user=request.user, path=path)
		new_progress.save()
	in_progress = sorted(in_progress, key=lambda item: item.created)
	context['in_progress'] = in_progress
	context['submitted'] = submitted
	return render(request, 'upload.html', context)

@restricted
def verify(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	context = {}
	progress = Progress(in_progress)
	if request.method == 'POST':
		row_form = forms.VerifyHeaders(request.POST, prefix=HeaderGuess.ROW_PREFIX)
		col_form = forms.VerifyHeaders(request.POST, prefix=HeaderGuess.COLUMN_PREFIX)
		dateform = forms.DateForm(request.POST)
		if not dateform.is_valid():
			return redirect('.') # TODO: Let user know dateform was invalid
		if row_form.is_bound and row_form.is_valid():
			row_type = row_form.cleaned_data['header_type']
		else:
			row_type = HeaderTypes.Data
		if col_form.is_bound and col_form.is_valid():
			col_type = col_form.cleaned_data['header_type']
		else:
			col_type = HeaderTypes.Data
		progress.store_date(dateform, save=False)
		progress.store_headers(row_type, col_type)
		if progress.dates_verified():
			return redirect('locations/')
		else:
			return redirect('.') # TODO: Let user know date was unverified
	else:
		col_guess, row_guess = progress.header_guesses()
		verify_dicts = []
		for guess in (col_guess, row_guess):
			if guess.our_guess() is None or not any(guess.users_input()):
				continue
			form = forms.VerifyHeaders(
					initial={'header_type': guess.our_guess()},
					prefix=guess.prefix
				)
			verify_dicts.append({'headers': guess.users_input(), 'form': form})
		context['verify_dicts'] = verify_dicts
		now_year = datetime.datetime.now().year
		context['dateform'] = forms.DateForm(initial={'year': now_year})
	return render(request, 'verify.html', context)

def verify_model_list(request, progress, template=None, Formcls=None, 
		create_initial_form=None, create_single_form=None, model_names=None, 
		map_name=None, is_verified=None, next_url=None, guesses=None
	):
	if create_single_form is None:
		create_single_form = lambda Fcls, prefix: Fcls(prefix=prefix)
	context = {}
	if request.method == 'POST':
		if 'single_model' in request.POST:
			form = Formcls(
					request.POST, 
					prefix='_whip_single'
				)
			if form.is_bound and form.is_valid():
				map_name(None, form)
		else:
			unsaved = False
			for name in list(model_names):
				form = Formcls(
						request.POST,
						prefix=name
					)
				if not form.is_bound:
					continue
				valid = form.is_valid()
				# try and grab some data in any case
				try:
					is_not = form.cleaned_data['is_not']
				except KeyError:
					is_not = False
				try:
					is_stat = form.cleaned_data['is_stat']
				except KeyError:
					is_stat = False
				if not valid:
					form = None # discard remainder of form
				if is_not or is_stat:
					map_name(name, None, delete=True, save=True)
				if is_stat:
					progress.add_statistic(name, save=True)
				if not is_not and not is_stat:
					map_name(name, form, save=False)
					unsaved = True
			if unsaved:
				progress.save()
		if is_verified():
			return redirect(next_url)
		else:
			return redirect('add/')
	else:
		verify_dicts = []
		for guess in guesses():
			form = create_initial_form(Formcls, guess)
			headers, values = [], []
			try:
				cells = list(progress.progress['cells'][guess.users_input()])
				cells[0] = ('', cells[0][1]) # blank first item
			except KeyError:
				cells = []
			for h, v in cells:
				headers.append(h)
				values.append(v)
			verify_dicts.append({
					'name': guess.users_input(), 
					'form': form,
					'headers': headers,
					'values': values,
				})
		context['verify_dicts'] = verify_dicts
		single_form = create_single_form(Formcls, '_whip_single')
		single_form.fields['is_not'].widget = django_forms.HiddenInput()
		context['single_form'] = single_form
		context['preview'] = progress.progress['cells']
	return render(request, template, context)

@restricted
def verify_locations(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	def create_location_form(Formcls, guess):
		initial = {
				'location': guess.our_guess(), 
				'planting_methods': guess.extra['planting_methods']
			}
		return Formcls(initial=initial, prefix=guess.users_input())
	return verify_model_list(
			request,
			progress,
			template='verify-locations.html',
			Formcls=forms.VerifyLocation,
			create_initial_form=create_location_form,
			model_names=progress.locations(),
			map_name=progress.map_location,
			is_verified=progress.locations_verified,
			next_url='../varieties/',
			guesses=progress.location_guesses,
		)
@restricted
def verify_varieties(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	def create_variety_form(Formcls, guess):
		initial = {'variety': guess.our_guess(), }
		return Formcls(initial=initial, prefix=guess.users_input())
	return verify_model_list(
			request,
			progress,
			template='verify-varieties.html',
			Formcls=forms.VerifyVariety,
			create_initial_form=create_variety_form,
			model_names=progress.varieties(),
			map_name=progress.map_variety,
			is_verified=progress.varieties_verified,
			next_url='../measures/',
			guesses=progress.variety_guesses,
		)
@restricted
def verify_measures(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	def create_measure_form(Formcls, guess):
		initial = {'measure': guess.our_guess(), }
		return Formcls(initial=initial, prefix=guess.users_input())
	return verify_model_list(
			request,
			progress,
			template='verify-measures.html',
			Formcls=forms.VerifyMeasure,
			create_initial_form=create_measure_form,
			model_names=progress.measures(),
			map_name=progress.map_measure,
			is_verified=progress.measures_verified,
			next_url='../statistics/',
			guesses=progress.measure_guesses,
		)
@restricted
def verify_stats(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	def create_statistic_form(Formcls, guess):
		initial = {
				'statistic': guess.our_guess(), 
				'alpha': guess.extra['alpha'],
			}
		return Formcls(initial=initial, prefix=guess.users_input())
	return verify_model_list(
			request,
			progress,
			template='verify-stats.html',
			Formcls=forms.VerifyStatistic,
			create_initial_form=create_statistic_form,
			model_names=progress.statistics(),
			map_name=progress.map_statistic,
			is_verified=progress.statistics_verified,
			next_url='../preview/',
			guesses=progress.statistic_guesses,
		)
@restricted
def verify_preview(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	context = {}
	if request.method == 'POST':
		progress.write_database()
		return redirect('../../')
	else:
		if not progress.dates_verified():
			return redirect('../')
		if not progress.locations_verified():
			return redirect('../locations/')
		if not progress.varieties_verified():
			return redirect('../varieties/')
		if not progress.measures_verified():
			return redirect('../measures/')
		if not progress.statistics_verified():
			return redirect('../statistics/')
		year, table, summary, statnames, colnames, rownames = progress.prepare_table()
		preview_table = zip(rownames, table)
		preview_summary = zip(statnames, summary)
		context['year'] = year
		context['preview_table'] = preview_table
		context['preview_summary'] = preview_summary
		context['column_headers'] = ['', ] + colnames
	return render(request, 'verify-preview.html', context)

def add_model(request, progress, unknown_names=None, template=None, 
		Formcls=None, form_fieldname=None, input_fieldname=None,
		map_name=None, is_verified=None, next_url='..', model_cache=None
	):
	context = {}
	if request.method == 'POST':
		unsaved = False
		for name in unknown_names:
			form = Formcls(
					request.POST,
					prefix=name
				)
			if form.is_bound and form.is_valid():
				user_input = form.cleaned_data[input_fieldname]
				try:
					model = model_cache[user_input]
				except KeyError:
					model = form.save()
					model_cache[user_input] = model
				form.cleaned_data[form_fieldname] = model
				map_name(name, form, save=False)
				unsaved = True
			else:
				if form.cleaned_data['is_not']:
					map_name(name, None, delete=True)
				else:
					map_name(name, None, save=False)
					unsaved = True
				unsaved = True
		if unsaved:
			progress.save()
		return redirect(next_url)
	else:
		add_model_dicts = []
		skip_names = utils.too_similar(unknown_names)
		for name in unknown_names:
			if name in skip_names:
				continue
			add_model_dicts.append({
					'name': name, 
					'form': Formcls(
							prefix=name,
						),
				})
		if len(add_model_dicts) == 0:
			return redirect(next_url)
		context['add_model_dicts'] = add_model_dicts
	return render(request, template, context)

@restricted
def add_locations(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	try:
		locations_map = progress.progress['locations']
	except KeyError:
		locations_map = None
	try:
		location_map = progress.progress['location']
	except KeyError:
		location_map = None
	if location_map:
		_locations = {None: location_map}
	elif locations_map:
		_locations = locations_map
	else:
		_locations = {None: {'pk': -1, 'planting_methods': -1}}
	unknown_names = [name for name in _locations if _locations[name]['pk'] == -1]
	return add_model(
			request, 
			progress,
			unknown_names=unknown_names,
			template='add-locations.html',
			Formcls=forms.AddLocation,
			form_fieldname='location',
			input_fieldname='name',
			map_name=progress.map_planting_methods,
			is_verified=progress.locations_verified,
			next_url='planting-methods/',
			model_cache=utils.create_location_model_cache(),
		)
@restricted
def add_planting_methods(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	try:
		location_map = progress.progress['locations']
		if not location_map:
			location_map = {None: {'planting_methods': -1}}
	except KeyError:
		location_map = {None: {'planting_methods': -1}}
	unknown_names = [name for name in location_map if location_map[name]['planting_methods'] == -1]
	return add_model(
			request, 
			progress,
			unknown_names=unknown_names,
			template='add-planting-methods.html',
			Formcls=forms.AddPlantingMethod,
			form_fieldname='planting_methods',
			input_fieldname='planting_methods',
			map_name=progress.map_planting_methods,
			is_verified=progress.locations_verified,
			next_url='../../',
			model_cache=utils.create_planting_methods_model_cache(),
		)
@restricted
def add_varieties(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	try:
		variety_map = progress.progress['varieties']
		if not variety_map:
			variety_map = {None: {'pk': -1}}
	except KeyError:
		variety_map = {None: {'pk': -1}}
	unknown_names = [name for name in variety_map if variety_map[name]['pk'] == -1]
	return add_model(
			request,
			progress,
			unknown_names=unknown_names,
			template='add-varieties.html',
			Formcls=forms.AddVariety,
			form_fieldname='variety',
			input_fieldname='name',
			map_name=progress.map_variety,
			is_verified=progress.varieties_verified,
			model_cache=utils.create_variety_model_cache(),
		)
@restricted
def add_stats(request, pk=None):
	def create_add_stat_form(Formcls, prefix):
		locations = progress.progress['locations'].keys()
		initial = {
				'data': 'hello\nhey\n',
				'data_json': json.dumps({
						'data': [[None]*len(locations)], 
						'rowname': [''],
						'headers': locations,
					}),
			}
		return Formcls(initial=initial, prefix=prefix)
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	raise NotImplementedError('add statistics uses a spreadsheet view, not written')
	try:
		variety_map = progress.progress['varieties']
		if not variety_map:
			variety_map = {None: {'pk': -1}}
	except KeyError:
		variety_map = {None: {'pk': -1}}
	unknown_names = [name for name in variety_map if variety_map[name]['pk'] == -1]
	return add_model(
			request,
			progress,
			unknown_names=unknown_names,
			template='add-stats.html',
			Formcls=forms.AddStatistic,
			form_fieldname='none',
			input_fieldname='name',
			map_name=progress.map_variety,
			is_verified=progress.varieties_verified,
			model_cache=utils.create_variety_model_cache(),
		)
	

def clean_cache(request, progress, template=None, clean=None):
	context = {}
	if request.method == 'POST':
		clean()
		return redirect('..')
	return render(request, template, context)

@restricted
def clean_locations(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	return clean_cache(
			request,
			progress,
			template='clean.html',
			clean=progress.clean_locations,
		)
@restricted
def clean_varieties(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	return clean_cache(
			request,
			progress,
			template='clean.html',
			clean=progress.clean_varieties,
		)
@restricted
def clean_measures(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	return clean_cache(
			request,
			progress,
			template='clean.html',
			clean=progress.clean_measures,
		)
@restricted
def clean_stats(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	return clean_cache(
			request,
			progress,
			template='clean.html',
			clean=progress.clean_statistics,
		)

@restricted
def update(request, pk=None):
	try:
		in_progress = models.UploadProgress.objects.get(pk=pk)
	except:
		raise Http404
	progress = Progress(in_progress)
	context = {}
	trials, significances = progress.load_trials()
	year = None
	pd = ''
	hd = ''
	colnames = []
	rownames = []
	statnames = []
	# inspect all trials and organize them
	entries = {}
	for trial in trials:
		if not year:
			year = trial.harvest_date.date.year
			pd = trial.plant_date.pk
			hd = trial.harvest_date.pk
		col = (
				trial.location.name,
				trial.location.pk,
				trial.planting_method_tags.planting_methods,
				trial.planting_method_tags.pk,
			)
		row = (trial.variety.name, trial.variety.pk)
		colnames.append(col)
		rownames.append(row)
		entries[(row, col)] = trial
	colnames = sorted(list(set(colnames)))
	rownames = sorted(list(set(rownames)))
	# inspect all significance entries
	summaries = {}
	trial_pks = {}
	for sig in significances:
		try:
			# this is simplified logic, we can assume that all trials in
			# sig.trials have the same location/planting method, due to their 
			# construction from progress.load_trials
			trial = sig.trials.all()[0]
			col = (
				trial.location.name,
				trial.location.pk,
				trial.planting_method_tags.planting_methods,
				trial.planting_method_tags.pk,
			)
		except:
			continue
		row = (sig.method, sig.alpha)
		statnames.append(row)
		summaries[(row, col)] = sig
		trial_pks[col] = ','.join([str(t.pk) for t in sig.trials.all()])
	statnames = sorted(list(set(statnames)))
	# collect table entries
	table = []
	for row in rownames:
		cells = []
		for col in colnames:
			try:
				cell = entries[(row, col)]
				extra = None
			except KeyError:
				cell = None
				extra = {'location': col[1], 'pmt': col[3], 'pd':pd, 'hd':hd}
			cells.append((cell, extra))
		table.append((row, cells))
	# collect summary entries
	summary = []
	for row in statnames:
		cells = []
		for col in colnames:
			try:
				pks = trial_pks[col]
			except KeyError:
				pks = ''
			try:
				cell = summaries[(row, col)]
			except KeyError:
				cell = None
			cells.append((cell, pks))
		summary.append((row, cells))
	try:
		firstpks = trial_pks[colnames[0]]
	except KeyError:
		firstpks = ''
	context['year'] = year
	context['table'] = table
	context['summary'] = summary
	context['first_trial_pks'] = firstpks
	context['column_headers'] = [('', -1, '', -1), ] + colnames
	return render(request, 'update.html', context)
