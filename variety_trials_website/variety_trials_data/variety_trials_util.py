from variety_trials_data.models import Trial_Entry #, Date
from variety_trials_data import models
from math import pi, sin, cos, asin, atan2, degrees, radians, sqrt, exp
from scipy.special import erfinv
import copy
from operator import add, attrgetter

class Location_Variety_Year_Field_Table():
	"""
	Utility functions on top of an array
	"""
	_data = []
	_location_indexes = {}
	_variety_indexes = {}
	_year_indexes = {}
	_field_indexes = {}
	_location_range = []
	_variety_range = []
	_year_range = []
	_locations_len = 0
	_varieties_len = 0
	_years_len = 0
	_fields_len = 0
		
	def __init__(self, entries, locations, varieties, years, fields):
		return self.populate(entries, locations, varieties, years, fields)
		
	def populate(self, entries, locations, varieties, years, fields):
		self._locations_len = len(locations)
		self._varieties_len = len(varieties)
		self._years_len = len(years)
		self._fields_len = len(fields)
		
		self._location_range = range(self._locations_len)
		self._variety_range = range(self._varieties_len)
		self._year_range = range(self._years_len)
		
		self._location_indexes = dict(zip(locations, self._location_range))
		self._variety_indexes = dict(zip(varieties, self._variety_range))
		self._year_indexes = dict(zip(years, self._year_range))
		self._field_indexes = dict(zip(fields, range(self._fields_len)))
		
		append = self._data.append # function pointer
		
		for l in locations:
			location_list = []
			lappend = location_list.append
			entries_by_location = [entry for entry in entries if entry.location.name == l.name]
			for v in varieties:
				variety_list = []
				vappend = variety_list.append
				entries_by_location_variety = [entry for entry in entries_by_location if entry.variety.name == v.name]
				for y in years:
					year_list = []
					yappend = year_list.append
					entries_by_location_variety_year = [entry for entry in entries_by_location_variety if int(entry.harvest_date.date.year) == y] # an empty list if no data
					for f in fields:
						field_avg = None
						len_lvy = len(entries_by_location_variety_year)
						if len_lvy > 0:
							try:
								field_avg = reduce(add, [float(getattr(entry, f.name)) for entry in entries_by_location_variety_year])
							except:
								field_avg = None
						if (field_avg > 0): # implied: and not None
							yappend(field_avg/len_lvy)
						else: # implied: if None: append(None)
							yappend(field_avg)
					vappend(year_list)
				lappend(variety_list)
			append(location_list)
					
	def fetch_for_location(self, location):
		return self._data[self._location_indexes[location]]
	
	def fetch_for_variety(self, variety):
		return [self._data[l][self._variety_indexes[variety]] for l in self._location_range]
			
	def fetch_for_year(self, year):
		#return [self._data[l][v][self._year_indexes[year]] for (l,v) in (self._location_range, self._variety_range)]
		return_list = []
		append = return_list.append
		y = self._year_indexes[year]
		for l in self._location_range:
			location_list = []
			lappend = location_list.append
			for v in self._variety_range:
				lappend(self._data[l][v][y])
			append(location_list)
		return return_list
		
	def fetch_for_field(self, field):
		#return [self._data[l][v][y][self._field_indexes[field]] for (l,v,y) in (self._location_range, self._variety_range, self._year_range)]
		return_list = []
		append = return_list.append
		f = self._field_indexes[field]
		for l in self._location_range:
			location_list = []
			lappend = location_list.append
			for v in self._variety_range:
				variety_list = []
				vappend = variety_list.append
				for y in self._year_range:
					vappend(self._data[l][v][y][f])
				lappend(variety_list)
			append(location_list)
		return return_list
		
	def fetch_for_location_variety(self, location, variety):
		return self.fetch_for_location(location)[self._variety_indexes[variety]]
		
	def fetch_for_location_year(self, location, year):
		return [self.fetch_for_location(location)[v][self._year_indexes[year]] for v in self._variety_range]
		
	def fetch_for_location_field(self, location, field):
		#return [self.fetch_for_location(location)[v][y][self._field_indexes[field]] for (v,y) in (self._variety_range, self._year_range)]
		return_list = []
		append = return_list.append
		l = self.fetch_for_location(location)
		f = self._field_indexes[field]
		for v in self._variety_range:
			variety_list = []
			vappend = variety_list.append
			for y in self._year_range:
				vappend(l[v][y][f])
			append(variety_list)
		return return_list
		
	def fetch_for_variety_year(self, variety, year):
		return [variety_list[self._year_indexes[year]] for variety_list in self.fetch_for_variety(variety)]
		
	def fetch_for_variety_field(self, variety, field):
		#return [variety_list[y][self._field_indexes[field]] for (variety_list, y) in (self.fetch_for_variety(variety), self._year_range)]
		return_list = []
		append = return_list.append
		variety_list = self.fetch_for_variety(variety)
		f = self._field_indexes[field]
		for v in variety_list:
			variety_list = []
			vappend = variety_list.append
			for y in self._year_range:
				vappend(v[y][f])
			append(variety_list)
		return return_list
		
	def fetch_for_year_field(self, year, field):
		return_list = []
		append = return_list.append
		for y in self.fetch_for_year(year):
			year_list = []
			yappend = year_list.append
			for l in y:
				yappend(l[self._field_indexes[field]])
			append(year_list)
		return return_list
		
	def fetch_for_location_variety_year(self, location, variety, year):
		return self.fetch_for_location_variety(location, variety)[self._year_indexes[year]]
		
	def fetch_for_location_variety_field(self, location, variety, field):
		return [self.fetch_for_location_variety(location, variety)[y][self._field_indexes[field]] for y in self._year_range]
		
	def fetch_for_location_year_field(self, location, year, field):
		return [self.fetch_for_location(location)[v][self._year_indexes[year]][self._field_indexes[field]] for v in self._variety_range]
		
	def fetch_for_variety_year_field(self, variety, year, field):
		return [variety_year_list[self._field_indexes[field]] for variety_year_list in self.fetch_for_variety_year(variety, year)]
	
	def fetch_for_location_variety_year_field(self, location, variety, year, field):
		return self.fetch_for_location_variety_year(location, variety, year)[self._field_indexes[field]]

