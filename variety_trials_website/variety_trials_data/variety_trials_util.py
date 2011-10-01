from variety_trials_data.models import Trial_Entry #, Date
from variety_trials_data import models
from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv

class Filter_by_Field:
	"""
	Utility class to return a formatted dictionary of all given entries,
	sorted by location name and year, filtered by one field and averaged
	across.
	"""
	
	field = {'name':''} # default value such that we return nothing if a bogus field is given
	entries = {}
	lsds = {}
	years = []
	locations = []
	year = 0
	
	def __init__(self):
		pass
	
	def __init__(self, entries, field, years, pref_year):
		"""
		Initializes internal data structures using the an input list of 
		entries, a field to filter on, and the years to include.
		"""
		return self.populate(entries, field, years, pref_year)
	
	def qnorm(self, probability):
		"""
		A reimplementation of R's qnorm() function.
		
		This function calculates the quantile function of the normal
		distributition.
		(http://en.wikipedia.org/wiki/Normal_distribution#Quantile_function)
		
		Required is the erfinv() function, the inverse error function.
		(http://en.wikipedia.org/wiki/Error_function#Inverse_function)
		"""
		if probability > 1 or probability <= 0:
			raise BaseException # TODO: raise a standard/helpful error
		else:
			return sqrt(2) * erfinv(2*probability - 1)
			
	def qt(self, probability, degrees_of_freedom):
		"""
		A reimplementation of R's qt() function.
		
		This function calculates the quantile function of the student's t
		distribution.
		(http://en.wikipedia.org/wiki/Quantile_function#The_Student.27s_t-distribution)
		
		This algorithm has been taken (line-by-line) from Hill, G. W. (1970)
		Algorithm 396: Student's t-quantiles. Communications of the ACM, 
		13(10), 619-620.
		
		Currently unimplemented are the improvements to Algorithm 396 from
		Hill, G. W. (1981) Remark on Algorithm 396, ACM Transactions on 
		Mathematical Software, 7, 250-1.
		"""
		n = degrees_of_freedom
		P = probability
		t = 0
		if (n < 1 or P > 1.0 or P <= 0.0 ):
			raise BaseException #TODO: raise a standard/helpful error
		elif (n == 2):
			t = sqrt(2.0/(P*(2.0-P)) - 2.0)
		elif (n == 1):
			P = P * pi/2
			t = cos(P)/sin(P)
		else:
			a = 1.0/(n-0.5)
			b = 48.0/(a**2.0)
			c = ((20700.0*a/b - 98.0)*a - 16.0)*a + 96.36
			d = ((94.5/(b+c) - 3.0)/b + 1.0)*sqrt(a*pi/2.0)*float(n)
			x = d*P
			y = x**(2.0/float(n))
		
			if (y > 0.05 + a):
				x = self.qnorm(P*0.5)
				y = x**2.0
				
				if (n < 5):
					c = c + 0.3*(float(n)-4.5)*(x+0.6)

				c = (((0.05*d*x-5.0)*x-7.0)*x-2.0)*x+b+c
				y = (((((0.4*y+6.3)*y+36.0)*y+94.5)/c-y-3.0)/b+1.0)*x
				y = a*y**2.0
				
				if (y > 0.002):
					y = exp(y) - 1.0
				else:
					y = 0.5*y**2.0 + y

			else:
				y = ((1.0/(((float(n)+6.0)/(float(n)*y)-0.089*d-0.822)*(float(n)+2.0)*3.0)+0.5/(float(n)+4.0))*y-1.0)*(float(n)+1.0)/(float(n)+2.0)+1.0/y
			
			t = sqrt(float(n)*y)
		
		return t

	def LSD(self, response_to_treatments, probability):
		"""
		A stripped-down reimplementation of LSD.test from the agricoloae
		package. (http://cran.r-project.org/web/packages/agricolae/index.html)
		
		Calculates the Least Significant Difference of a multiple comparisons
		trial, over a balanced dataset.
		"""
		trt = response_to_treatments
		#model = aov(y~trt)
		#df = df.residual(model)
		# df is the residual Degrees of Freedom
		# n are factors, k is responses per factor
		n = len(trt)
		k = len(trt[0]) # == len(trt[1]) == ... == len(trt[n])
		degrees_freedom_of_error = n*(k-1)
		
		# SSE is the Error Sum of Squares
		
		treatment_means = {}
		for i in range(len(trt)):
			sum = 0.0
			count = 0
			for j in trt[i]:
				sum += float(j)
				count += 1
			treatment_means[i] = sum/float(count)
		
		SSE = 0.0
		for i in range(len(trt)):
			for j in trt[i]:
				SSE += (float(j) - treatment_means[i])**2.0
		
		mean_squares_of_error = SSE / degrees_freedom_of_error
		
		Tprob = self.qt(probability, degrees_freedom_of_error)
			
		LSD = Tprob * sqrt(2.0 * mean_squares_of_error / k)

		return LSD
		
	def populate(self, entries, field, years, pref_year):
		"""
		"""
		self.field = {'name':''}
		self.entries = {}
		self.years = []
		self.locations = []
		self.year = pref_year
		
		# test if field is a Trial_Entry field
		if field in Trial_Entry._meta.fields:
			self.field = field
		
		# test if years are ordered properly
		test = True;
		for i in range(len(years)):
			test = (test and (years[i] == sorted(years, reverse=True)[i]))
		
		if test:
			self.years = years
		else:
			self.years = years 
			#raise # TODO alert the programmer, not the user.
		
		# test if year is in the list of years
		if self.year not in self.years:
			self.year = max(self.years)
		
		fieldname = self.field.name
		locations = {} # use a dictionary so we don't have to check for dups
		for entry in entries:
			year = int(entry.harvest_date.date.year)
			if year in self.years:
				name = str(entry.variety.name)
				location = str(entry.location.name)
				locations[location] = None
				try:
					value = getattr(entry, fieldname)
				except AttributeError:
					value = None
				if value != None:
					try:
						self.entries[year][name][location].append(value)
					except KeyError:
						try:
							self.entries[year][name][location] = [value]
						except KeyError:
							try:
								self.entries[year][name] = {}
							except KeyError:
								self.entries[year] = {}
								self.entries[year][name] = {}
							self.entries[year][name][location] = [value]
					
					value = entry.lsd_05
					if (value is not None and float(value) > 0.0):
						pass
					else:
						value = entry.hsd_10
						if (value is not None and float(value) > 0.0):
							pass
						else:
							value = entry.lsd_10
							if (value is not None and float(value) > 0.0):
								pass
							else:
								value = None
					
					try:
						self.lsds[year][name][location].append(value)
					except KeyError:
						try:
							self.lsds[year][name][location] = [value]
						except KeyError:
							try:
								self.lsds[year][name] = {}
							except KeyError:
								self.lsds[year] = {}
								self.lsds[year][name] = {}
							self.lsds[year][name][location] = [value]
		
		self.locations = sorted(locations.keys())
		# test if the most recent year has enough data
		try:
			test_dict = self.entries[max(self.years)]
		except KeyError:
			test_dict = {}
		
		if len(test_dict.keys()) < 5: # TODO: hardcoded numeric value
			self.years.remove(max(self.years))
		
					
	
	def fetch(self):
		"""
		Returns a list of lists, suitable for a tabular layout. The first
		list contains the header names, and each other list begins with the
		variety name, followed by the values correpsonding to the header.
		"""
		data = {}
		avg_years = []
		
		myear = self.year
		try:
			current_year = self.entries[myear].keys()
		except KeyError:
			try:
				myear = max(self.entries.keys())
				current_year = self.entries[myear].keys()
			except:
				current_year = []
		
		for name in current_year:
			for location in self.entries[myear][name]:
				sum_list = self.entries[myear][name][location]
				avg_value = round(sum(sum_list) / len(sum_list), 2)
				#lsd_list = self.lsds[myear][name][location]
				#lsd_value = max(lsd_list)
				try:
					#data[name][location] = (avg_value, lsd_value) # a tuple
					data[name][location] = avg_value
				except KeyError:
					data[name] = {}
					#data[name][location] = (avg_value, lsd_value) # a tuple
					data[name][location] = avg_value
		
		years_less = [myear]
		for year in self.years:
			if year < myear:
				years_less.append(year)
		
		for year in sorted(years_less):
			for element in avg_years:
				element.append(year)
			avg_years.append([year])
			
		for element in avg_years:
			key = '%d-yr' % len(element)
			for year in element:
				if year in self.entries.keys():
					for name in self.entries[year].keys():
						try:
							data[name]['meta'] = {}
						except KeyError:
							data[name] = {}
							data[name]['meta'] = {}
						data[name]['meta'][key] = 0
						count = 0
						for location in self.entries[year][name].keys():
							sum_list = self.entries[year][name][location]
							data[name]['meta'][key]	+= sum(sum_list)
							count += len(sum_list)
							### TODO: de we need to tack on lsd info?
						### TODO: this is the wrong handling of the "don't average a single value, single year" case, it also short circuits 2-yr and 3-yr
						if count > 1: # don't average out a set of one element
							data[name]['meta'][key] = round(data[name]['meta'][key] / count, 2)
						else:
							data[name]['meta'][key] = None
						###
		
		return_list = []
		
		temp_list = [myear] # header: year 
		temp_list.extend(self.locations) # header: location names
		for element in sorted(avg_years, reverse=True):
			temp_list.append('%d-yr' % len(element)) # header: 1-yr, 2-yr, etc.
		return_list.append(temp_list)
			
		for name in sorted(data.keys()):
			temp_list = [name]
			for location in self.locations:
				try:
					value = data[name][location]
				except KeyError:
					value = None
				temp_list.append(value)
			# Discard a row (variety) that is all `None'
			if len([e for e in temp_list if e is not None]) > 1:
				for element in sorted(avg_years, reverse=True):
					key = '%d-yr' % len(element)
					try:
						value = data[name]['meta'][key]
					except KeyError:
						value = None
					temp_list.append(value)
				return_list.append(temp_list)
				
		# Discard a column (location) that is all `None'
		empty_columns = []
		for i in range(len(self.locations) - 1):# range of a negative integer returns an empty list
			empty = True
			for row in return_list[1::]: # skip header row
				empty = empty and (row[i+1] == None) # + 1 to skip past the variety name
			if empty:
				empty_columns.append(i+1)
		
		for i in sorted(empty_columns, reverse=True): # reverse transverse so indexes don't change on us	
			for row in return_list: # include header row
				del(row[i])
		
		# Sort the list by common locations, add lsd row between groups.
		# Note: this is the subset problem(?), which is NP-complete
		subsets = {}
		for row in return_list[1::]: # skip header row
			count = 0
			for element in row[1::]: # skip past variety name
				if element is not None:
					count += 1
			try:
				subsets[count].append(row)
			except KeyError:
				subsets[count] = [row]
		
		# Append lsd information for each subset
		for i in subsets.keys():
			lsd_list = ['LSD']
			len_locations_remaining = len(self.locations) - len(empty_columns)
			if (i > 1) and (len(subsets[i]) > 1):
				for j in range(len_locations_remaining): # each location
				### TODO: BRANNGG We need to use the db's stored LSD
					csum = 0.0
					squared_sum = 0.0
					count = 0
					for row in subsets[i]:
						if row[j+1] is not None:
							csum += float(row[j+1]) # skip past variety name
							squared_sum += float(row[j+1]) * float(row[j+1])
							count += 1
					if count > 0:
						lsd_list.append(None)
						#lsd_list.append(round(sqrt((squared_sum - (csum * csum)/count)/count), 2))
					else:
						lsd_list.append(None)
				### TODO: BRANNNGG We need to use the db's stored LSD
				for j in range(len(avg_years)): # each 1-yr, 2-yr etc. average
					location_treatment = {}
					for k in range(len_locations_remaining):
						location_treatment[k] = []
						for row in subsets[i]:
							if row[k+1] is not None:
								location_treatment[k].append(float(row[k+1]))
					for row in subsets[i]:
						if row[j+1] is not None:
							float(row[j+1])
							count += 1
					length = 0
					for sample in location_treatment.keys():
						length = len(location_treatment[sample])
						break
					balanced = True
					for treatment in location_treatment.values():
						if len(treatment) != length:
							balanced = False
					if balanced and j == 0:
						lsd_list.append(round(self.LSD(location_treatment.values(), .05),2))
					else:
						lsd_list.append(None)
			else:
				for j in range(len_locations_remaining): # each single location
					lsd_list.append(None)
				for j in range(len(avg_years)): # each 1-yr, 2-yr etc. average
					lsd_list.append(None)
					
			subsets[i].append(lsd_list)
		# Write our modified rows back to return_list
		return_list = [return_list[0]] # erase all rows
		for i in sorted(subsets.keys(), reverse=True): # put the rows back
			for row in subsets[i]:
				return_list.append(row)
			
		return return_list

