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
	year = 0 # current year
	all_varieties = True # whether to use all varieties, or the ones in "varieties"
	# also used to show different data for varieties/locations view.
	# TODO: pull out into common-function call to make this boolean's use
	# more clear, instead of needing to search for where it's used.
	
	years = [] #year "y"
	locations = [] # location "l"
	varieties = [] # variety "v"
	
	# all data
	entries = {} # {(l,v): {y: [43.2, ...] y: [34.2], ...}, ...}
	# data (with duplicates) separated into balanced subsets
	groups = {} # {(major,minor): [v, ...], ...}
	# lsds of the data
	lsds = {} # {(l,y): [12.2, ...], ...}
	
	
	def __init__(self):
		pass

	def __init__(self, entries, field, years, pref_year, varieties_list):
		"""
		Initializes internal data structures using the an input list of 
		entries, a field to filter on, and the years to include.
		"""
		if len(varieties_list) > 0:
			self.all_varieties = False
			self.varieties = varieties_list #TODO: check these names
		else:
			self.all_varieties = True
			self.varieties = []
			
		return self.populate(entries, field, years, pref_year)

	def LSD(self, response_to_treatments, probability):
		"""
		A stripped-down reimplementation of LSD.test from the agricoloae
		package. (http://cran.r-project.org/web/packages/agricolae/index.html)
		
		Calculates the Least Significant Difference of a multiple comparisons
		trial, over a balanced dataset.
		"""
			
		def qnorm(probability):
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
				
		def qt(probability, degrees_of_freedom):
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
					x = qnorm(P*0.5)
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
		
		Tprob = qt(probability, degrees_freedom_of_error)
			
		LSD = Tprob * sqrt(2.0 * mean_squares_of_error / k)

		return LSD
		
	def populate(self, entries, field, years, pref_year):
		"""
		"""
		self.field = {'name':''}
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
		for entry in entries:
			year = int(entry.harvest_date.date.year)
			if year in self.years:
				location = str(entry.location.name)
				self.locations.append(location)
				
				name = str(entry.variety.name)
				if self.all_varieties: # if we are using all varieties, add this variety to our list
					self.varieties.append(name)
					
				if name in self.varieties:
					# store our field's value
					try:
						value = getattr(entry, fieldname)
					except AttributeError:
						value = None
					if value != None:
						try:
							self.entries[(location, name)][year].append(value)
						except KeyError:
							try:
								self.entries[(location, name)][year] = [value]
							except KeyError:
								self.entries[(location, name)] = {}
								self.entries[(location, name)][year] = [value]
						
						# store the lsd from this entry
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
							self.lsds[(location, year)].append(value)
						except KeyError:
							self.lsds[(location, year)] = [value]
							
		# remove duplicates
		self.locations = sorted(list(set(self.locations)))
		self.varieties = sorted(list(set(self.varieties)))
		
	def fetch(self):
		"""
		Returns a list of lists, suitable for a tabular layout. The first
		list contains the year and location names, and each other list 
		begins with the variety name, followed by the values correpsonding 
		with the header.
		
		Year Loc1 Loc2 Loc3 ...
		Var1 *    *    *    ...
		Var2 *    *    *    ...
		...  ...  ...  ...  ...
		"""
		
		return_list = []
				
		# Discard a column (location) that is all `None'
		empty_locations = []
		for l in self.locations:
			empty = True
			for v in self.varieties:
				try:
					empty = empty and (self.entries[(l,v)][self.year] is None)
					if not empty:
						break
				except KeyError:
					pass
			if empty:
				empty_locations.append(l)
		
		self.locations = sorted(list(
					set(self.locations).difference(
					set(empty_locations))
			))
		
		# initialize the groups variable
		self.groups = {}
		for i in range(len(self.locations)):
			self.groups[(i+1,0)] = [] # (major, minor)
		
		# Sort by common locations
		# Note: this is the subset problem(?), which is NP-complete
		
		# for each variety, count the number of locations we have data
		for v in self.varieties:
			count = 0
			for l in self.locations:
				try:
					if self.entries[(l,v)][self.year] is not None:
						count += 1
				except KeyError:
					pass
			if (count > 0): # discard rows with no data
				self.groups[(count,0)].append(v)
		
		def break_into_subsets():
			# Go through each subset and break into more subsets.
			new_subsets = {}
			for key in self.groups.keys():
				variety_subset = self.groups[key]
				locations = []
				if (len(variety_subset) > 1): # only try to subdivde sets that have two or more members
					v = variety_subset[0]
					for l in self.locations:
						try:
							if self.entries[(l,v)][self.year] is not None:
								locations.append(l)
						except KeyError:
							pass
					new_subset = []
					for v in variety_subset[1::]: # skip past variety_subset[0]
						balanced = True
						for l in locations: # only iterate over locations in variety_subset[0]
							try:
								balanced = balanced and self.entries[(l,v)][self.year] is not None
							except KeyError:
								balanced = False
						if not balanced:
							new_subset.append(v)
					if len(new_subset) > 0:
						new_subsets[key] = new_subset # save result for post-processing
				
			# insert the subsets into self.groups
			for key in new_subsets.keys():
				self.groups[key] = sorted(list(
						set(self.groups[key]).difference(
						set(new_subsets[key]))
				))
				new_key = (key[0], key[1]+1) # increase the minor order by one
				self.groups[new_key] = new_subsets[key]
				
		for num_times in range(3): # TODO: hard-coded numeric value
			break_into_subsets()
		
		# intialize a dictionary of orders
		major_orders = {}
		for key in self.groups.keys():
			try:
				major_orders[key[0]].append(key)
			except KeyError:
				major_orders[key[0]] = [key]
				
		if self.all_varieties: # if we are the locations view
			# put all elements from higher-order groups into lower-order groups,
			# putting 'None' into non-common locations.
			for order in major_orders.keys(): # reverse-traverse
				for key in self.groups.keys():
					if key[0] < order: # if this group's order is smaller than another, add all from the higher order
						for larger_group_key in major_orders[order]:
							for v in self.groups[larger_group_key]:
								self.groups[key].append(v)
		else: # if we are the varieties view
			# find the biggest group(s) representing the chosen varieties, then delete the rest
			ordered_groups_keys = sorted(self.groups.keys(), reverse=True)
			groups_keys_save = []
			
			for v in self.varieties:
				ordered_groups_pos = 0
				while ordered_groups_pos < len(ordered_groups_keys):
					if v in self.groups[ordered_groups_keys[ordered_groups_pos]]:
						groups_keys_save.append(ordered_groups_keys[ordered_groups_pos])
						break # break the while loop
					ordered_groups_pos += 1
			# delete non-matching
			for key in self.groups.keys():
				if key not in groups_keys_save:
					del self.groups[key]
				
		
		# make a list of years to average over
		avg_years = []
		
		# find all years before the current year, inclusive
		def f(x): return (x <= self.year)
				
		# construct a list for n-yr averaging e.g. [[2010], [2010, 2009], [2010, 2009, 2008]]
		for year in sorted(filter(f, self.years)):
			for element in avg_years:
				element.append(year)
			avg_years.append([year])		
			
		avg_years = sorted(avg_years, reverse=True) # order them 1-yr, 2-yr, ...
		
		# construct rows from our data
		
		# append header row
		head_row = [self.year] # first (row, column) value is the current year
		for l in self.locations:
			head_row.append(l)
		# constuct column headers for n-yr averaging
		for element in avg_years:
			n_yr = '%d-yr' % len(element)
			head_row.append(n_yr);
		return_list.append(head_row) # append first row
		
		# construct the rest of the rows
		for key in sorted(self.groups.keys(), reverse=True): # for each subset
			subset_list = []
			locations = []
			
			# define the locations that need to be printed for this subset
			if len(self.groups[key]) > 0:
				variety = self.groups[key][0]
				for l in self.locations:
					try:
						if self.entries[(l,variety)][self.year] is not None:
							locations.append(l)
					except KeyError:
						pass
			
				# add the values for this subset
				for v in sorted(self.groups[key]): # Sort each group alphabetically
					temp_row = [v]
					append_me = True
					one_year_sums = []
					
					for l in self.locations:
						if l not in locations: # ensure all subgroups only show data for common locations
							temp_row.append(None)
						else:
							try:
								values = self.entries[(l,v)][self.year]
								value = round(sum(values)/len(values), 2)
								temp_row.append(value)
								one_year_sums.append(value) # will not contain None
							except KeyError:
								if l in locations: # this variety is from a higher-order set, but does not have data for one of our common locations
									append_me = False
									break
								temp_row.append(None)
								
					if append_me:
						if len(one_year_sums) > 1: # if we have two or more datapoints
							# append 1-yr avg
							temp_row.append(round(sum(one_year_sums)/len(one_year_sums), 2))
						else:
							append_me = False # cause the 2-yr,... to short-circuit
							temp_row.append(None)
						# append 2-yr, ... avgs
						for years_to_average in avg_years[1::]: # skip past 1-yr avg
							sum_list = []
							for year in years_to_average:
								if append_me: # only continue while there are no errors
									if year != self.year: # we already retrieved the data for this year
										for l in locations:
											try:
												values = self.entries[(l,v)][year]
												value = round(sum(values)/len(values), 2)
												sum_list.append(value)
											except KeyError:
												append_me = False
												break
									else:
										sum_list.extend(one_year_sums)
							
							if append_me and len(sum_list) > 1:
								temp_row.append(round(sum(sum_list)/len(sum_list), 2))
							else:
								temp_row.append(None)
						subset_list.append(temp_row)
						
				# prepare a list to compute lsd on, by removing all "None" from this subset
				lsd_list = []
				for row in subset_list:
					not_none = []
					for cell in row[1:len(self.locations)+1:]: # skip past first column (the variety name), and do not include n-yr avgs
						if cell is not None:
							not_none.append(cell)
					if len(not_none) > 1:
						lsd_list.append(not_none)
				# append the calculated lsd row for this subset
				
				temp_row = ["LSD"]
				for l in self.locations:
					if l in locations:
						try:
							temp_row.append(max(self.lsds[(l, self.year)])) #TODO: smarter logic needed
						except KeyError:
							temp_row.append(None)
					else:
						temp_row.append(None)
				if len(lsd_list) > 0:
					# append 1-yr lsd
					try:
						value = round(self.LSD(response_to_treatments=lsd_list, probability=0.05), 2)
					except:
						value = None
					temp_row.append(value)
				else:
					temp_row.append(None)
				# append 2-yr, ... lsds
				append_me = True # reset error flag
				for years_to_average in avg_years[1::]: # skip past 1-yr avg
					multiple_year_lsd_list = []	
					for v in sorted(self.groups[key]): #TODO: we iterated through this already...
						variety_across_years = []
						for year in years_to_average:						
							if append_me:
								for l in locations:
									try:
										values = self.entries[(l,v)][year]
										value = round(sum(values)/len(values), 2)
																	
									except KeyError:
										append_me = False
										break
						multiple_year_lsd_list.append(variety_across_years)
					
					if append_me:
						try:
							value = round(self.LSD(response_to_treatments=multiple_year_lsd_list, probability=0.05), 2)
						except:
							value = None
						temp_row.append(value)
					else:
						temp_row.append(None)
				subset_list.append(temp_row)
					
				return_list.extend(subset_list) # append the lists inside subset_list to return_list

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
