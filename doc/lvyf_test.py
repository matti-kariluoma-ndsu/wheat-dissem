import datetime
from operator import add

class Location():
	name = ""
	def __init__(self, lname):
		self.name = lname
class Variety():
	name = ""
	def __init__(self, vname):
		self.name = vname
class Year():
	date = None
	def __init__(self, yval):
		self.date = datetime.date(yval,1,1)
class Field():
	name = ""
	def __init__(self, fname):
		self.name = fname
class Entry():
	location = None
	variety = None
	harvest_date = None
	bushels_acre = None

	def __init__(self, lname, vname, yval, buac_value):
		self.location = Location(lname)
		self.variety = Variety(vname)
		self.harvest_date = Year(yval)
		self.bushels_acre = buac_value

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
		self._varieties_range = range(self._varieties_len)
		self._years_range = range(self._years_len)
		
		self._location_indexes = dict(zip(locations, self._location_range))
		self._variety_indexes = dict(zip(varieties, self._varieties_range))
		self._year_indexes = dict(zip(years, self._years_range))
		self._field_indexes = dict(zip(fields, range(self._fields_len)))
		
		append = self._data.append # function pointer
		
		for l in locations:
			location_list = []
			entries_by_location = [entry for entry in entries if entry.location.name == l.name]
			#print entries_by_location
			for v in varieties:
				variety_list = []
				entries_by_location_variety = [entry for entry in entries_by_location if entry.variety.name == v.name]
				#print entries_by_location_variety
				for y in years:
					year_list = []
					entries_by_location_variety_year = [entry for entry in entries_by_location_variety if int(entry.harvest_date.date.year) == y] # an empty list if no data
					#print entries_by_location_variety_year
					for f in fields:
						field_avg = None
						len_lvy = len(entries_by_location_variety_year)
						if len_lvy > 0:
							#print [float(getattr(entry, f.name)) for entry in entries_by_location_variety_year]
							try:
								field_avg = reduce(add, [float(getattr(entry, f.name)) for entry in entries_by_location_variety_year])
							except:
								field_avg = None
						#print field_avg
						if (field_avg > 0): # implied: and not None
							year_list.append(field_avg/len_lvy)
						else: # implied: if None: append(None)
							year_list.append(field_avg)
					variety_list.append(year_list)
				location_list.append(variety_list)
			append(location_list)
		
		#print self._data
		
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
			for v in self._variety_range:
				append(self._data[l][v][y])
		return return_list
		
	def fetch_for_field(self, field):
		#return [self._data[l][v][y][self._field_indexes[field]] for (l,v,y) in (self._location_range, self._variety_range, self._year_range)]
		return_list = []
		append = return_list.append
		f = self._field_indexes[field]
		for l in self._location_range:
			for v in self._variety_range:
				for y in self._year_range:
					append(self._data[l][v][y][f])
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
			for y in self._year_range:
				append(l[v][y][f])
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
			for y in self._year_range:
				append(v[y][f])
		return return_list
		
	def fetch_for_year_field(self, year, field):
		return [year_list[self._field_indexes[field]] for year_list in self.fetch_for_year(year)]
		
	def fetch_for_location_variety_year(self, location, variety, year):
		return self.fetch_for_location_variety(location, variety)[self._year_indexes[year]]
		
	def fetch_for_location_variety_field(self, location, variety, field):
		return [self.fetch_for_location_variety(location, variety)[y][self._field_indexes[field]] for y in self._year_range]
		
	def fetch_for_variety_year_field(self, variety, year, field):
		return [variety_year_list[self._field_indexes[field]] for variety_year_list in self.fetch_for_variety_year(variety, year)]
	
	def fetch_for_location_variety_year_field(self, location, variety, year, field):
		return self.fetch_for_location_variety_year(location, variety, year)[self._field_indexes[field]]


def main():
	
	locations = [Location("Bismarck"), Location("Fargo"), Location("Grand Forks"), Location("Williston")]
	varieties = [Variety("Jenna"), Variety("Reeder"), Variety("RB")]
	years = [2009, 2010, 2011]
	fields = [Field("bushels_acre")]
	entries = [Entry("Fargo", "Jenna", 2009, 4.0), Entry("Fargo", "Jenna", 2010, 3.2), 
		Entry("Fargo", "Jenna", 2011, 5.1), Entry("Grand Forks", "Jenna", 2009, 5.0),
		Entry("Bismarck", "RB", 2011, 5.2), Entry("Bismarck", "Reeder", 2011, 11.0),
		Entry("Bismarck", "Jenna", 2011, 3.8)
	]
	
	table = Location_Variety_Year_Field_Table( entries, locations, varieties, years, fields)
	
	for l in locations:
		print l.name
		print table.fetch_for_location(l)
	for v in varieties:
		print v.name
		print table.fetch_for_variety(v)
	for y in years:
		print y
		print table.fetch_for_year(y)
	for f in fields:
		print f.name
		print table.fetch_for_field(f)
	
	l = locations[0]
	v = varieties[0]
	y = years[2]
	f = fields[0]
	print "%s %s %d %s" % (l.name, v.name, y, f.name)
	
	print "%s %s" % (l.name, v.name)
	print table.fetch_for_location_variety(l, v)
	
	print "%s %d" % (l.name, y)
	print table.fetch_for_location_year(l, y)
	
	print "%s %s" % (v.name, f.name)
	print table.fetch_for_variety_field(v, f)
	
	print "%s %d" % (v.name, y)
	print table.fetch_for_variety_year(v,y)
	
	print "%d %s" % (y, f.name)
	print table.fetch_for_year_field(y, f)
		
if __name__ == '__main__':
	main()
