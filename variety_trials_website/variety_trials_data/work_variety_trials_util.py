from variety_trials_data.variety_trials_util import LSD_Calculator

def perform(prefix="58102_100_"):
	# deserialize our inputs
	from django.core import serializers
	entries = []
	locations = []
	varieties = []
	with open(prefix+"entries.json", "r") as infile:
		for entry in serializers.deserialize("json", infile):
			entries.append(entry.object)
	with open(prefix+"locations.json", "r") as infile:
		for l in serializers.deserialize("json", infile):
			locations.append(l.object)
	with open(prefix+"varieties.json", "r") as infile:
		for v in serializers.deserialize("json", infile):
			varieties.append(v.object)
	
	import json
	with open(prefix+"years.json", "r") as infile:
		years = json.load(infile)
	with open(prefix+"pref_year.json", "r") as infile:
		pref_year = json.load(infile)
	
	class fakeFieldClass:
		name = ""
		def __init__(self, name):
			self.name = name
	
	with open(prefix+"field.json", "r") as infile:
		data = json.load(infile)
		field = fakeFieldClass(data["name"])
		
	sorted_list = LSD_Calculator(entries, locations, varieties, years, pref_year, field).fetch()
	
	print sorted_list

"""
def __test__():
	import sys
	if len(sys.argv) > 0:
		perform(prefix=str(sys.argv[1]))
	else:
		perform()
		
if __name__ == "__main__":
	__test__()
"""
