#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django import VERSION
from django.utils.text import normalize_newlines
from django.core.files.storage import default_storage
from hrsw import models # TODO: reduce coupling
from fuzzywuzzy import fuzz, process as fuzz_process # pip install fuzzywuzzy
import os, json, datetime
from utils import isfloat

measure_aliases = {
		'yield': 'bushels_acre',
		'protein': 'protein_percent',
		'weight': 'test_weight',
	}

class HeaderTypes:
	Data      	= 'data'
	Locations 	= 'locations'
	Varieties 	= 'varieties'
	Measures  	= 'measures'
	Statistics	= 'statistics'
class Guess(object):
	def users_input(self):
		return None
	def our_guess(self):
		return None
	def set_extra(self, extra):
		self.extra = extra
class ModelGuess(Guess):
	def __init__(self, name, pk, ratio):
		self.name = name
		self.pk = pk
		self.ratio = ratio
	def users_input(self):
		return self.name
	def our_guess(self):
		return self.pk
class FieldGuess(Guess):
	def __init__(self, name, fieldname, ratio):
		self.name = name
		self.fieldname = fieldname
		self.ratio = ratio
	def users_input(self):
		return self.name
	def our_guess(self):
		return self.fieldname
class HeaderGuess(Guess):
	ROW_PREFIX = 'row'
	COLUMN_PREFIX = 'column'
	def __init__(self, headers, header_type, prefix):
		self.headers = headers
		self.header_type = header_type
		self.prefix = prefix
	def users_input(self):
		return self.headers
	def our_guess(self):
		return self.header_type

