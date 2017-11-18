#$ python manage.py shell
from variety_trials_data import models

## source "" sent 

locations = [
		#("Crookston", "Conventional"),
		#("Crookston", "Intensive"),
	]

rename_locations = {
		#"LeCenter": ("Le Center", "Conventional"),
	}

fail = False
for lname, tags in locations:
	try:
		if lname in rename_locations:
			lname, tags = rename_locations[lname]
		location = models.Location.objects.filter(name=lname)[0]
	except:
		fail = True
		print 'Missing Location record: ', lname

varieties = [
#		"Bolles",
	]

rename_varieties = {}
#rename_varieties["Elgin-ND"] = "Elgin"


for vname in varieties:
	try:
		if vname in rename_varieties:
			vname = rename_varieties[vname]
		variety = models.Variety.objects.filter(name=vname)[0]
	except:
		fail = True
		print 'Missing Variety record: ', vname
		models.Variety.objects.filter(name__contains=vname)

if fail:
	print ("ERROR: Missing records. See preceding output. Exiting...")
	import sys
	sys.exit(1)

# location name, planting tags, yield lsd5, yield lsd10
yield_lsds = [
		#("Crookston", "Conventional", "4.5903503484", "3.4775381427"),
		#("Crookston", "Intensive", "4.6464563911", "3.5200427205"),
	]

# regexps to help transform tab-delimited copy+paste from source workbook
# s/\t/, /
# s/$/]/
# s/^/yields["/
# s/^([^,]+), /\1"]=[/
yields = {}
#yields["Bolles"] = [ 103.5, 96.6, 101.3, 85.4, 70.7, 63.7, 73.0, 82.0, 81.8, 75.9, 82.9, 96.0, 62.6, 71.5, 67.2, 73.6]

proteins = {}
#proteins["Bolles"] = [ 14.8, 14.0, 15.4, 17.1, 16.7, 17.5, 16.9, 16.2, 17.2, 16.2, 16.0, 15.1, 17.0, 15.9, 14.2, 15.2]

weights = {}
#weights["Bolles"] = [ 56.2, 61.3, 60.4, 56.8, 58.1, 56.0, 59.0, 59.2, 58.0, 60.0, 60.6, 58.5, 56.3, 58.6, 57.7, 59.5]

planted = models.Date.objects.filter(date__year=2017, date__month=5)[0]
harvested = models.Date.objects.filter(date__year=2017, date__month=8)[0]

for vname in yields:
	for i in range(len(yield_lsds)):
		tags = None
		hidden = False
		bushels = yields[vname][i]
		if bushels is None:
			continue
		lname, tags, lsd5, lsd10 = yield_lsds[i]
		if lname in rename_locations:
			lname, tags = rename_locations[lname]
		if tags is not None and tags is not "Conventional":
			hidden = True
		weight = weights[vname][i]
		protein = proteins[vname][i]
		if vname in rename_varieties:
			dbvname = rename_varieties[vname]
		else:
			dbvname = vname
		new_trial = models.Trial_Entry(
				bushels_acre=bushels, 
				plant_date=planted, 
				harvest_date=harvested, 
				location=models.Location.objects.filter(name=lname)[0], 
				variety=models.Variety.objects.filter(name=dbvname)[0], 
				hidden=hidden
			)
		if weight is not None:
			new_trial.test_weight = weight
		if protein is not None:
			new_trial.protein_percent = protein
		if tags is not None:
			new_trial.planting_method_tags = tags
		if lsd10 is not None:
			new_trial.lsd_10 = lsd10
		if lsd5 is not None: 
			new_trial.lsd_05 = lsd5
		new_trial.save()
		#if not dbvname or not planted or not harvested or not lname: print(new_trial)