class Locations_from_Zipcode_x_Radius:
	"""
	Utility class to return a list of locations located a specified
	distance from a specified point.
	"""
	
	zipcode = ''
	radius = 0.0
	
	def __init__(self):
		pass
	
	def __init__(self, zipcode, radius):
		"""
		Initializes internal data structures using the input zipcode and
		radius. 
		"""
		return self.populate(zipcode, radius)
	
	def populate(self, zipcode, radius):
		"""
		Calling populate() multiple times is supported, but untested. YMMV.
		"""
		# test if zipcode, radius are strings or floats
		try:
			self.zipcode = str(int(float(zipcode)))
		except ValueError:
			self.zipcode = ''
			
		try:
			self.radius = float(radius)
		except ValueError:
			self.radius = 100.0
	
	def fetch(self):
		"""
		Returns a list of locations within the specified search area.
		raises a `models.Zipcode.DoesNotExist'
		"""
		lat2_list = []
		lon2_list = []
		locations = []
		
		try:
			zipcode_query = models.Zipcode.objects.filter(zipcode=self.zipcode)
			zipcode_object = zipcode_query.get() # should only be one result
		except (ValueError, models.Zipcode.DoesNotExist) as instance:
			raise models.Zipcode.DoesNotExist(instance)
		if (self.radius < 1.0) and (self.radius > -1.0):
			locations = models.Location.objects.all()
		else:
			lat1 = float(zipcode_object.latitude) 
			lon1 = float(zipcode_object.longitude) # alternatively, we can call zipcode[0].longitude, but this might throw an IndexError
			lat1 = radians(lat1)
			lon1 = radians(lon1)
			R = 6378137.0 # Earth's median self.radius, in meters
			d = self.radius * 1609.344	 # in meters 
			# TODO: Search the max distance, then have the user decide what threshold to filter at after _all_ results returned.
			# TODO: have the Location objects grab default lat/long, not user entered
			bearing_list = [ 0.0, pi/2.0, pi, 3.0*pi/2.0 ] # cardinal directions
			for theta in bearing_list:
				lat2 = asin(sin(lat1)*cos(d/R) + cos(lat1)*sin(d/R)*cos(theta))
				lat2_list.append( degrees(lat2) )
				lon2 = lon1 + atan2(sin(theta)*sin(d/R)*cos(lat1), cos(d/R)-sin(lat1)*sin(lat2))
				lon2_list.append( degrees(lon2) )
				lon2 = (lon2+3.0*pi)%(2.0*pi) - pi	# normalise to -180...+180
			lat2_list = lat2_list[0::2] # discard non-moved points
			lon2_list = lon2_list[1::2] # both should contain two values, {min, max} lat/long
			
			locations = models.Location.objects.filter(
					zipcode__latitude__range=(str(min(lat2_list)), str(max(lat2_list)))
				).filter(
					zipcode__longitude__range=(str(min(lon2_list)), str(max(lon2_list)))
				)
			#TODO: We just searched a square, now discard searches that are > x miles away.
		
		
		return locations