class LSD_Calculator:
	"""
	Utility class to return a formatted dictionary of all given entries,
	sorted by location name and year, filtered by one field and averaged
	across.
	"""
	
	
	
	
	locations = [] # location "l"
	varieties = [] # variety "v"
	years = [] #year "y"
	year = 0 # current year we are viewing
	field = None
	
	# all data
	entries = None # a Location_Variety_Year_Field_Table object
	
	# data (with duplicates) separated into balanced subsets
	groups = {} # {(major,minor): [v, ...], ...}
	# lsds of the data
	lsds = {} # {(l,y): [12.2, ...], ...}
	
	def __init__(self, entries_table, locations, varieties, years, pref_year, field):
		"""
		Initializes internal data structures using the an input list of 
		entries, a field to filter on, and the years to include.
		"""
		
		return self.populate(self, entries_table, locations, varieties, years, pref_year, field)

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
		
	def populate(self, entries_table, locations, varieties, years, pref_year):
		"""
		"""
		
		self.years = years
		self.locations = locations
		self.varieties = varieties
		self.year = pref_year
		self.entries = entries_table
		
		# re-init to empty (persistent between each user's session)
		# TODO: consider not recalculating absolutely everything?
		self.groups = {} 
		self.lsds = {}
		
		# test if year is in the list of years
		if self.year not in self.years:
			self.year = max(self.years)
		
		"""
		self.raw_varieties = varieties
		self.raw_locations = locations
		
		self.varieties = [variety.name for variety in varieties]
		self.locations = [location.name for location in locations]
		
		# remove duplicates
		self.locations = sorted(list(set(self.locations)))
		self.varieties = sorted(list(set(self.varieties)))
		"""
		
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
		
		# make a list of years to average over
		avg_years = []
		
		# find all years before the current year, inclusive
		def f(x): return (x <= self.year)
		
		append = avg_years.append
		# construct a list for n-yr averaging e.g. [[2010], [2010, 2009], [2010, 2009, 2008]]
		for year in sorted(filter(f, self.years)):
			for element in avg_years:
				element.append(year)
			append([year])
			
		avg_years = sorted(avg_years, reverse=True) # order them 1-yr, 2-yr, ...
		
		#
		# construct rows from our data
		#
		
		# append header row
		head_row = [self.year] # first (row, column) value is the current year
		
		append = head_row.append
		
		# constuct column headers for n-yr averaging
		append([ (n_yr = '%d-yr' % len(element), -1) for element in avg_years])
		
		# censure empty locations before we append them to the header
		"""
		# make sum tables while going through all of it
		
		for l in self.locations:
			for y in self.years:
				location_year_entries = reduce(add, [location_entry[y] for location_entry in self.entries.fetch_for_location(l.name)]) # list addition
				
				if (len(location_year_entries) == 0):
					sum_location_year[(l, y)] = None
				else:
					sum_location_year[(l, y)] = reduce(add, [float(getattr(entry, self.field.name)) for entry in location_year_entries]) # float addition
					
			if (sum_location_year[(l, self.year)] is None):
				empty_locations.append(l)
		"""
		"""
		sums_location_year = {}
		empty_locations = []
		# Discard a column (location) that is empty
		for l in self.locations:
			empty = True
			for v in self.varieties:
				for y in self.years:
					location_variety_year_entries = reduce(add, self.entries.fetch_for_location_variety(l, v, y)) # list addition
					if y is self.year:
						empty = empty or (len(location_year_entries) == 0)
						sum_location_year[(l, v, y)] = None
					else
					if (len(location_year_entries) == 0):
						sum_location_year[(l, y)] = None
					else:
						sum_location_year[(l, y)] = reduce(add, [float(getattr(entry, self.field.name)) 
				if not empty:
					break
			if empty:
				empty_locations.append(l)
				
		# remove empty locations
		self.locations = sorted(list(
					set(self.locations).difference(
					set(empty_locations))
			), key=attrgetter('name')) #TODO: distance sort instead of alphabetical by name
		"""
		# construct column headers for locations
		append([ (l.name, l.id) for l in self.locations])
			
		return_list.append(head_row) # append first row
		
		# the header between each group
		next_header = [('Variety', -1)]
		next_header.extend(head_row[1::])
		
		
		
		
			
		"""
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
		"""
		
		
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
