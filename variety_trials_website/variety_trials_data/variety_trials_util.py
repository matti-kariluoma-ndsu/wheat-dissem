from variety_trials_data.models import Trial_Entry #, Date
from variety_trials_data import models
from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv
import copy

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
		degrees_freedom_of_error = (n-1)*(k-1)
		
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
						self.lsds[year][location].append(value)
					except KeyError:
						try:
							self.lsds[year][location] = [value]
						except KeyError:
							self.lsds[year] = {}
							self.lsds[year][location] = [value]
		
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
				avg_value = round(sum(sum_list) / len(sum_list), 1)
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
							data[name]['meta'][key] = round(data[name]['meta'][key] / count, 1)
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
				subsets[(count, 0)].append(row) # key is (order, minor order)
			except KeyError:
				subsets[(count, 0)] = [row]
		
		# Go through each subset and break into more subsets. Each new
		# subset increases the minor order by 1, but the order is unchanged.
		
		all_subsets_found = False
		while not all_subsets_found:
			all_subsets_found = True # TODO: repeat until all have been sorted into coherent sets.
			for (i, mi) in subsets.keys():
				if len(subsets[(i, mi)]) > 0:
					first_row = subsets[(i, mi)][0]						
					matching = []
					unmatching = []
					for row in subsets[(i, mi)]:
						all_match = True
						for j in range(len(row)):
							all_match = all_match and ((row[j] is None and first_row[j] is None) or (row[j] is not None and first_row[j] is not None))
						if all_match:
							matching.append(row)
						else:
							unmatching.append(row)
					subsets[(i, mi)] = matching
					if len(unmatching) > 0:
						subsets[(i, mi + 1)] = unmatching
		
		
				
		# put all elements from higher-order groups into lower-order groups,
		# putting 'None' into non-common locations.
		subsets_to_copy = {} # can't add to the item we're iterating through
		for (i, mi) in subsets.keys():
			blanks = [] # indexes of each empty column
			if len(subsets[(i, mi)]) > 0:
				for pos in range(len(subsets[(i, mi)][0])): # iterate through each column in the first row
					if subsets[(i, mi)][0][pos] is None:
						blanks.append(pos)
			for (j, mj) in subsets.keys():
				if j > i: # add all from higher-order groups.
					for row in subsets[(j, mj)]:
						new_row = copy.copy(row) # a shallow copy, will not follow refs
						doAppend = True
						for pos in range(len(row)):
							if pos in blanks:
								new_row[pos] = None
							if (new_row[pos] is None) and (pos not in blanks):
								doAppend = False
								break
						if doAppend:
							try:
								subsets_to_copy[(i, mi)].append(new_row)
							except KeyError:
								subsets_to_copy[(i, mi)] = [new_row]
		
		for (i, mi) in subsets_to_copy.keys():
			for row in subsets_to_copy[(i, mi)]:
				subsets[(i, mi)].append(row)
		
		# Sort each group alphabetically
		for (i, mi) in subsets.keys():
			print "alpha"
			sorted_variety_names = []
			for row in subsets[(i, mi)]:
				if len(row) > 1:
					sorted_variety_names.append(row[0])
			sorted_variety_names.sort()
			new_ordering = []
			for name in sorted_variety_names:
				for row in subsets[(i, mi)]:
					if len(row) > 1:
						if row[0] == name:
							new_ordering.append(row)
			subsets[(i, mi)] = new_ordering
		
		# Append lsd information for each subset
		for (i, mi) in subsets.keys():
			lsd_list = ['LSD']
			len_locations_remaining = len(self.locations) - len(empty_columns)
			if (i > 1) and (len(subsets[(i, mi)]) > 1):
				for location in return_list[0][1:len_locations_remaining+1:]: # each location
					try:
						lsds = self.lsds[myear][location]
					except KeyError:
						lsds = []
					if len(lsds) > 1:
						lsd_list.append(lsds[0])
					else:
						lsd_list.append(None)
					
						
				for j in range(len(avg_years)): # each 1-yr, 2-yr etc. average
					location_treatment = {}
					for k in range(len_locations_remaining):
						location_treatment[k] = []
						for row in subsets[(i, mi)]:
							if row[k+1] is not None:
								location_treatment[k].append(float(row[k+1]))
					for row in subsets[(i, mi)]:
						if row[j+1] is not None:
							float(row[j+1])
							count += 1
					
					for key in location_treatment.keys():
						if len(location_treatment[key]) == 0:
							del(location_treatment[key])
					length = 0
					for sample in location_treatment.keys():
						length = len(location_treatment[sample])
						break
					balanced = True
					for treatment in location_treatment.values():
						if len(treatment) != length:
							balanced = False
					if balanced and j == 0:
						#print location_treatment.values()
						lsd_list.append(round(self.LSD(location_treatment.values(), .05),2))
					else:
						lsd_list.append(None)
			else:
				for j in range(len_locations_remaining): # each single location
					lsd_list.append(None)
				for j in range(len(avg_years)): # each 1-yr, 2-yr etc. average
					lsd_list.append(None)
					
			subsets[(i, mi)].append(lsd_list)
		
		
		# Write our modified rows back to return_list
		return_list = [return_list[0]] # erase all rows
		for (i, mi) in sorted(subsets.keys(), reverse=True): # put the rows back
			for row in subsets[(i, mi)]:
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