class Trial_x_Location_x_Year:
	""" 
	Organizational class for our Trial_Entry x Location x Year data.
	Pass in a django queryset and the fields you want to consider for
	averaging.
	"""
	"""
	import rpy2.robjects as robjects # for def least_significant_difference()
	r = robjects.r
	r('library(mattikariluomandsuwheatdissem2011)')
	"""
	# A dictionary of variety_name to a year dictionary with Trial_Entry 
	# objects and their count.
	# {(name, location): {'year': [count, [trial_entry_objects]]}}
	_varieties = {}
	
	# private iterators
	_names = []
	_locations = []
	_years = []
	_include_fields = []
	
	def __init__(self):
		pass
				
	def __init__(self, trial_set, location_set = None, year_list = None, field_list = None):
		""" 
		Initializes with all elements matching field_list in query_set, or
		all elements if field_list is None. Optional parameters of locations
		and years may be included if known a priori.
		"""
		return self.populate(trial_set, location_set, year_list, field_list)
		
	def populate(self, trial_set, location_set = None, year_list = None, field_list = None):
		""" 
		Adds all elements matching field_list in query_set, or all elements 
		if field_list is None. Optional parameters of locations and years 
		may be included if known a priori.
		
		Calling populate() multiple times is supported, but untested. Your
		mileage may vary.
		"""
		self._varieties = {}
		self._names = []
		self._locations = []
		self._years = []
		self._include_fields = []
		# Bring location_set to a consistent state
		if location_set is None:
			for entry in query_set:
				location = str(entry.location.name)
				if location not in self._locations:
					self._locations.append(location)
		else:
			for entry in location_set:
				location = str(entry.name)
				if location not in self._locations:
					self._locations.append(location)
					
		# Bring year_list to a consistent state
		if year_list is None:
			for entry in query_set:
				year = str(entry.harvest_date.date.year)
				if year not in self._years:
					self._years.append(year)
		else:
			for year in year_list:
				if year not in self._years:
					self._years.append(year)
					
		# Bring field_list to a consistent state
		if field_list is None:
			for field in Trial_Entry._meta.fields:
				if (field.get_internal_type() == 'DecimalField' 
						or field.get_internal_type() == 'PositiveIntegerField' 
						or field.get_internal_type() == 'SmallIntegerField'
						or field.get_internal_type() == 'IntegerField'):
					self._include_fields.append(field) # only consider averageable data
		else:
			for field in field_list:
				if (field.get_internal_type() == 'DecimalField' 
						or field.get_internal_type() == 'PositiveIntegerField' 
						or field.get_internal_type() == 'SmallIntegerField'
						or field.get_internal_type() == 'IntegerField'):
					if field in models.Trial_Entry._meta.fields:
						self._include_fields.append(field) # ensure the user passed in good data
		
		# Initialize our inner data structures
		for entry in trial_set:
			name = str(entry.variety.name) # force evaluation
			location = str(entry.location.name) 
			year = str(entry.harvest_date.date.year)
			
			self._names.append(name)
			
			try:
				self._varieties[name]['count'] += 1
			except KeyError: # initialize and add the first value
				self._varieties[name] = {'count': 1}

			try:
				self._varieties[name][location]['count'] += 1
			except KeyError:
				self._varieties[name][location] = {'count': 1}

			try:
				self._varieties[name][location][year]['count'] += 1
				self._varieties[name][location][year]['entries'].append(entry)
			except KeyError: 
				self._varieties[name][location][year] = {'count': 1, 'entries': [entry]}
		
	def _most_recent_years_with_sufficient_data(self, var_key, loc_key, n_list = None):
		""" 
		Query for the most recent year that has sufficient data to post a 
		result using the variety_name. 
		
		This currently just returns the most recent year in the set, but in 
		the future it may be wise to check if the most recent year adversely
		affects a variety's ranking merely because only one trial result has
		been input insofar.
		
		Raises: KeyError
		"""
		if n_list is None:
			n_list = [1]
		
		return_list = []
		
		for element in self._varieties[var_key][loc_key].keys():
			if (element != 'count') and (element != 'entries'):
				return_list.append(element)

		#TODO: n_list isn't being treated properly, consider n_list=[1,3,4]

		# Returns a list with the first element(s) of a sort-descending list			
		# Remember to `try/except KeyError' when calling this function.
		return sorted(return_list, reverse=True)[:max(n_list):]
	
	def _get(self):
		""" 
		Return all data held in this object.
		"""
		return self._varieties
	
	def _get_recent(self, n_list = None):
		"""
		Return the data matching a list of variety_names in this object that
		is most recent in year, and has sufficient data in that year. If
		n_list is none, the most recent year is returned. If variety_x_location_list is
		None, all recent data are returned. An optional list of field names
		filters by those field names.
		"""
		data = self._get()
		
		recent_dict = {}
		for name in data.keys():
			recent_dict[name] = data[name]
			for location in data[name].keys():
				if location != 'count':
					years = self._most_recent_years_with_sufficient_data(name, location, n_list)
					years.append('count') # don't want to delete the accounting field
					for year in recent_dict[name][location].keys():
						if year not in years:
							del recent_dict[name][location][year]
							recent_dict[name][location]['count'] -= 1
		
		return recent_dict
	
	def _get_recent_ranked(self, n_list = None):
		"""
		Returns a list of dictionaries ranked by number of locations x years
		per variety, filtered first by date such that the n_list most recent
		years are considered.
		"""
		
		data = self._get_recent(n_list)
		
		rank_list = []
		rank_dict = {}
		
		for name in data.keys():
			try:
				rank_dict[data[name]['count']].update({name: data[name]})
			except KeyError:
				rank_dict[data[name]['count']] = {name: data[name]}
		
		maxrank = max(rank_dict.keys())
		rank_list = range(maxrank)
		
		for i in rank_list:
			rank_list[i] = {} # ensure empty dictionaries 
		
		for i in rank_dict.keys():
			#rank_list[i-1] = rank_dict[i] # smallest rank first
			rank_list[maxrank - i] = rank_dict[i] # largest rank first
		"""
		first_dict = {}
		rank_dict = {}
		last_dict = {}
		
		# rank 0, each name with their locations
		for name in data.keys():
			print("%s: %d" % (name, data[name]['count']))
			if name != 'count':
				first_dict[name] = set()
				for location in data[name].keys():
					if location != 'count':
						for year in data[name][location].keys():
							if year != 'count':
								first_dict[name].add((location,year))
		rank_dict = first_dict
		rank_list.append(rank_dict)

		# rank 1, pairs of names with their common locations
		last_dict = first_dict
		rank_dict = {}
		for name in last_dict.keys():
			for oname in first_dict.keys():
				if oname != name:
					locations = last_dict[name].union(first_dict[oname])
					if len(list(locations)) > 0:
						nlist = [name,oname]
						nlist.sort()
						rank_dict[tuple(nlist)] = locations
		rank_list.append(rank_dict)
		
		# rank 2
		last_dict = rank_dict
		rank_dict = {}
		for nametuple in last_dict.keys():
			for oname in first_dict.keys():
				if oname not in nametuple:
					locations = last_dict[nametuple].union(first_dict[oname])
					if len(list(locations)) > 0:
						nlist = list(nametuple)
						nlist.append(oname)
						nlist.sort()
						rank_dict[tuple(nlist)] = locations
		rank_list.append(rank_dict)
		
		# rank 3
		last_dict = rank_dict
		rank_dict = {}
		for nametuple in last_dict.keys():
			for oname in first_dict.keys():
				if oname not in nametuple:
					locations = last_dict[nametuple].union(first_dict[oname])
					if len(list(locations)) > 0:
						nlist = list(nametuple)
						nlist.append(oname)
						nlist.sort()
						rank_dict[tuple(nlist)] = locations
		rank_list.append(rank_dict)
		
		# rank 4
		last_dict = rank_dict
		rank_dict = {}
		for nametuple in last_dict.keys():
			for oname in first_dict.keys():
				if oname not in nametuple:
					locations = last_dict[nametuple].union(first_dict[oname])
					if len(list(locations)) > 0:
						nlist = list(nametuple)
						nlist.append(oname)
						nlist.sort()
						rank_dict[tuple(nlist)] = locations
		rank_list.append(rank_dict)
		"""

		return rank_list
	
	def _get_averages(self, n_list = None, field_list = None):
		"""
		Given a list of the number of dates to go back (e.g. [1,2,3] for the
		1-yr, 2-yr, and 3-yr averages), return those averaged data. An 
		optional list of varieties filers by those varieties, and an 
		optional list of fieldnames filters by those fieldnames.

		The returned dictionary tags the keys of the averaged items, 
		prepending `1-yr-avg-' `2-year-avg-' etc. based on the values in 
		n_list.
		"""
		
		#TODO: work this into the main for-loop below.
		def custom_sort(trial_set, year_list, location_list):
			return_list = []
			pre_sort = {}
			year_list = sorted(year_list, reverse=True)

			for entry in trial_set:			
				year = str(entry.harvest_date.date.year)
				#TODO: sort by year (done), then location
				location = str(entry.location.name)
				try:
					pre_sort[year][location].append(entry)
				except KeyError:
					try:
						pre_sort[year][location] = [entry]
					except KeyError:
						pre_sort[year] = {}
						pre_sort[year][location] = [entry]
	
			for year in year_list:
				for location in sorted(pre_sort[year].keys()):
					pre_sort[year][location].sort()
					return_list.extend(pre_sort[year][location])
				
			return return_list
		
		def number_of_environments(dictionary):
			return_value = 0
			for name in dictionary.keys():
				if name != 'count':
					try:
						return_value = len(dictionary[name]['entries'])
						break
					except KeyError:
						continue
			return return_value
			
		def least_significant_difference(field_dictionary):
			LSD_dict = {}
			"""
			for key in field_dictionary:
				count = field_dictionary[key][0]
				value_list = field_dictionary[key][1]
				location_list = field_dictionary[key][2]
				test = len(value_list)
				
				if test == len(location_list) and (test == count): # paranoia
					try:
						y = robjects.FloatVector(value_list)
						trt = robjects.FactorVector(location_list)
						robjects.globalenv['y'] = y
						robjects.globalenv['trt'] = trt
						model = r('aov(y~trt)')
						df = r['df.residual'](model)
						MSerr = r['deviance'](model).ro / df[0]
						LSD_dict[key] = r['LSD.return'](y, trt, df, MSerr)[0]
					except:
						break
			
			"""
			return LSD_dict
			
		
		if field_list is None: # paranoia
			field_list = self._include_fields

		data_list = self._get_recent_ranked(n_list)
		averaged = range(len(data_list))
		
		j = 0
		for rank_dict in data_list:
			avg_dict = {}
			avg_dict['lsd'] = {}
			for name in rank_dict.keys():
				avg_dict[name] = {}
				all_years = set()
				all_locations = []
				for location in rank_dict[name].keys():
					if location != 'count':
						all_locations.append(location) # TODO: this is a candidate to be stored on populate()
						for year in rank_dict[name][location].keys():
							if year != 'count':
								all_years.add(year) # TODO: this is a candidate to be stored on populate()
				all_years = sorted(list(all_years))
				
				# populate years, a dictionary of {'prefix': [2000, 1999, ...], ...}
				years = {}
				i = 0
				for year in all_years: # *must* be done on a per variety basis
					prefix = "%d_yr_avg_" % (len(all_years) - i)
					for prev_prefixes in years.keys():
						years[prev_prefixes].append(year) # append this year to each existing element
					years[prefix] = [year] # make a list containing only this year
					i += 1

				# populate avg_dict, a dictionary {'name': {'prefix'+'field': float, ...}, ...}
				for location in all_locations:
					for year in all_years:
						for prefix in years.keys():
							if year in years[prefix]:
								try:
									entries = rank_dict[name][location][year]['entries']
								except KeyError:
									continue # skip to next iteration of `for prefix in years.keys()'
								for entry in entries:
									try:
										if entry not in avg_dict[name]['entries']:
											avg_dict[name]['entries'].append(entry)
									except KeyError:
										avg_dict[name]['entries'] = [entry]
									for field in field_list:
										fieldname = field.name
										key = "%s%s" % (prefix, fieldname)
										value = getattr(entry, fieldname)
										if value != None:
											try:
												avg_dict[name][key][0] += 1 # count
												avg_dict[name][key][1].append(value) # running total
												avg_dict[name][key][2].append(location)
												avg_dict['lsd'][key][0] += 1 # doesn't get reset for each name
												avg_dict['lsd'][key][1].append(value) 
												avg_dict['lsd'][key][2].append(location)
											except KeyError:
												avg_dict[name][key] = [1,[value],[location]]
												avg_dict['lsd'][key] = [1,[value],[location]]
										
				#Either we update the average each insertion, or we iterate over the dict again and calculate the averages...
				for key in avg_dict[name].keys():
					if key != 'entries':
						avg_dict[name][key] = round(sum(avg_dict[name][key][1]) / avg_dict[name][key][0], 2)
				
				#avg_dict['count'] = rank_dict[name]['count']	
				avg_dict[name]['entries'] = custom_sort(avg_dict[name]['entries'], all_years, all_locations)
			
			if avg_dict:
				avg_dict['lsd'] = least_significant_difference(avg_dict['lsd'])
				avg_dict['count'] = number_of_environments(avg_dict)
			
			averaged[j] = avg_dict
			j += 1
		
		return averaged

	def fetch(self, n_list = None, field_list = None):
		"""
		Main accessor method for this class. The optional parameters n_list 
		and field_list are used to return multi-year averaged fields, while 
		fields not in field_list are returned as 1 (last) year averages. 
		When n_list is not supplied, a 1 year average is assumed. If no 
		field_list is supplied, results are calculated over all fields.
		
		Returns a ranked list of dictionaries [ {variety_name: { entries: [objects], 1-yr-avg-fieldname: value, ... } }, ... ]
		where the ranking is determined by number of locations for that variety.
		"""
		if field_list is None:
			field_list = []
			exclusion_fields = self._include_fields
		else:
			exclusion_fields = list(set(self._include_fields).difference(set(field_list)))
		
		
		a = self._get_averages([1], exclusion_fields)
		b = self._get_averages(n_list, field_list)
		
		for i in range(len(a)):
			for key in a[i].keys():
				try:
					access = b[i]
				except IndexError:
					continue
				try:
					a[i][key].update(b[i][key])
				except KeyError:
					pass
				except AttributeError: # raised when trying to access prefix_count
					pass
					
		return a
