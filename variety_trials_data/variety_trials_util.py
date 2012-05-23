from variety_trials_data.models import Trial_Entry #, Date
from variety_trials_data import models
from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv
from itertools import chain
from operator import attrgetter
import copy
	
class LSD_Calculator:
	"""
	Utility class to return a list of lists for output,
	and a list of lists of lsd data corresponding.
	"""
	
	field = {'name':''} # default value such that we return nothing if a bogus field is given
	year = 0 # current year
	all_varieties = True # whether to use all varieties, or the ones in "varieties"
	# also used to show different data for varieties/locations view.
	# TODO: pull out into common-function call to make this boolean's use
	# more clear, instead of needing to search for where it's used.
	
	
	locations = [] # location "l"
	varieties = [] # variety "v"
	years = [] #year "y"
	
	location_indexes = {}
	year_indexes = {}
	
	# all data
	entries = {} # {v: [[43.2, ...], [34.2, ...], [45.2, ...]], ...}
	# lsds of the data
	lsds = {} # {(l,y): [12.2, ...], ...}
	# (count, avg) of the data at each variety x year
	entry_avgs = {} # {v: [(9, 43.5), (9, 45.3), (10, 52.2)], ...}
	# data (with duplicates) separated into balanced subsets
	groups = {} # {(major,minor): [v, ...], ...}
	# same as above w/ common locations for that group
	groups_loc = {} # {(major,minor): [l, ...], ...}

	def __init__(self, entries, locations, varieties, years, pref_year, field):
		"""
		Initializes internal data structures using the an input list of 
		entries, a field to filter on, and the years to include.
		"""
		
		return self.populate(entries, locations, varieties, years, pref_year, field)

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
		
		treatment_means = {}
		for i in range(n): # n == len(trt)
			total = 0.0
			for j in range(k):
				total += float(trt[i][j])
			treatment_means[i] = total/k
			
		block_means = {}
		for j in range(k):
			total = 0.0
			for i in range(n):
				total += float(trt[i][j])
			block_means[j] = total/n
		
		grand_mean = sum(treatment_means.values()) / float(n)
		
		# SSE is the Error Sum of Squares
		# TODO: what is the difference between type I and type III SS? (http://www.statmethods.net/stats/anova.html)
		SSE = 0.0
		for i in range(n): # n == len(trt)
			for j in range(k):
				SSE += (float(trt[i][j]) - treatment_means[i] - block_means[j] + grand_mean)**2.0
		
		mean_squares_of_error = SSE / degrees_freedom_of_error
		
		Tprob = qt(probability, degrees_freedom_of_error)
			
		LSD = Tprob * sqrt(2.0 * mean_squares_of_error / k)

		return LSD
		
	def populate(self, entries, locations, varieties, years, pref_year, field):
		"""
		For each variety, store three lists, one for each year.
		order by location, and place None when there is no data.
		"""
		
		# serialize our inputs
		"""
		from django.core import serializers
		prefix="58501_100_"
		JSONSerializer = serializers.get_serializer("json")()
		with open(prefix+"entries.json", "w") as out:
			JSONSerializer.serialize(entries, stream=out)
		with open(prefix+"locations.json", "w") as out:
			JSONSerializer.serialize(locations, stream=out)
		with open(prefix+"varieties.json", "w") as out:
			JSONSerializer.serialize(varieties, stream=out)
		
		import json
		with open(prefix+"years.json", "w") as out:
			json.dump(years, out)
		with open(prefix+"pref_year.json", "w") as out:
			json.dump(pref_year, out)
		with open(prefix+"field.json", "w") as out:
			json.dump({"name":field.name}, out)
		"""
		# init to empty
		self.location_indexes = {}
		self.year_indexes = {}
		self.entries = {}
		self.groups = {}
		self.groups_loc = {}
		self.lsds = {}
		
		self.year = pref_year
		self.field = field
		
		# order years properly
		self.years = sorted(years, reverse=True)
		
		# test if year is in the list of years
		if self.year not in self.years:
			self.year = max(self.years)
		
		
		# order locations, varieties
		self.locations = sorted(locations, key=attrgetter('name'))
		self.varieties = sorted(varieties, key=attrgetter('name'))
		
		#
		# initialize self.entries, self.lsds
		#
		
		# initialize self.location_indexes
		self.location_indexes = dict(zip(self.locations, range(len(self.locations))))
		l_i = self.location_indexes
		
		#initialize self.year_indexes
		
		self.year_indexes = dict(zip(self.years, range(len(self.years))))
		y_i = self.year_indexes
		
		for v in varieties:
			self.entries[v] = [[None for l in self.locations] for y in self.years]
		for l in locations:
			self.lsds[l] = [None for y in self.years]
		
		# grab data pertaining to our field
		fieldname = self.field.name
		for entry in entries:
			year = int(entry.harvest_date.date.year)
			if year in self.years:
				location = entry.location
				v = entry.variety
							
				if v in self.varieties:
					# store our field's value
					try:
						value = getattr(entry, fieldname)
					except AttributeError:
						value = None
					if value is not None:
						y = y_i[year]
						l = l_i[location]
						self.entries[v][y][l] = float(value)
						
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
						
						self.lsds[location][y] = value
		
	def fetch(self, reduce_to_one_subset=False):
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
		
		# Utility functions to average our variety x year data
		
		"""
		def add_not_none(x,y):
		"""
		"""
			It is very important to prepend 0 to any iterable passed into
			this function, since we don't check if x is not None, only y.
			
			If using the reduce() function, chain([0], data) is a good way
			to prepend a zero to an iterable: 
			
			i.e. data_sum = reduce(add_if_not_none, chain([0], data))
		"""
		"""
			if y: # if y is not None and y is not 0
				return x+y
			else:
				return x
		"""
		def len_not_none(l):
			"""
			Returns the length of a list that is None padded.
			"""
			return len([i for i in l if i is not None])	
		
		#
		# Sort by common locations
		# Note: this is the subset problem(?), which is NP-complete
		#
		
		
		# populate groups with a list of all varieties having n locations
		cy_i = self.year_indexes[self.year] #current_year_index
		
		l_indexes = self.location_indexes
		
		for entry in self.entries.items():
			count = [0,0,0] # TODO: _Heavily_ assumes we are only using the last three years
			for y in self.year_indexes.values():
				count[y] = len_not_none(entry[1][y])
			if count[0] or count[1] or count[2]:
				key = (tuple(count), 0)
				if key in self.groups:
					self.groups[key].append(entry[0]) # .append(entry.key)
				else:
					self.groups[key] = [entry[0]]
				
		# populate an initial guess on the locations in each group
		for key in self.groups:
			v = self.groups[key][0]
			self.groups_loc[key] = [None, None, None] # _heavily_ assumes we are only dealing with 3 years
			for y in self.year_indexes.values():
				self.groups_loc[key][y] = [l for l in self.locations if self.entries[v][y][l_indexes[l]] is not None]
		
		
		def break_into_subsets():
			# Go through each subset and break into more subsets.
			new_subsets = {}
			for entry in self.groups.items():
				key = entry[0]
				
				variety_subset = entry[1]
				if (len(variety_subset) > 1): # only try to subdivde sets that have two or more members
					v = variety_subset[0]
					
					"""
					locations = []
					for l in l_indexes:
						if self.entries[v][cy_i][l] is not None:
							locations.append(l)
					"""
					#locations = [l for l in l_indexes.values() if self.entries[v][cy_i][l] is not None]
					
					for y in self.year_indexes.values():
						if key in self.groups_loc.keys():
							locats = self.groups_loc[key][y]
						else: # TODO: We should never need to take this else branch
							locats = [l for l in self.locations if self.entries[v][y][l_indexes[l]] is not None]

						new_subset = []
						for v in variety_subset[1::]: # skip past variety_subset[0]
							balanced = True
							for l in locats: # only iterate over locations in variety_subset[0]
								balanced = balanced and self.entries[v][y][l_indexes[l]] is not None
							if not balanced:
								new_subset.append(v)
					if len(new_subset) > 0:
						new_subsets[key] = new_subset # save result for post-processing
				
			# insert the subsets into self.groups
			for entry in new_subsets.items():
				key = entry[0]
				self.groups[key] = list(
						set(self.groups[key]).difference(
						set(new_subsets[key]))
				)
				new_key = (key[0], key[1]+1) # increase the minor order by one
				self.groups[new_key] = new_subsets[key]
				v = self.groups[new_key][0]
				
				# which locations are in this new subset?
				self.groups_loc[new_key] = [None, None, None] # _heavily_ assumes we are only dealing with 3 years
				for y in self.year_indexes.values():
					self.groups_loc[new_key][y] = [l for l in self.locations if self.entries[v][y][l_indexes[l]] is not None]
		
		# make more subgroups, and update the locations for each new subgroup
		for num_times in range(3): # TODO: hard-coded numeric value
			break_into_subsets()
		
		#TODO: mayhap this check should be done before break_into_subsets()?
		if reduce_to_one_subset: # if we are the varieties view
			# find the biggest group(s) representing the chosen varieties, then delete the rest
			most_varieties = []
			max_len = max(map(len, self.groups.values()))
			for key in sorted(self.groups.keys(), reverse=True):
				if len(self.groups[key]) >= max_len:
					most_varieties.append(key)
			
			
			"""
			# for the groups that remain, delete the non-common locations until one subset remains
			init_locale = self.groups_loc[most_varieties[0]]
			common_locations = []
			for locations in init_locale:
				common_locations.extend(locations)
			common_locations = dict(zip(common_locations, common_locations)) # make a copy as a dictionary
			
			for key in most_varieties[1::]: # skip first
				for locations in self.groups_loc[key]:
					to_delete = []
					for location in common_locations:
						if location not in locations:
							to_delete.append(location)
					for location in to_delete:
						del common_locations[location]
			"""
			# commented out since we don't have that many 3-yr complete data
			
			# delete non-common locations with respect to the selected year
			init_locale = self.groups_loc[most_varieties[0]]
			common_locations = init_locale[cy_i]
			common_locations = dict(zip(common_locations, common_locations)) # make a copy as a dictionary
			
			for key in most_varieties[1::]: # skip first
				to_delete = []
				for location in common_locations:
					if location not in self.groups_loc[key][cy_i]:
						to_delete.append(location)
				for location in to_delete:
					del common_locations[location]
			
			# put all into one group
			del self.groups
			del self.groups_loc
			order = len(common_locations)
			self.groups[((order,order,order),0)] = list(self.varieties)
			self.groups_loc[((order,order,order),0)] = [list(common_locations), list(common_locations), list(common_locations)]# TODO: heavily assumes 3-yrs
		else: # if we are the locations view
			# Add all varieties from larger subsets to smaller subsets
			add_all_varieties_from_larger_subsets = False
			if add_all_varieties_from_larger_subsets:
				"""
				common_varieties = []
				common_buffer = []
				common_key = len(self.locations)
				for key in sorted(self.groups.keys(), reverse=True):
					if key[0] < common_key: # if we are less than the major order of the previous subset
						common_varieties.extend(common_buffer)
						common_buffer = []
					common_key = key[0] # the major order
					self.groups[key].extend(common_varieties)
					common_buffer.extend(self.groups[key])
				"""
				for key in sorted(self.groups.keys(), reverse=True):
					for lkey in [lesser_key for lesser_key in self.groups.keys() if lesser_key[0] <= key[0]]: # python does compares on tuples well
						if lkey is not key: # ignore the case where we are the same key
							self.groups[lkey].extend(self.groups[key])
							self.groups[lkey] = list(set(self.groups[lkey])) # remove duplicates
		
			
		#print self.groups
		#
		# make a list of years to average over
		#
		avg_years = []
		
		# find all years before the current year, inclusive
		def f(x): return (x <= self.year)
		
		# construct a list for n-yr averaging e.g. [[2010], [2010, 2009], [2010, 2009, 2008]]
		for year in sorted(filter(f, self.years)):
			for element in avg_years:
				element.append(year)
			avg_years.append([year])		
		
		avg_years = sorted(avg_years, reverse=True) # order them 1-yr, 2-yr, ...
		
		#
		# construct header rows
		#
		remove_non_common_locations_in_current_year = True
		
		# header row
		head_row = [self.year] # first (row, column) value is the current year
		
		# constuct column headers for n-yr averaging
		for element in avg_years:
			n_yr = '%d-yr' % len(element)
			head_row.append((n_yr, -1)) # tuple: (name, id)
		l_indexes_values = []
		if reduce_to_one_subset: # if we are the varieties view
			for l in sorted(self.groups_loc.values()[0][0], key=attrgetter('name')): ##TODO: Super-kludge
				l_indexes_values.append(l_indexes[l])
				head_row.append((l.name, l.id))
		else:
			if remove_non_common_locations_in_current_year:
				years_locations = []
				for key in self.groups_loc:
					years_locations.extend(self.groups_loc[key][cy_i])
				years_locations = list(set(years_locations))
				for l in sorted(years_locations, key=attrgetter('name')):
					l_indexes_values.append(l_indexes[l])
					head_row.append((l.name, l.id))
			else:
				for l in sorted(self.locations, key=attrgetter('name')):
					l_indexes_values.append(l_indexes[l])
					head_row.append((l.name, l.id))
		return_list.append(head_row) # append first row
		
		# the header between each group
		next_header = [('Variety', -1)]
		next_header.extend(head_row[1::])
		
		#
		# construct the rest of the rows
		#
		
		for key in sorted(self.groups.keys(), reverse=True): # for each subset
			subset_list = []
			
			# define the locations that need to be printed for this subset
			if key in self.groups_loc:
				#locations = [l_indexes[l] for l in self.groups_loc[key][cy_i]] # TODO: do we need to consider the other years here?
				# TODO: kludge, adds unececssary locales, much extra processing. should changfe 'locations' for each year when doing multyear
				locations = []
				if remove_non_common_locations_in_current_year:
					locations = [l_indexes[l] for l in self.groups_loc[key][cy_i]]
				else:
					for y in self.year_indexes.values():
						locations.extend([l_indexes[l] for l in self.groups_loc[key][y]])
					locations = list(set(locations)) # remove duplicates
			else:
				locations = []
				if len(self.groups[key]) > 0:
					variety = self.groups[key][0]
					for l in l_indexes_values:
						if self.entries[variety][cy_i][l] is not None:
							locations.append(l)
			
			#
			# add the values for this subset
			#
			for v in sorted(self.groups[key], key=attrgetter('name')): # Sort each group alphabetically
				temp_row = [(v.name, v.id)+key] # tuple: (name, id, #curyear, #curyear-1, #curyear-2)
				append_me = True
				one_year_sums = []
				
				for l in l_indexes_values:
					if l not in locations: # ensure all subgroups only show data for common locations
						temp_row.append(None)
					else:
						value = self.entries[v][cy_i][l]
						
						if value is not None:
							value = round(value, 1) # TODO: is round necessary here?
							temp_row.append(value)
							one_year_sums.append(value) # will not contain None
						else:
							"""
							if l in locations: # this variety is from a higher-order set, but does not have data for one of our common locations
								append_me = False
								break
							"""
							temp_row.append(None)
							
				if append_me:
					avg_list = []
					if len(one_year_sums) > 1: # if we have two or more datapoints
						# prepend 1-yr avg, after the variety name
						avg_list.append(round(sum(one_year_sums)/len(one_year_sums), 1))
					else:
						avg_list.append(None)
						
					# append 2-yr, ... avgs
					for years_to_average in avg_years[1::]: # skip past 1-yr avg
						sum_list = []
						append_me = True
						for year in years_to_average:
							if append_me: # only continue while there are no errors
								if year != self.year: # we already retrieved the data for this year
									for l in l_indexes_values:
										
										value = self.entries[v][self.year_indexes[year]][l]
										if value is not None:
											sum_list.append(round(value, 1))
										"""
										else:
											append_me = False
											break
										"""
								else:
									sum_list.extend(one_year_sums)
						
						if append_me and len(sum_list) > 1:
							# prepend, after the 1-yr avg
							avg_list.append(round(sum(sum_list)/len(sum_list), 1))
						else:
							avg_list.append(None)
					subset_list.append(temp_row)
					
					for cell in avg_list[::-1]: # reverse-traverse the list
						temp_row.insert(1, cell)
					
			#	
			# prepare a list to compute lsd on, by removing all "None" from this subset
			#
			
			lsd_list = []
			for row in subset_list:
				not_none = []
				for cell in row[len(avg_years)+1::]: # skip past first column (the variety name), and do not include n-yr avgs
					if cell is not None:
						not_none.append(cell)
				if len(not_none) > 1:
					lsd_list.append(not_none)
			# append the calculated lsd row for this subset
			
			temp_row = ["LSD"]
			
			if len(lsd_list) > 0:
				# append 1-yr lsd
				#print "calculating lsd:"
				#print lsd_list
				try:
					value = round(self.LSD(response_to_treatments=lsd_list, probability=0.05), 1)
				except:
					value = None
				temp_row.append(value)
			else:
				temp_row.append(None)
			
			# append 2-yr, ... lsds
			append_me = True # reset error flag
			for years_to_average in avg_years[1::]: # skip past 1-yr avg
				multiple_year_lsd_list = []	
				for v in sorted(self.groups[key], key=attrgetter('name')): #TODO: we iterated through this already...
					variety_across_years = []
					for year in years_to_average:
						variety_for_year = []
						if append_me:
							for l in locations:
								value = self.entries[v][self.year_indexes[year]][l]
								if value is not None:
									variety_for_year.append(round(value,1))
								else:
									pass #print "multyear lsd error on: \t%s %s %s" % (v, year, l)
								"""
								else:
									append_me = False
									break
								"""
						variety_across_years.extend(variety_for_year)
					multiple_year_lsd_list.append(variety_across_years)
				
				# now go through and drop any larger than the minimum length
				
				if append_me:
					#print "calculating multyear lsd:"
					#print multiple_year_lsd_list
					try:
						value = round(self.LSD(response_to_treatments=multiple_year_lsd_list, probability=0.05), 1)
					except:
						#print "problem in multyear lsd"
						value = None
					temp_row.append(value)
				else:
					temp_row.append(None)
			
			if reduce_to_one_subset: # if we are the varieties view
				for l in sorted(self.groups_loc.values()[0][0], key=attrgetter('name')): ##TODO: Super-kludge	
					if self.location_indexes[l]  in locations:
						value = self.lsds[l][cy_i] #TODO: smarter logic needed
						if value is not None:
							temp_row.append(value)
						else:
							temp_row.append(None)
					else:
						temp_row.append(None)
					
			else:
				for l in self.location_indexes:
					if self.location_indexes[l] in locations:
						value = self.lsds[l][cy_i] #TODO: smarter logic needed
						if value is not None:
							temp_row.append(value)
						else:
							temp_row.append(None)
					else:
						temp_row.append(None)
					
			subset_list.append(temp_row)
			
			
			return_list.extend(subset_list) # append the lists inside subset_list to return_list
			return_list.append(next_header) # append another header row
		
		#print return_list[:len(return_list)-1:]
		
		return return_list[:len(return_list)-1:] # remove last row, a header row with nothing under it

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

	def __init__(self, entries, field, years, pref_year, varieties):
		"""
		Initializes internal data structures using the an input list of 
		entries, a field to filter on, and the years to include.
		"""
		self.varieties = [] # reset the variable, otherwise we see the last added to our new ones (TODO: might be a useful feature)
		for variety in varieties:
			self.varieties.append(variety.name)

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
		
		treatment_means = {}
		for i in range(n): # n == len(trt)
			total = 0.0
			for j in range(k):
				total += float(trt[i][j])
			treatment_means[i] = total/k
			
		block_means = {}
		for j in range(k):
			total = 0.0
			for i in range(n):
				total += float(trt[i][j])
			block_means[j] = total/n
		
		grand_mean = sum(treatment_means.values()) / float(n)
		
		# SSE is the Error Sum of Squares
		# TODO: what is the difference between type I and type III SS? (http://www.statmethods.net/stats/anova.html)
		SSE = 0.0
		for i in range(n): # n == len(trt)
			for j in range(k):
				SSE += (float(trt[i][j]) - treatment_means[i] - block_means[j] + grand_mean)**2.0
		
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
		self.entries = {}
		self.groups = {}
		self.lsds = {}
		
		# test if field is a Trial_Entry field
		if field in Trial_Entry._meta.fields:
			self.field = field
		
		# order years properly
		self.years = sorted(years, reverse=True)
		
		# test if year is in the list of years
		if self.year not in self.years:
			self.year = max(self.years)
		
		# grab data pertaining to our field
		fieldname = self.field.name
		for entry in entries:
			year = int(entry.harvest_date.date.year)
			if year in self.years:
				location = str(entry.location.name)
				self.locations.append(location)
				name = str(entry.variety.name)
							
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
		
	def fetch(self, reduce_to_one_subset=False):
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
		
		# remove empty groups
		groups_to_delete = []
		for key in self.groups:
			if len(self.groups[key]) == 0: # if the list is empty
				groups_to_delete.append(key)
		for key in groups_to_delete:
			del self.groups[key]
		
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
				
		if reduce_to_one_subset: # if we are the varieties view
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
			
			# for the groups that remain, delete the non-common locations until one subset remains
			locations_save = []
			
			for l in self.locations:
				add_location = True
				for key in self.groups.keys():
					for v in self.groups[key]:
						try:
							if self.entries[(l,v)][self.year] is None:
								add_location = False
								break # don't check anymore groups
						except KeyError:
							add_location = False
							break # don't check anymore groups
				if add_location:
					locations_save.append(l)
			#print locations_save
			if len(locations_save) > 0: # if any locations remain, replace
				self.locations = locations_save
				# put all into one group
				new_groups = {}
				new_groups[(1,0)] = list(self.varieties) # make a copy
				self.groups = new_groups

		else: # if we are the locations view
			# put all elements from higher-order groups into lower-order groups,
			# putting 'None' into non-common locations.
			for order in major_orders.keys(): # reverse-traverse
				for key in self.groups.keys():
					if key[0] < order: # if this group's order is smaller than another, add all from the higher order
						for larger_group_key in major_orders[order]:
							for v in self.groups[larger_group_key]:
								self.groups[key].append(v)
		
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
		
		#
		# construct rows from our data
		#
		
		# append header row
		head_row = [self.year] # first (row, column) value is the current year
		
		# constuct column headers for n-yr averaging
		for element in avg_years:
			n_yr = '%d-yr' % len(element)
			head_row.append((n_yr, -1)) # tuple: (name, id)
		for l in self.locations:
			location_id = -1
			try:
				location_id = models.Location.objects.get(name__iexact=l).id # TODO bad,bad,bad no-no-no we shouldn't need to hit the db like this
			except:
				pass
			head_row.append((l, location_id))
		return_list.append(head_row) # append first row
		
		# the header between each group
		next_header = [('Variety', -1)]
		next_header.extend(head_row[1::])
		
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
					variety_id = -1
					try:
						variety_id = models.Variety.objects.get(name__iexact=v).id # TODO bad,bad,bad no-no-no we shouldn't need to hit the db like this
					except:
						pass
					temp_row = [(v, variety_id)] # tuple: (name, id)
					append_me = True
					one_year_sums = []
					
					for l in self.locations:
						if l not in locations: # ensure all subgroups only show data for common locations
							temp_row.append(None)
						else:
							try:
								values = self.entries[(l,v)][self.year]
								value = round(sum(values)/len(values), 1) # TODO: is round necessary here?
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
							#temp_row.append(round(sum(one_year_sums)/len(one_year_sums), 1))
							# prepend 1-yr avg, after the variety name
							temp_row.insert(1, round(sum(one_year_sums)/len(one_year_sums), 1))
						else:
							append_me = False # cause the 2-yr,... to short-circuit
							#temp_row.append(None)
							temp_row.insert(1, None)
						# append 2-yr, ... avgs
						for years_to_average in avg_years[1::]: # skip past 1-yr avg
							sum_list = []
							append_me = True
							for year in years_to_average:
								if append_me: # only continue while there are no errors
									if year != self.year: # we already retrieved the data for this year
										for l in locations:
											try:
												values = self.entries[(l,v)][year]
												value = round(sum(values)/len(values), 1)
												sum_list.append(value)
											except KeyError:
												append_me = False
												break
									else:
										sum_list.extend(one_year_sums)
							
							if append_me and len(sum_list) > 1:
								# append
								#temp_row.append(round(sum(sum_list)/len(sum_list), 1))
								# prepend, after the 1-yr avg
								
								temp_row.insert(2, round(sum(sum_list)/len(sum_list), 1))
							else:
								#temp_row.append(None)
								temp_row.insert(2, None)
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
				
				if len(lsd_list) > 0:
					# append 1-yr lsd
					try:
						value = round(self.LSD(response_to_treatments=lsd_list, probability=0.05), 1)
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
							variety_for_year = []
							if append_me:
								for l in locations:
									try:
										values = self.entries[(l,v)][year]
										value = round(sum(values)/len(values), 1)
										variety_for_year.append(value)
									except KeyError:
										append_me = False
										break
							variety_across_years.extend(variety_for_year)
						multiple_year_lsd_list.append(variety_across_years)
					
					if append_me:
						try:
							value = round(self.LSD(response_to_treatments=multiple_year_lsd_list, probability=0.05), 1)
						except:
							value = None
						temp_row.append(value)
					else:
						temp_row.append(None)
						
				for l in self.locations:
					if l in locations:
						try:
							temp_row.append(max(self.lsds[(l, self.year)])) #TODO: smarter logic needed
						except KeyError:
							temp_row.append(None)
					else:
						temp_row.append(None)
						
				subset_list.append(temp_row)
					
				return_list.extend(subset_list) # append the lists inside subset_list to return_list
				return_list.append(next_header) # append another header row

		return return_list[:len(return_list)-1:] # remove last row, a header row with nothing under it