class Progress(object):
	def __init__(self, upload_progress):
		'''
		Load user's progress. 
		This will be called for every view -- don't mutate state!
		'''
		self.model = upload_progress
		self.path = default_storage.path(upload_progress.path)
		try:
			with open(self.path, 'r') as f:
				self.progress = json.load(f)
		except:
			raise
		self.validate()
	def validate(self):
		'''
		ensure sensible defaults. 
		minimally mutate data to ensure restored from disk `properly'.
		'''
		if not isinstance(self.progress, dict):
			self.progress = {}
		def get_or_create(_dict, name, default):
			try:
				get = _dict[name]
			except KeyError:
				get = _dict[name] = default()
			return get
		rows = get_or_create(self.progress, 'rows', list)
		cols = get_or_create(self.progress, 'columns', list)
		date = get_or_create(self.progress, 'date', lambda: None)
		cells = get_or_create(self.progress, 'cells', dict)
		headers = get_or_create(self.progress, 'headers', dict)
		headers_rows = get_or_create(headers, 'rows', lambda: None)
		headers_cols = get_or_create(headers, 'columns', lambda: None)
		headers_stats = get_or_create(headers, HeaderTypes.Locations, list)
		headers_stats = get_or_create(headers, HeaderTypes.Varieties, list)
		headers_stats = get_or_create(headers, HeaderTypes.Measures, list)
		headers_stats = get_or_create(headers, HeaderTypes.Statistics, list)
		def convert_null_to_none(_dict):
			if len(_dict) == 1:
				key = _dict.keys()[0]
				if key == 'null':
					_dict[None] = _dict[key]
					del _dict[key]	
		varieties  = get_or_create(self.progress, 'varieties', dict)
		convert_null_to_none(varieties)
		locations  = get_or_create(self.progress, 'locations', dict)
		convert_null_to_none(locations)
		measures   = get_or_create(self.progress, 'measures', dict)
		convert_null_to_none(measures)
		statistics = get_or_create(self.progress, 'statistics', dict)
		convert_null_to_none(statistics)
		forgot = get_or_create(self.progress, 'forgot', dict)
		forgot_locs  = get_or_create(forgot, 'locations', list)
		forgot_vars  = get_or_create(forgot, 'varieties', list)
		forgot_meas  = get_or_create(forgot, 'measures', list)
		forgot_stats = get_or_create(forgot, 'statistics', list)
		trial_entries = get_or_create(self.progress, 'trial_entries', list)
		submitted = get_or_create(self.progress, 'submitted', dict)
		locations = get_or_create(submitted, 'locations', list)
		varieties = get_or_create(submitted, 'varieties', list)
		methods = get_or_create(submitted, 'planting_methods', list)
		harvest_date = get_or_create(submitted, 'harvest_date', dict)
	def save(self, sync=True):
		try:
			with open(self.path, 'w') as f:
				json.dump(self.progress, f)
				if sync:
					f.flush()
					os.fsync(f.fileno())
		except:
			raise
	def match_statistic(self, name):
		db_statistics = models.SignificanceEntry.methods
		db_name, ratio = fuzz_process.extractOne(
				name,
				db_statistics
			)
		if ratio > 85:
			return db_name
		return None
	def header_guesses(self, save=True):
		if self.progress:
			data = self.progress['data']
		else:
			data = [[None]] # no data
		def classify_headers(headers):
			# first check if we are a list of numbers
			if all(isfloat(x) for x in headers[1:]):
				return HeaderTypes.Data
			# fuzzy check against database
			variety_names = [v.name for v in models.Variety.objects.all()]
			location_names = [l.name for l in models.Location.objects.all()]
			measure_names = models.TrialEntry.measures + tuple(measure_aliases.keys())
			vratio = fuzz.token_sort_ratio(headers, ' '.join(variety_names))
			lratio = fuzz.token_sort_ratio(headers, ' '.join(location_names))
			mratio = fuzz.token_sort_ratio(headers, ' '.join(measure_names))
			candidates = (
					(vratio, HeaderTypes.Varieties),
					(lratio, HeaderTypes.Locations),
					(mratio, HeaderTypes.Measures),
				)
			winner = sorted(
					candidates,
					reverse=True,
					key=lambda ratio_type: ratio_type[0],
				)[0]
			ratio, _type = winner
			if ratio < 40:
				_type = None
			return _type
		rows = []
		columns = [[] for _ in data[0]] # assume balanced table
		# create data structure for rows, columns
		# [(header?, value), ...]
		# where header? is the first value in the row for rows, first value in column for columns
		# Note: the data is repeated; each value is in both a row and column
		# Note: the first element will always be (header?, header?)
		## first remove empty columns
		empty_cols = []
		rowrange = range(len(data))
		colrange = range(len(data[0]))
		for j in colrange:
			if not any([data[i][j] for i in rowrange]):
				empty_cols.append(j)
		for row in data:
			if not any(row[1:]):
				continue
			subrow = []
			for (j, cell) in enumerate(row):
				if j in empty_cols:
					continue
				subrow.append((data[0][j], cell))
				columns[j].append((row[0], cell))
			rows.append(subrow)
		columns = [c for c in columns if any(c)]
		# map each column, row by header name for easier lookup later
		column_headers = self.progress['columns'] = []
		row_headers = self.progress['rows'] = []
		for column in columns:
			_, header = column[0]
			row_headers.append(header)
			self.progress['cells'][header] = column
		for row in rows:
			_, header = row[0]
			column_headers.append(header)
			self.progress['cells'][header] = row
		# when making a guess, first discard first item (usually cell(0, 0) is garbage),
		# then attempt to filter out any statistics so our users are not too 
		# confused (although they'll see them later when confirming the mapping)
		column_guess = HeaderGuess(
				[c for c in column_headers[1:] if self.match_statistic(c) is None],
				classify_headers(column_headers),
				HeaderGuess.COLUMN_PREFIX
			)
		row_guess = HeaderGuess(
				[r for r in row_headers[1:] if self.match_statistic(r) is None],
				classify_headers(row_headers),
				HeaderGuess.ROW_PREFIX
			)
		if save:
			self.save()
		return (column_guess, row_guess)
	def store_date(self, form, save=True):
		self.progress['date'] = form.cleaned_data['year']
		if save:
			self.save()
	def store_headers(self, row_type, col_type, save=True):
		self.progress['headers']['rows'] = row_type
		self.progress['headers']['columns'] = col_type
		self.progress['headers'][row_type] = self.progress['rows']
		self.progress['headers'][col_type] = self.progress['columns']
		if row_type != HeaderTypes.Data and col_type != HeaderTypes.Data:
			# if there are headers for both row and columns, drop the first item (i.e. cell (0, 0)) from header lists
			self.progress['headers'][row_type].pop(0)
			self.progress['headers'][col_type].pop(0)
		if save:
			self.save()
	def store_statistics(self, form, save=True):
		raise NotImplementedError('this code was copypasted here, please clean up')
		if form.cleaned_data['is_json']:
			try:
				data_json = json.loads(form.cleaned_data['data_json'])
			except:
				data_json = {'data': [''], 'headers': ['']}
			try:
				rows = data_json['data']
				headers = data_json['headers']
			except:
				rows = [['']] # list: list: empty string
				headers = ['']
			try:
				row = rows[0]
			except IndexError:
				row = ['']
			if any(row):
				name_value = dict(zip(headers, row))
		else:
			data = form.cleaned_data['data']
			data = normalize_newlines(data)
			zipped = []
			for row in data.split('\n'):
				try:
					name, value =  (item.strip() for item in row.split(':'))
				except:
					continue
				zipped.append((name, value))
			if any(zipped):
				name_value = dict(zipped)
		existing_name['name_value'] = name_value
	def get_headers(self, oftype):
		'''
		oftype: an enum from HeaderTypes
		returns a list of strings the user uploaded, or an empty list if 
		no match to 'oftype'
		'''
		try:
			headers = self.progress['headers'][oftype]
		except KeyError:
			headers = []
		return headers
	def locations(self):
		return self.get_headers(HeaderTypes.Locations)
	def varieties(self):
		return self.get_headers(HeaderTypes.Varieties)
	def measures(self):
		return self.get_headers(HeaderTypes.Measures)
	def statistics(self):
		return self.get_headers(HeaderTypes.Statistics)
	def add_statistic(self, name, save=True):
		if name not in self.progress['headers'][HeaderTypes.Statistics]:
			self.progress['headers'][HeaderTypes.Statistics].append(name)
			if save:
				self.save()
	def make_model_guesses(self, names=None, existing=None, name_model=None):
		'''
		names: list of names the user input
		existing: dictionary of {name: {pk: int}} that we've previously stored
		name_model: dictionary of {model.name: model} where model has member pk ('model.pk')
		returns a list of ModelGuess
		'''
		guesses = []
		for name in names:
			pk = -1
			try:
				existing_name = existing[name]
			except (KeyError, TypeError):
				existing_name = None
			if existing_name:
				try:
					pk = existing_name['pk']
				except:
					pk = -1
			ratio = None
			if pk == -1 and name_model:
				db_name, ratio = fuzz_process.extractOne(
						name,
						name_model.keys()
					)
				if ratio > 85:
					pk = name_model[db_name].pk
			guesses.append(ModelGuess(name, pk, ratio))
		return guesses
	def location_guesses(self):
		db_locations = dict([(l.name, l) for l in models.Location.objects.all()])		
		existing = self.progress['locations']
		guesses = self.make_model_guesses(
				names = self.locations(),
				existing = existing,
				name_model = db_locations,
			)
		db_methods = dict([(pm.planting_methods, pm) for pm in models.PlantingMethod.objects.all()])
		for guess in guesses:
			name = guess.name
			planting_methods = -1
			try:
				existing_name = existing[name]
			except (KeyError, TypeError):
				existing_name = {}
			try:
				planting_methods = existing_name['planting_methods']
			except (KeyError, TypeError):
				planting_methods = -1
			if guess.ratio and guess.ratio > 98:
				try:
					planting_methods = models.PlantingMethod.objects.get(planting_methods='').pk
				except:
					planting_methods = -1
			elif db_methods:
				db_methodname, ratio = fuzz_process.extractOne(
						name,
						db_methods.keys(),
					)
				if ratio > 85:
					planting_methods = db_methods[db_methodname].pk
			guess.set_extra({'planting_methods': planting_methods})
		return guesses
	def variety_guesses(self):
		db_varieties = dict([(l.name, l) for l in models.Variety.objects.all()])
		return self.make_model_guesses(
				names = self.varieties(),
				existing = self.progress['varieties'],
				name_model = db_varieties,
			)
	def make_field_guesses(self, names=None, existing=None, fields=None):
		'''
		names: a list of user input names
		existing:  dictionary of {name: {fieldname: str}} that we've previously stored
		fields: a list of str, valid fields for the model we have data for
		returns a list of FieldGuess
		'''
		guesses = []
		for name in names:
			fieldname = None
			try:
				existing_name = existing[name]
			except KeyError:
				existing_name = None
			if existing_name:
				try:
					fieldname = existing_name['fieldname']
				except:
					fieldname = None
			ratio = None
			if not fieldname:
				fieldname, ratio = fuzz_process.extractOne(
						name,
						fields
					)
			guesses.append(FieldGuess(name, fieldname, ratio))
		return guesses
	def measure_guesses(self):
		guesses = self.make_field_guesses(
				names = self.measures(),
				existing = self.progress['measures'],
				fields = models.TrialEntry.measures + tuple(measure_aliases.keys()),
			)
		for guess in guesses:
			aliasname = guess.fieldname
			if aliasname in measure_aliases.keys():
				guess.fieldname = measure_aliases[aliasname]
		return guesses
	def statistic_guesses(self):
		existing = self.progress['statistics']
		guesses = self.make_field_guesses(
				names = self.statistics(),
				existing = existing,
				fields = models.SignificanceEntry.methods,
			)
		db_levels = dict([(str(f), f) for f in models.SignificanceEntry.levels if f is not None])
		for guess in guesses:
			name = guess.name
			extra = {}
			# set data
			coltype = self.progress['headers']['columns']
			rowtype = self.progress['headers']['rows']
			if coltype == HeaderTypes.Locations and rowtype == HeaderTypes.Varieties:
				headers = self.progress['data'][0][1:]
				for row in self.progress['data'][1:]:
					if row[0] == name:
						break
				row = row[1:]
				for i, h in enumerate(headers):
					if h is None:
						break
				headers = headers[:i]
				row = row[:i]
			else:
				# TODO: handle other cases of stats being reported!
				headers = ['']
				row = ['']
			extra['data'] = '\n'.join(['{}: {}'.format(h, r) for (h, r) in zip(headers, row)])
			# set data_json
			extra['data_json'] = json.dumps({
					'headers': headers,
					'data': [row],
					'rowname': [name],
				})
			# set alpha
			alpha = None
			try:
				existing_name = existing[name]
			except (KeyError, TypeError):
				existing_name = None
			try:
				alpha = existing_name['alpha']
			except:
				alpha = None
			if guess.ratio and guess.ratio > 98:
				alpha = None
			elif db_levels:
				db_levelstr, ratio = fuzz_process.extractOne(
						name,
						db_levels.keys(),
					)
				if ratio > 85:
					alpha = db_levels[db_levelstr]
			extra['alpha'] = alpha
			guess.set_extra(extra)
		return guesses
	def forget_header(self, name, oftype):
		headers = self.get_headers(oftype)
		try:
			headers.remove(name)
		except ValueError:
			pass
	def forget_location(self, name):
		self.forget_header(name, HeaderTypes.Locations)
		self.progress['forgot']['locations'].append(name)
		self.save()
	def forget_variety(self, name):
		self.forget_header(name, HeaderTypes.Varieties)
		self.progress['forgot']['varieties'].append(name)
		self.save()
	def forget_measure(self, name):
		self.forget_header(name, HeaderTypes.Measures)
		self.progress['forgot']['measures'].append(name)
		self.save()
	def forget_statistic(self, name):
		self.forget_header(name, HeaderTypes.Statistics)
		self.progress['forgot']['statistics'].append(name)
		self.save()
	def map_model_name(self, name, form, save=True, delete=False, existing=None,
			forget=None, form_fieldname=None
		):
		'''
		name: users input
		form: form containing which database model to map 'name' to
		save: set False for batch processing; remember to manually save when done
		delete: set True to unmap 'name'
		existing: the node in self.progress where we are storing this mapping
		forget: a function that removes 'name' from further user-views
		form_fieldname: the fieldname in 'form' where our model-pk can be found
		
		maps the users input to a database name, and stores this mapping. Also
		handles unmapping.
		'''
		if delete:
			save = False # next call will save()
			forget(name)
		else:
			if form is None:
				pk = -1
				mname = None
			else:
				model = form.cleaned_data[form_fieldname]
				pk = model.pk
				mname = model.name
			existing[name] = {
					'pk': pk,
					'name': mname,
				}
		if save:
			self.save()
	def map_location(self, name, form, save=True, delete=False):
		self.map_model_name(
				name, 
				form, 
				save = save, 
				delete = delete,
				existing = self.progress['locations'],
				forget = self.forget_location,
				form_fieldname = 'location',
			)
		self.map_planting_methods(name, form, save=save, delete=delete)
	def map_planting_methods(self, name, form, save=True, delete=False):
		'''
		dig out a location, and add planting_methods info to it
		'''
		try:
			locations_name = self.progress['locations'][name]
		except KeyError:
			locations_name = {} # discard data rather than return (fewer branches)
			save = False
		if delete:
			pass
		else:
			if form is None:
				planting_methods = -1
				pmtext = None
			else:
				try:
					model = form.cleaned_data['planting_methods']
					planting_methods = model.pk
					pmtext = model.planting_methods
				except:
					planting_methods = -1
					pmtext = None
			locations_name['planting_methods'] = planting_methods
			locations_name['planting_methods_text'] = pmtext
		if save:
			self.save()
	def map_variety(self, name, form, save=True, delete=False):
		self.map_model_name(
				name, 
				form, 
				save = save, 
				delete = delete,
				existing = self.progress['varieties'],
				forget = self.forget_variety,
				form_fieldname = 'variety',
			)
	def map_field_name(self, name, form, save=True, delete=False, existing=None,
			forget=None, form_fieldname=None
		):
		'''
		name: users input
		form: form containing which database model to map 'name' to
		save: set False for batch processing; remember to manually save when done
		delete: set True to unmap 'name'
		existing: the node in self.progress where we are storing this mapping
		forget: a function that removes 'name' from further user-views
		form_fieldname: the fieldname in 'form' where our model-pk can be found
		
		maps the users input to a database fieldname, and stores this mapping. Also
		handles unmapping.
		The logic here is different than map_model_name, a fieldname will always
		be selected. Special logic exists for the 'not a fieldname' (form=None) case.
		'''
		if delete:
			save = False # next call will save()
			forget(name)
		if form is None:
			fieldname = None
			try:
				del existing[name]
			except KeyError:
				pass
		else:
			fieldname = form.cleaned_data[form_fieldname]
			existing[name] = {
					'fieldname': fieldname,
				}
		if save:
			self.save()
	def map_measure(self, name, form, save=True, delete=False):
		self.map_field_name(
				name, 
				form, 
				save = save, 
				delete = delete,
				existing = self.progress['measures'],
				forget = self.forget_measure,
				form_fieldname = 'measure',
			)
	def map_statistic(self, name, form, save=True, delete=False):
		existing = self.progress['statistics']
		self.map_field_name(
				name, 
				form, 
				save = save, 
				delete = delete,
				existing = existing,
				forget = self.forget_statistic,
				form_fieldname = 'statistic',
			)
		if not delete and form is not None:
			try:
				existing_name = existing[name]
			except KeyError:
				existing_name = {} # discard
			existing_name['alpha'] = form.cleaned_data['alpha']
			existing_name['comparing'] = form.cleaned_data['measure']
		if save:
			self.save()
	def clean_locations(self):
		self.progress['locations'] = {}
		locations = self.get_headers(HeaderTypes.Locations)
		locations.extend(self.progress['forgot']['locations'])
		self.progress['forgot']['locations'] = []
		self.save()
	def clean_varieties(self):
		self.progress['varieties'] = {}
		varieties = self.get_headers(HeaderTypes.Varieties)
		varieties.extend(self.progress['forgot']['varieties'])
		self.progress['forgot']['varieties'] = []
		self.save()
	def clean_measures(self):
		self.progress['measures'] = {}
		measures = self.get_headers(HeaderTypes.Measures)
		measures.extend(self.progress['forgot']['measures'])
		self.progress['forgot']['measures'] = []
		self.save()
	def clean_statistics(self):
		self.progress['statistics'] = {}
		statistics = self.get_headers(HeaderTypes.Statistics)
		statistics.extend(self.progress['forgot']['statistics'])
		self.progress['forgot']['statistics'] = []
		self.save()
	def dates_verified(self):
		if self.progress['date'] is None:
			return False
		return True
	def _verified(self, existing=None, names=None, valid=None, use_existence_test=True):
		if use_existence_test and not existing:
			return False
		if not names:
			names = [None, ]
		for name in names:
			try:
				existing_name = existing[name]
			except KeyError:
				return False
			if valid(existing_name):
				continue
			return False
		return True
	def locations_verified(self):
		return self._verified(
				existing = self.progress['locations'],
				names = self.locations(),
				valid = lambda existing_name: existing_name['pk'] != -1 and existing_name['planting_methods'] != -1,
			)
	def varieties_verified(self):
		return self._verified(
				existing = self.progress['varieties'],
				names = self.varieties(),
				valid = lambda existing_name: existing_name['pk'] != -1,
			)
	def measures_verified(self):
		return self._verified(
				existing = self.progress['measures'],
				names = self.measures(),
				valid = lambda existing_name: existing_name['fieldname'] in models.TrialEntry.measures,
			)
	def statistics_verified(self):
		return self._verified(
				existing = self.progress['statistics'],
				names = self.statistics(),
				valid = lambda _: True,
				use_existence_test = False,
			)
	def prepare_table(self):
		## collect entered data
		trial_entries = {}
		summary_entries = {}
		locations = []
		varieties = []
		measures = []
		# locations, varieties, measures
		lnames = self.progress['headers'][HeaderTypes.Locations]
		vnames = self.progress['headers'][HeaderTypes.Varieties]
		mnames = self.progress['headers'][HeaderTypes.Measures]
		if not lnames and not vnames and not mnames:
			pass
		elif not lnames and not vnames:
			pass
		elif not vnames and not mnames:
			pass
		elif not lnames and not mnames:
			pass
		else:
			if not lnames:
				lnames = [None]
			if not vnames:
				vnames = [None]
			if not mnames:
				mnames = [None]
		# statistics
		snames = self.progress['headers'][HeaderTypes.Statistics]
		if not snames:
			snames = []
		# define get_cell
		row_type = self.progress['headers']['rows']
		col_type = self.progress['headers']['columns']
		if row_type == HeaderTypes.Locations:
			get_row = lambda (ln, vn, mn): ln
		elif row_type == HeaderTypes.Varieties:
			get_row = lambda (ln, vn, mn): vn
		elif row_type == HeaderTypes.Measures:
			get_row = lambda (ln, vn, mn): mn
		else: # HeaderTypes.Data
			get_row = lambda (ln, vn, mn): None
		if col_type == HeaderTypes.Locations:
			get_col = lambda (ln, vn, mn): ln
		elif col_type == HeaderTypes.Varieties:
			get_col = lambda (ln, vn, mn): vn
		elif col_type == HeaderTypes.Measures:
			get_col = lambda (ln, vn, mn): mn
		else: # HeaderTypes.Data
			get_col = lambda (ln, vn, mn): None
		def get_cell(ln, vn, mn):
			row = get_row((ln, vn, mn))
			col = get_col((ln, vn, mn))
			cell = (None, None)
			if row is None:
				tmp = col
				col = row
				row = tmp
			try:
				rows = self.progress['cells'][row]
			except KeyError:
				rows = []
			for col_val in rows:
				if col_val[0] == col:
					cell = col_val
					break
			return cell
		# collect entries
		for lname in lnames:
			location = self.progress['locations'][lname]
			location_name = '{}-{}'.format(location['name'], location['planting_methods_text'])
			locations.append(location_name)
			summary_entries[lname] = {}
			for vname in vnames:
				variety = self.progress['varieties'][vname]
				variety_name = variety['name']
				varieties.append(variety_name)
				for mname in mnames:
					measure = self.progress['measures'][mname].copy()
					measure_name = measure['fieldname']
					measures.append(measure_name)
					val = get_cell(lname, vname, mname)[1]
					if not isfloat(val):
						val = None
					measure['value'] = val
					entry = {
							'location': location,
							'variety': variety,
							'measure': measure,
						}
					trial_entries[(location_name, variety_name, measure_name)] = entry
					for sname in snames:
						cells = self.progress['cells'][sname]
						cell = (None, None)
						for col_val in cells:
							if col_val[0] == lname:
								cell = col_val
								header = lname
								break
							elif col_val[0] == vname:
								cell = col_val
								header = vname
								break
							elif col_val[0] == mname:
								cell = col_val
								header = mname
								break
						sentry = {
								'value': cell[1],
							}
						summary_entries[header][sname] = sentry
		# collect summary_entries
		for name in []:
			stats = {}
			stat = {}
			stat['value'] = sval
			stats[name] = stat
			summary_entries[location_name] = stats
		## construct main table
		locations = sorted(list(set(locations)))
		varieties = sorted(list(set(varieties)))
		measures = sorted(list(set(measures)))
		table = []
		for v in varieties:
			row = []
			for l in locations:
				cell = []
				for m in measures:
					try:
						item = trial_entries[(l, v, m)]
					except KeyError:
						item = None
					cell.append(item)
				row.append(cell)
			table.append(row)
		## construct summary table (statistic entries)
		summary = []
		prettystatnames = []
		statistics = self.progress['statistics']
		havestats = True
		if None in statistics and not statistics[None]:
			havestats = False
		if havestats:
			statmap = {}
			statnames = []
			# make a mapping from pretty names to user-input names
			for name in statistics:
				pretty = '{} ({})'.format(statistics[name]['fieldname'], statistics[name]['alpha'])
				statmap[pretty] = name
			# sort pretty names
			prettystatnames = sorted(statmap.keys())
			# ensure we iterate using the ordering we just made over pretty names
			for name in prettystatnames:
				statnames.append(statmap[name])
			for name in statnames:
				row = []
				for l in lnames: # only show stats that compare across locations
					try:
						val = summary_entries[l][name]['value']
					except KeyError:
						val = None
					row.append({'value': val, 'comparing': statistics[name]['comparing']})
				summary.append(row)
		## bundle it up and send it along
		year = self.progress['date']
		self.progress['trial_entries'] = trial_entries.values()
		#self.progress['table'] = table
		#self.progress['summary'] = summary
		self.save()
		return year, table, summary, prettystatnames, locations, varieties
	def write_database(self):
		# create SignificanceEntry
		significance_entries = []
		name_sigentry = {}
		statistics = self.progress['statistics']
		# TODO: BUG: if a location has no entries, but has stat entries,
		# TODO: it will not show up in the preview but will be written here
		# TODO: (kinda harmless though, since it won't have any trials mapped to it)
		for name in statistics:
			if not statistics[name]:
				continue
			fieldname = statistics[name]['fieldname']
			alpha = statistics[name]['alpha']
			if not alpha:
				alpha = None
			comparing = statistics[name]['comparing']
			try:
				cells = self.progress['cells'][name]
			except KeyError:
				cells = []
			for header, value in cells:
				if not value or not isfloat(value):
					continue
				sigentry = models.SignificanceEntry(
						comparing=comparing,
						method=fieldname,
						alpha=alpha,
						value=value,
					)
				significance_entries.append(sigentry)
				try:
					name_sigentry[header].append(sigentry)
				except KeyError:
					name_sigentry[header] = [sigentry]
		for sigentry in significance_entries:
			sigentry.save()
		# create Date
		year = int(self.progress['date'])
		date_pd = datetime.date(year=year, month=5, day=1)
		date_hd = datetime.date(year=year, month=8, day=1)
		try: 
			plant_date = models.Date.objects.get(date=date_pd)
		except:
			plant_date = models.Date(date=date_pd)
			plant_date.save()
		try:
			harvest_date = models.Date.objects.get(date=date_hd)
		except:
			harvest_date = models.Date(date=date_hd)
			harvest_date.save()
		# create/update TrialEntry objects
		entries = []
		lpvh_entries = {}
		location_names = []
		variety_names = []
		planting_methods = []
		for trial in models.TrialEntry.objects.filter(harvest_date=harvest_date):
			lpvh = (
					trial.location.pk,
					trial.planting_method_tags.pk,
					trial.variety.pk,
					trial.harvest_date.pk
				)
			lpvh_entries[lpvh] = trial
		for entry in self.progress['trial_entries']:
			location = entry['location']['pk']
			planting_methods = entry['location']['planting_methods']
			variety = entry['variety']['pk']
			lpvh = (location, planting_methods, variety, harvest_date.pk)
			try:
				trial = lpvh_entries[lpvh]
			except KeyError:
				trial = models.TrialEntry(
						location_id=location,
						variety_id=variety,
						planting_method_tags_id=planting_methods,
						harvest_date=harvest_date,
						plant_date=plant_date,
					)
				lpvh_entries[lpvh] = trial
			measure = entry['measure']['fieldname']
			value = entry['measure']['value']
			if value is None:
				continue
			setattr(trial, measure, value)
			entries.append(trial)
			trial.save()
			# grab info for a later requery of these trials
			location_names.append(trial.location.name)
			variety_names.append(trial.variety.name)
			planting_methods.append(trial.planting_method_tags.planting_method)
		# attach TrialEntry objects to SignificanceEntry objects
		for name, sigentries in name_sigentry.items():
			# name is a user-entered string, lookup in our mappings
			# TODO: assume name is a location for now
			location = self.progress['locations'][name]['pk']
			planting_methods = self.progress['locations'][name]['planting_methods']
			# TODO: avoid the following database call
			trials = list(
					models.TrialEntry.objects.filter(
							location_id=location
						).filter(
							planting_method_tags_id=planting_methods
						).filter(
							harvest_date=harvest_date
						)
				)
			for sigentry in sigentries:
				sigentry.trials.add(*trials)
				sigentry.save()
		# save TrialEntry query for later editing
		self.progress['submitted']['locations'] = list(set(location_names))
		self.progress['submitted']['varieties'] = list(set(variety_names))
		self.progress['submitted']['planting_methods'] = list(set(planting_methods))
		self.progress['submitted']['harvest_date'] = {
				'year': harvest_date.date.year,
				'month': harvest_date.date.month,
				'day': harvest_date.date.day,
			}
		self.save()
		self.model.submitted = True
		self.model.save()
	def load_trials(self):
		locations = self.progress['submitted']['locations']
		varieties = self.progress['submitted']['varieties']
		planting_methods = self.progress['submitted']['planting_methods']
		date = self.progress['submitted']['harvest_date']
		harvest_date = datetime.date(
				year=date['year'],
				month=date['month'],
				day=date['day'],
			)
		trials = models.TrialEntry.objects.filter(
				location__name__in=locations,
				variety__name__in=varieties,
				planting_method_tags__planting_methods__in=planting_methods,
				harvest_date__date=harvest_date,
			).select_related('location', 'variety')
		sigs = models.SignificanceEntry.objects.filter(
				trials__in=trials,
			).prefetch_related('trials')
		return trials, sigs