class Locations_from_Zipcode_x_Radius:
	"""
	Utility class to return a list of locations located a specified
	distance from a specified point.
	"""
	
	zipcode = ''
	radius = 0.0
	radius_sentinels = ['ALL', 'ND', 'MN']
	
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
		
		
		if radius in self.radius_sentinels: # if we are doing a specific search
			self.radius = radius
		else: # get the numeric value
			try:
				self.radius = float(radius)
			except ValueError:
				self.radius = 100.0
	
	def fetch(self):
		"""
		Returns a list of locations within the specified search area.
		raises a `models.Zipcode.DoesNotExist'
		"""
		locations = []
		skip_lookup = False
		
		if self.radius in self.radius_sentinels:
			skip_lookup = True
			if self.radius == 'ALL':
				locations = models.Location.objects.all()
			elif self.radius == 'ND':
				locations = models.Location.objects.select_related(
					depth=2).filter(zipcode__in=models.Zipcode.objects.filter(state__iexact="nd"))
			elif self.radius == 'MN':
				locations = models.Location.objects.select_related(
					depth=2).filter(zipcode__in=models.Zipcode.objects.filter(state__iexact="mn"))
			else:
				self.radius = 50.0
				skip_lookup = False
		
		if not skip_lookup:
			lat2_list = []
			lon2_list = []
			
			try:
				zipcode_query = models.Zipcode.objects.filter(zipcode=self.zipcode)
				zipcode_object = zipcode_query.get() # should only be one result
			except (ValueError, models.Zipcode.DoesNotExist) as instance:
				raise models.Zipcode.DoesNotExist(instance)

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