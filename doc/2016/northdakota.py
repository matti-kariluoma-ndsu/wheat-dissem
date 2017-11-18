#$ python manage.py shell
from variety_trials_data import models

## source "Selection tool data 2016.xlsx" sent Dec/10/2016, 12:30 CST

locations = [
		"Carr-Dry",
		"Carr-Irr",
		"Carr-Elite",
		"CREC-Dazey",
		"CREC-Wishek",
		"Casselton",
		"Prosper",
		"Langdon",
		"LREC-Cando",
		"LREC-Cavalier",
		"LREC-Park River",
		"LREC-Pekin",
		"Dickinson",
		"Hettinger",
		"Minot",
		"Garrison",
		"Mohall",
		"Williston",
		"Williston-Irr.",
	]

rename_locations = {}
# (name, planting_method_tags)
rename_locations["Carr-Dry"] = ("Carrington", "dryland")
rename_locations["Carr-Irr"] = ("Carrington", "irrigated")
rename_locations["Carr-Elite"] = ("Carrington", "elite")
rename_locations["CREC-Dazey"] = ("Dazey", None)
rename_locations["CREC-Wishek"] = ("Wishek", None)
rename_locations["LREC-Cando"] = ("Cando", None)
rename_locations["LREC-Cavalier"] = ("Cavalier", None)
rename_locations["LREC-Park River"] = ("Park River", None)
rename_locations["LREC-Pekin"] = ("Pekin", None)
rename_locations["Garrison"] = ("McLean County", None)
rename_locations["Williston"] = ("Williston", "dryland")
rename_locations["Williston-Irr."] = ("Williston", "irrigated")

fail = False
for lname in locations:
	try:
		if lname in rename_locations:
			lname, tags = rename_locations[lname]
		location = models.Location.objects.filter(name=lname)[0]
	except:
		fail = True
		print 'Missing Location record: ', lname

varieties = [
		"07S0027-3 (SY Rockford)",
		"Advance",
		"Barlow",
		"Bolles",
		"Boost",
		"Brennan",
		"Briggs",
		"Duclair",
		"Egan",
		"Elgin-ND",
		"Faller",
		"Faller (1.8M PLS)",
		"Filler (Glenn)",
		"Focus",
		"Forefront",
		"Freyr",
		"Glenn",
		"HRS 3100",
		"HRS 3361",
		"HRS 3419",
		"HRS 3504",
		"HRS 3530",
		"HRS 3616",
		"Jenna",
		"Kelby",
		"LCS Anchor",
		"LCS Breakaway",
		"LCS Iguacu",
		"LCS Nitro",
		"LCS Powerplay",
		"LCS Prime",
		"LCS Pro",
		"Linkert",
		"MN10261-1",
		"Mott",
		"MS Chevelle",
		"MS Stingray",
		"ND901CL Plus",
		"Prestige",
		"Prevail",
		"Prosper",
		"RB07",
		"Redstone",
		"Reeder",
		"Rollag",
		"Shelly",
		"Steele-ND",
		"Surpass",
		"SY Ingmar",
		"SY-Rowyn",
		"SY-Soren",
		"SY-Tyra",
		"SY-Valda",
		"SY605CL",
		"TCG-Cornerstone",
		"TCG-Spitfire",
		"TCG-Wildfire",
		"Vantage",
		"Velva",
		"Vida",
		"WB-Digger",
		"WB-Mayville",
		"WB-Mayville (1.8 M PLS)",
		"WB9312",
		"WB9507",
		"WB9653",
	]

rename_varieties = {}
rename_varieties["Elgin-ND"] = "Elgin"
rename_varieties["SY-Rowyn"] = "SY Rowyn"
rename_varieties["SY-Soren"] = "SY Soren"
rename_varieties["SY-Tyra"] = "SY Tyra"
rename_varieties["SY-Valda"] = "SY Valda"
rename_varieties["ND901CL Plus"] = "ND 901CL Plus"
rename_varieties["SY605CL"] = "SY605 CL"
rename_varieties["WB9879CLP+"] = "WB9879CLP Plus"
rename_varieties["07S0027-3 (SY Rockford)"] = "SY Rockford 07S0027-3"
rename_varieties["TCG-Cornerstone"] = "TCG Cornerstone"
rename_varieties["TCG-Spitfire"] = "TCG Spitfire"
rename_varieties["TCG-Wildfire"] = "TCG Wildfire"
rename_varieties["WB-Mayville (1.8 M PLS)"] = "WB-Mayville (1.8M PLS)"
rename_varieties["Vantage"] = "WB-Vantage"

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
	print "ERROR: Missing records. See preceding output. Exiting..."
	import sys
	sys.exit(1)

# location name, yield lsd10, yield lsd5
yield_lsds = [
		("Carr-Dry", "4.6", "5.5"),
		("Carr-Irr", None, None),
		("Carr-Elite", "5.4", "6.5"),
		("CREC-Dazey", "7.1", "8.4"),
		("CREC-Wishek", "9.1", "10.9"),
		("Casselton", "6.1", "7.3"),
		("Prosper", "6.3", "7.5"),
		("Langdon", "6.8", "8.1"),
		("LREC-Cando", "5.7", "6.9"),
		("LREC-Cavalier", "4.9", "5.9"),
		("LREC-Park River", "4.3", "5.1"),
		("LREC-Pekin", "4.8", "5.7"),
		("Dickinson", "6.4", "7.6"),
		("Hettinger", "4", "4.7"),
		("Minot", "11", "13.1"),
		("Garrison", "6.5", "7.7"),
		("Mohall", "7", "8.4"),
		("Williston", "4.4", "5.3"),
		("Williston-Irr.", "9", "10.7"),
	]

# regexps to help transform tab-delimited copy+paste from source workbook
# s/\t/, /
# s/$/]/
# s/^/yields["/
# s/^([^,]+), /\1"]=[/
yields = {}
yields["07S0027-3 (SY Rockford)"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, 48.7, None, None, None, 57.5, None]
yields["Advance"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 87.6]
yields["Barlow"] = [ 34.8, None, 38.9, 79.6, 74.4, 80.0, 73.3, 59.6, None, None, None, None, 48.5, 48.4, 63.6, 56.7, 79.1, 52.8, 76.6]
yields["Bolles"] = [ 28.5, None, 32.3, 64.4, 54.5, 69.9, 65.8, 62.6, 77.2, 48.1, 69.0, 64.1, 47.5, 44.0, 70.2, 61.1, 74.2, 45.6, 79.4]
yields["Boost"] = [ 39.3, None, 41.0, 74.2, 70.5, 79.0, 67.3, 60.5, 68.0, 44.4, 68.9, 72.2, 52.3, 50.6, 66.0, 59.4, 76.5, 48.5, None]
yields["Brennan"] = [ 33.7, None, None, 64.2, 65.4, None, None, None, None, None, None, None, None, None, None, None, None, None, 73.0]
yields["Briggs"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 73.1]
yields["Duclair"] = [ None, None, None, None, None, None, None, None, None, None, None, None, 49.8, 48.5, 84.4, None, None, 53.0, None]
yields["Egan"] = [ None, None, None, None, None, None, None, None, None, None, None, None, 45.4, 51.6, 71.0, None, None, 48.4, 80.7]
yields["Elgin-ND"] = [ 36.0, None, 42.0, 73.7, 76.8, 78.0, 74.1, 64.7, 76.0, 52.9, 77.3, 63.6, 48.5, 48.5, 80.0, 60.6, 82.3, 57.2, 89.9]
yields["Faller"] = [ 30.1, None, 45.0, 85.2, 88.4, 72.0, 80.8, 79.0, 87.9, 60.5, 81.2, 71.1, 47.1, 43.4, 84.2, 65.1, 87.5, 53.5, 79.0]
yields["Faller (1.8M PLS)"] = [ None, None, None, 84.7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
yields["Filler (Glenn)"] = [ None, None, 30.2, 69.9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
yields["Focus"] = [ 32.2, None, 35.4, 78.5, 71.9, 85.0, 70.8, 53.1, 85.6, 43.8, 69.0, 62.6, 49.6, 48.2, 65.3, None, None, 54.7, 66.8]
yields["Forefront"] = [ 36.1, None, None, 77.5, 69.0, None, None, None, None, None, None, None, None, None, None, None, None, None, 78.8]
yields["Freyr"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 75.9]
yields["Glenn"] = [ 31.4, None, 30.8, 69.1, 65.2, 67.1, 66.9, 64.3, None, None, None, None, 51.2, 49.1, 76.4, 56.1, 79.2, 52.7, 69.7]
yields["HRS 3100"] = [ None, None, None, None, None, None, None, 69.5, 79.2, 61.3, 70.8, 72.9, None, None, None, None, None, 57.0, None]
yields["HRS 3361"] = [ 32.6, None, 46.1, 82.1, 77.1, 78.3, 81.7, 70.5, 80.0, 63.5, 72.2, 72.3, 55.3, 44.6, 90.2, None, None, None, None]
yields["HRS 3419"] = [ 35.2, None, 46.2, 86.8, 63.3, 82.7, 86.4, 78.9, 93.0, 68.4, 82.7, 70.6, 60.5, 54.7, 83.8, 63.2, 80.0, None, 102.1]
yields["HRS 3504"] = [ 38.5, None, 56.4, 79.1, 75.8, 82.3, 85.3, 73.2, 75.3, 57.1, 68.6, 71.5, 65.0, 48.3, 83.6, None, None, 59.8, None]
yields["HRS 3530"] = [ 23.7, None, 45.0, 89.1, 77.5, 87.8, 93.6, 78.1, 91.7, 56.9, 79.9, 79.8, 59.1, 43.7, 73.5, 66.0, 84.7, None, 89.5]
yields["HRS 3616"] = [ 37.4, None, None, 61.5, 67.8, 76.7, 75.4, 65.9, 77.3, 50.0, 73.3, 68.5, 48.9, 48.6, 75.6, None, None, 52.2, 77.0]
yields["Jenna"] = [ 34.1, None, None, 74.0, 77.3, None, None, None, None, None, None, None, None, None, None, None, None, None, 84.0]
yields["Kelby"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 62.2]
yields["LCS Anchor"] = [ 38.0, None, None, 67.2, 66.2, None, None, 59.5, 78.0, 44.9, 61.3, 67.3, 51.7, 52.6, 72.5, None, None, 55.2, 64.8]
yields["LCS Breakaway"] = [ 35.8, None, 43.0, 79.4, 67.8, 79.0, 79.1, 70.9, 77.8, 45.7, 75.1, 72.7, 51.2, 48.4, 86.9, None, None, 49.8, None]
yields["LCS Iguacu"] = [ 31.9, None, None, None, None, 76.6, 85.3, 75.7, None, None, None, None, 54.0, 47.5, 75.4, None, None, 50.7, 81.7]
yields["LCS Nitro"] = [ 33.8, None, 37.2, 80.0, 69.6, 82.2, 82.4, 77.8, None, None, None, None, 57.0, 44.9, 109.1, 59.2, 85.8, 52.5, 87.4]
yields["LCS Powerplay"] = [ 33.3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
yields["LCS Prime"] = [ 31.4, None, 45.1, 77.8, 66.7, 73.3, 75.2, 68.7, 80.0, 45.7, 75.6, 75.4, 60.5, 49.1, 77.7, 68.4, 82.9, 55.9, 77.6]
yields["LCS Pro"] = [ 38.3, None, None, None, None, 79.3, 74.8, 67.8, None, None, None, None, 60.7, 49.7, 81.2, 64.2, 75.3, 57.1, None]
yields["Linkert"] = [ 32.9, None, 42.2, 77.4, 82.8, 72.0, 75.5, 62.8, 74.7, 56.1, 71.1, 66.2, 52.9, 43.6, None, 57.8, 69.1, 51.3, 71.8]
yields["MN10261-1"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, 49.9, 77.5, None, None, 55.2, None]
yields["Mott"] = [ 33.6, None, None, None, 77.4, None, None, None, None, None, None, None, 45.1, 46.4, 66.9, None, None, 53.3, 79.7]
yields["MS Chevelle"] = [ 38.2, None, 45.8, 67.7, 72.8, 76.0, 78.5, 67.7, None, None, None, None, 57.7, 47.8, 86.7, None, None, 57.8, 86.5]
yields["MS Stingray"] = [ 32.8, None, None, None, None, 87.1, 87.8, 75.6, None, None, None, None, 52.1, 43.2, 99.1, None, None, 55.4, None]
yields["ND901CL Plus"] = [ None, None, None, None, None, None, None, None, None, None, None, None, 49.5, 41.5, 69.9, None, None, 53.0, None]
yields["Prestige"] = [ 37.0, None, None, None, None, 79.1, 73.1, 67.8, None, None, None, None, 54.1, 45.8, 74.2, 66.2, 85.2, 51.4, 104.3]
yields["Prevail"] = [ 32.2, None, 40.9, 78.1, 64.1, 82.4, 88.4, 65.9, 83.4, 54.6, 78.7, 69.7, 57.5, 49.3, 64.2, 60.6, 75.6, 57.9, 74.1]
yields["Prosper"] = [ 28.9, None, 43.9, 82.1, 85.4, 75.4, 75.5, 77.8, 82.5, 56.8, 78.6, 75.3, 55.0, 36.0, 93.8, 62.8, 87.7, 51.2, 83.4]
yields["RB07"] = [ 32.9, None, None, None, None, None, None, None, None, None, None, None, 47.6, None, 85.4, None, None, None, 78.4]
yields["Redstone"] = [ 34.1, None, None, None, None, 80.1, 75.2, 75.9, None, None, None, None, 56.6, 47.0, 86.2, 63.9, 96.9, 56.9, 69.5]
yields["Reeder"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 80.6]
yields["Rollag"] = [ 36.4, None, 38.9, 77.2, 75.9, 75.5, 74.1, 71.2, 72.8, 58.0, 74.2, 63.1, 52.6, 47.3, 74.6, None, None, 53.7, 74.3]
yields["Shelly"] = [ 30.3, None, 39.4, 84.2, 72.2, 82.7, 81.6, 71.1, 87.0, 50.9, 82.3, 71.5, None, 50.9, 71.2, 62.2, 84.2, 51.6, None]
yields["Steele-ND"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 75.9]
yields["Surpass"] = [ 35.6, None, 41.4, 82.3, 63.8, 89.3, 82.2, 58.5, 81.5, 46.0, 72.9, 75.2, None, 49.7, 68.6, None, None, 54.8, None]
yields["SY Ingmar"] = [ 38.0, None, None, None, 77.8, 83.1, 76.6, 70.0, 76.2, 55.4, 74.2, 73.6, 56.7, 48.1, 84.6, 62.6, 82.2, 51.9, 84.7]
yields["SY-Rowyn"] = [ 30.1, None, None, 77.2, None, 81.0, 88.5, 67.2, 81.2, 55.7, 75.9, 77.6, 58.6, 48.8, 70.5, None, None, 50.8, None]
yields["SY-Soren"] = [ 35.3, None, 44.8, 66.7, 74.6, 72.5, 70.8, 68.9, 82.0, 54.0, 76.0, 72.3, 50.1, 50.1, 68.6, 60.4, 80.0, 54.4, 77.4]
yields["SY-Tyra"] = [ None, None, None, None, None, None, None, None, None, None, None, None, 51.9, 46.6, 74.2, None, None, 53.8, None]
yields["SY-Valda"] = [ 33.8, None, 47.7, 83.0, 80.6, 87.8, 91.1, 78.4, 83.3, 59.3, 77.7, 79.4, 63.5, 49.6, 77.1, 69.4, 84.2, 55.4, 70.2]
yields["SY605CL"] = [ None, None, None, None, None, None, None, None, None, None, None, None, 45.9, 49.0, 73.3, None, None, 55.2, None]
yields["TCG-Cornerstone"] = [ 32.2, None, None, None, None, 70.9, 75.9, 58.3, 61.6, 43.6, 60.0, 58.9, 52.0, 43.2, 60.7, None, None, 47.5, None]
yields["TCG-Spitfire"] = [ 37.4, None, None, None, None, 75.5, 80.2, 58.2, None, None, None, None, 59.7, 52.0, 87.7, None, None, 55.0, None]
yields["TCG-Wildfire"] = [ 33.5, None, None, None, None, 84.3, 79.2, 64.2, None, None, None, None, 52.0, 45.3, 71.5, None, None, 53.4, None]
yields["Vantage"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 82.8]
yields["Velva"] = [ 38.0, None, None, None, None, 71.4, 64.5, 52.6, None, None, None, None, 55.3, 43.0, 80.0, None, None, 58.9, 82.1]
yields["Vida"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 82.9]
yields["WB-Digger"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 77.8]
yields["WB-Mayville"] = [ 34.6, None, 42.4, 79.5, 70.8, 78.8, 79.3, 56.9, 69.3, 43.1, 65.4, 66.0, 53.7, 45.9, 69.7, None, None, 52.6, 68.4]
yields["WB-Mayville (1.8 M PLS)"] = [ 32.2, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
yields["WB9312"] = [ None, None, None, None, None, 83.0, 87.6, None, None, None, None, None, 56.1, 39.1, 77.3, None, None, 48.9, None]
yields["WB9507"] = [ 34.1, None, 45.6, 83.7, 79.9, 83.6, 81.9, 76.6, 84.4, 57.4, 80.2, 81.0, 52.8, 36.2, 73.3, 58.0, 81.8, 52.8, 69.5]
yields["WB9653"] = [ 36.7, None, 48.5, 80.5, 78.7, 86.7, 90.4, 76.1, 73.5, 62.0, 69.7, 72.6, 61.8, 45.8, 87.5, None, None, 56.3, 76.2]

weights = {}
weights["07S0027-3 (SY Rockford)"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, 55.0, None, None, None, 56.9, None]
weights["Advance"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 62.9]
weights["Barlow"] = [ 57.1, None, 57.9, 58.0, 58.8, 62.4, 61.8, 60.0, None, None, None, None, 60.3, 59.0, 61.9, 64.2, 63.4, 59.3, 62.8]
weights["Bolles"] = [ 54.3, None, 55.9, 53.9, 57.4, 60.6, 59.3, 60.2, 59.9, 57.9, 58.3, 56.2, 58.2, 58.8, 60.9, 61.8, 61.2, 56.5, 61.2]
weights["Boost"] = [ 53.4, None, 57.6, 56.8, 58.1, 61.4, 61.0, 58.5, 59.1, 58.2, 58.2, 58.8, 61.1, 57.6, 59.6, 62.2, 62.0, 57.5, None]
weights["Brennan"] = [ 56.7, None, None, 55.2, 57.6, None, None, None, None, None, None, None, None, None, None, None, None, None, 61.4]
weights["Briggs"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 61.9]
weights["Duclair"] = [ None, None, None, None, None, 59.9, 59.4, None, None, None, None, None, 57.9, 56.2, 59.6, None, None, 56.6, None]
weights["Egan"] = [ None, None, None, None, None, 59.6, 58.4, None, None, None, None, None, 55.9, 56.4, 57.9, None, None, 55.9, 59.3]
weights["Elgin-ND"] = [ 54.7, None, 57.2, 55.8, 57.8, 61.0, 60.2, 59.2, 60.1, 58.5, 59.1, 57.0, 57.8, 56.8, 60.6, 62.4, 62.1, 57.8, 61.8]
weights["Faller"] = [ 53.0, None, 56.9, 57.3, 57.9, 60.3, 61.1, 60.8, 60.2, 60.1, 58.9, 57.2, 58.5, 57.1, 60.1, 61.3, 61.1, 56.5, 61.0]
weights["Faller (1.8M PLS)"] = [ None, None, None, 57.4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
weights["Filler (Glenn)"] = [ None, None, 59.3, 59.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
weights["Focus"] = [ 57.4, None, 58.2, 59.3, 59.3, 62.9, 62.8, 61.2, 61.5, 60.9, 59.8, 59.5, 62.1, 59.6, 60.6, None, None, 59.8, 62.4]
weights["Forefront"] = [ 56.4, None, None, 57.5, 57.9, None, None, None, None, None, None, None, None, None, None, None, None, None, 61.8]
weights["Freyr"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 61.6]
weights["Glenn"] = [ 58.1, None, 59.4, 59.4, 60.1, 63.9, 63.4, 63.0, None, None, None, None, 59.2, 60.1, 63.2, 65.0, 64.4, 60.7, 63.5]
weights["HRS 3100"] = [ None, None, None, None, None, None, None, 58.1, 57.3, 58.6, 56.4, 56.9, None, None, None, None, None, 57.2, None]
weights["HRS 3361"] = [ 55.2, None, 56.2, 54.5, 57.0, 60.3, 59.8, 58.7, 57.6, 58.0, 57.0, 56.6, 59.9, None, 60.1, None, None, 56.6, None]
weights["HRS 3419"] = [ 51.9, None, 57.1, 56.7, 57.5, 60.5, 60.1, 59.1, 59.8, 58.8, 58.1, 56.3, 59.2, 57.3, 59.5, 61.7, 61.4, 55.1, 60.3]
weights["HRS 3504"] = [ 54.1, None, 56.9, 54.8, 57.0, 60.9, 60.0, 58.2, 57.1, 57.9, 55.6, 56.1, 61.4, 56.7, 60.1, None, None, 56.9, None]
weights["HRS 3530"] = [ 52.3, None, 57.2, 58.8, 58.7, 62.3, 62.2, 60.8, 60.5, 59.3, 59.8, 58.6, 60.5, 55.4, 60.5, 61.7, 61.8, 56.8, 61.7]
weights["HRS 3616"] = [ 54.8, None, None, 53.7, 56.6, 60.4, 60.1, 59.4, 58.8, 58.0, 57.8, 56.9, 61.3, 57.2, 60.9, None, None, 57.4, 61]
weights["Jenna"] = [ 54.9, None, None, 55.4, 57.6, None, None, None, None, None, None, None, None, None, None, None, None, None, 61.2]
weights["Kelby"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 60.8]
weights["LCS Anchor"] = [ 58.0, None, None, 56.9, 58.0, None, None, 59.3, 59.8, 58.9, 57.3, 57.5, 60.9, 59.4, 61.6, None, None, 59.1, 61.2]
weights["LCS Breakaway"] = [ 57.4, None, 58.5, 57.6, 58.8, 62.7, 62.3, 61.7, 61.5, 60.0, 60.0, 58.8, 62.6, 58.8, 61.9, None, None, 59.4, None]
weights["LCS Iguacu"] = [ 56.4, None, 58.5, None, None, 62.0, 62.6, 60.7, None, None, None, None, 60.2, 60.2, 60.5, None, None, 58.7, 61.8]
weights["LCS Nitro"] = [ 53.7, None, 56.6, 55.5, 57.3, 60.9, 60.1, 60.0, None, None, None, None, 57.6, 57.3, 60.4, 61.1, 61.2, 56.1, 61.1]
weights["LCS Powerplay"] = [ 54.9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
weights["LCS Prime"] = [ 56.7, None, 57.8, 58.1, 59.0, 62.1, 62.5, 60.9, 60.3, 59.4, 59.1, 58.9, 60.1, 57.5, 61.4, 63.2, 62.9, 59.4, 62.5]
weights["LCS Pro"] = [ 56.2, None, None, None, None, 62.4, 61.4, 61.1, None, None, None, None, 62.1, 58.3, 61.6, 63.4, 62.4, 57.6, None]
weights["LCS Trigger"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, 57.3, None, None, None, None, None]
weights["Linkert"] = [ 55.5, None, 56.4, 57.4, 58.5, 61.4, 61.2, 59.7, 59.4, 59.3, 58.3, 56.8, 61.0, 57.8, 60.8, 62.8, 61.7, 58.1, 61.7]
weights["MN10261-1"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, 59.6, None, None, None, 59.3, None]
weights["Mott"] = [ 54.1, None, None, None, 57.7, 61.7, 61.1, None, None, None, None, None, 58.5, 58.5, 59.5, None, None, 57.5, 62.1]
weights["MS Chevelle"] = [ 56.6, None, 56.7, 54.6, 58.0, 61.1, 60.1, 58.5, None, None, None, None, 60.8, 58.0, 61.2, None, None, 58.3, 62.1]
weights["MS Stingray"] = [ 53.1, None, None, None, None, 60.2, 59.8, 58.8, None, None, None, None, 59.4, 55.7, 55.5, None, None, 56.9, None]
weights["ND901CL Plus"] = [ None, None, None, None, None, 61.3, 61.1, None, None, None, None, None, 61.8, 57.7, 60.7, None, None, 58.6, None]
weights["Prestige"] = [ 57.1, None, None, None, None, 60.7, 60.3, 59.4, None, None, None, None, 59.1, 58.3, 60.1, 61.7, 61.3, 56.1, 61.1]
weights["Prevail"] = [ 55.8, None, 56.6, 57.1, 57.8, 61.5, 61.2, 59.3, 59.6, 58.3, 57.9, 57.8, 60.2, 59.0, 60.2, 61.7, 61.3, 57.7, 61.1]
weights["Prosper"] = [ 53.5, None, 57.4, 56.9, 58.2, 60.3, 60.5, None, 59.8, 59.3, 59.1, 58.0, 59.5, 54.9, 60.8, 61.9, 61.5, 57.3, 61.4]
weights["RB07"] = [ 56.6, None, None, None, None, None, None, None, None, None, None, None, 58.6, None, 61.1, None, None, None, 60.8]
weights["Redstone"] = [ 52.6, None, None, None, None, 61.4, 59.9, 60.1, None, None, None, None, 58.9, 56.2, 60.3, 60.9, 61.3, 58.1, 60.3]
weights["Reeder"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 61.6]
weights["Rollag"] = [ 55.9, None, 57.1, 58.2, 58.8, 62.5, 61.7, 61.3, 60.2, 60.4, 59.9, 57.9, 60.7, 58.8, 61.2, None, None, 57.6, 62.1]
weights["Shelly"] = [ 53.8, None, 56.4, 56.7, 58.7, 62.2, 61.1, 59.7, 59.8, 58.8, 58.7, 56.6, 60.5, 56.8, 61.0, 62.0, 62.1, 58.3, None]
weights["Steele-ND"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 62.6]
weights["Surpass"] = [ 57.0, None, 56.3, 58.0, 57.9, 61.0, 61.4, 59.4, 60.0, 59.0, 57.8, 57.8, 60.7, 58.8, 61.0, None, None, None, None]
weights["SY Ingmar"] = [ 54.5, None, None, None, 58.1, 62.0, 60.6, 60.9, 59.2, 59.9, 59.2, 59.0, 62.4, 58.8, 61.1, 62.9, 63.1, 57.7, 62.9]
weights["SY-Rowyn"] = [ 54.5, None, None, 56.5, None, 61.6, 61.6, 60.1, 60.1, 59.9, 58.3, 59.2, 60.5, 58.3, 61.1, None, None, 57.1, None]
weights["SY-Soren"] = [ 55.2, None, 57.1, 54.7, 58.1, 60.6, 59.4, 60.6, 60.0, 59.4, 58.9, 58.0, 59.5, 57.9, 61.4, 62.6, 62.4, 58.4, 61.6]
weights["SY-Tyra"] = [ None, None, 57.4, None, None, 60.0, 58.7, None, None, None, None, None, 61.0, 57.6, 57.3, None, None, 58.6, None]
weights["SY-Valda"] = [ 54.7, None, None, 56.9, 58.1, 61.7, 61.9, 60.5, 59.7, 59.2, 58.4, 59.1, 61.0, 57.7, 57.4, 62.4, 62.2, 57.9, 62.2]
weights["SY605CL"] = [ None, None, None, None, None, 61.7, 60.4, None, None, None, None, None, 58.7, 59.1, 62.0, None, None, 59.1, None]
weights["TCG-Cornerstone"] = [ 54.6, None, None, None, None, 61.2, 60.9, 59.5, 58.5, 57.6, 57.9, 57.1, 59.2, 57.1, 61.5, None, None, 57.5, None]
weights["TCG-Spitfire"] = [ 53.0, None, None, None, None, 59.7, 59.4, 59.0, None, None, None, None, 60.6, 56.1, 58.6, None, None, 57.2, None]
weights["TCG-Wildfire"] = [ 52.9, None, None, None, None, 61.8, 60.7, 59.4, None, None, None, None, 58.6, 58.5, 59.8, None, None, 58.3, None]
weights["Vantage"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 62.9]
weights["Velva"] = [ 53.6, None, None, None, None, 60.2, 59.3, 57.7, None, None, None, None, 60.1, 56.2, 59.1, None, None, 58.2, 61.5]
weights["Vida"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 59.3]
weights["WB-Digger"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 60.7]
weights["WB-Mayville"] = [ 56.3, None, 56.8, 56.3, 57.5, 62.0, 61.6, 58.9, 57.6, 57.0, 57.1, 57.0, 60.1, 55.8, 59.6, None, None, 57.7, 60.5]
weights["WB-Mayville (1.8 M PLS)"] = [ 54.6, None, None, 57.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
weights["WB9312"] = [ None, None, None, None, None, 60.5, 61.6, None, None, None, None, None, 61.4, 55.8, 61.3, None, None, 57.8, None]
weights["WB9507"] = [ 52.2, None, 55.3, 54.9, 56.6, 59.3, 59.3, 59.2, 58.1, 57.7, 57.1, 56.9, 59.2, 53.9, 59.0, 60.2, 60.3, 55.1, 59.4]
weights["WB9653"] = [ 55.3, None, 56.3, 55.7, 57.5, 61.2, 60.8, 58.5, 56.6, 57.7, 55.7, 56.2, 60.4, 56.8, 60.5, None, None, 57.6, 61]

proteins = {}
proteins["07S0027-3 (SY Rockford)"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, 13.8, None, None, None, 13.6, None]
proteins["Advance"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 14.9]
proteins["Barlow"] = [ 15.5, None, 13.4, 15.2, 14.7, 13.9, 15.3, 14.8, None, None, None, None, 14.8, 14.5, 14.8, 13.4, 14.4, 14.2, 16.3]
proteins["Bolles"] = [ 17.3, None, 15.0, 16.0, 16.8, 15.3, 16.9, 15.9, 16.0, 15.9, 14.9, 15.9, 16.3, 15.8, 15.4, 13.6, 15.9, 16.0, 17.5]
proteins["Boost"] = [ 15.5, None, 13.9, 14.7, 14.8, 14.4, 15.5, 15.0, 15.7, 14.6, 14.2, 15.0, 15.7, 14.7, 15.2, 13.1, 14.2, 15.2, None]
proteins["Brennan"] = [ 16.0, None, None, 14.9, 14.5, None, None, None, None, None, None, None, None, None, None, None, None, None, 15.5]
proteins["Briggs"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.6]
proteins["Duclair"] = [ None, None, None, None, None, 14.0, 14.8, None, None, None, None, None, 13.9, 13.5, 14.6, None, None, 13.9, None]
proteins["Egan"] = [ None, None, None, None, None, 15.2, 15.5, None, None, None, None, None, 15.1, 14.8, 15.8, None, None, 15.7, 16.9]
proteins["Elgin-ND"] = [ 15.0, None, 13.3, 14.9, 14.1, 13.7, 14.9, 14.9, 14.9, 14.6, 13.6, 14.7, 13.9, 14.6, 14.9, 13.0, 14.1, 14.1, 16.0]
proteins["Faller"] = [ 15.5, None, 13.0, 14.1, 13.6, 13.4, 14.1, 13.6, 13.7, 13.8, 13.0, 14.0, 14.1, 13.2, 13.8, 13.0, 13.1, 13.4, 14.6]
proteins["Faller (1.8M PLS)"] = [ None, None, 3.0, 14.1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
proteins["Filler (Glenn)"] = [ None, None, 14.2, 14.7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
proteins["Focus"] = [ 15.4, None, 13.5, 14.1, 13.7, 13.5, 15.2, None, 13.9, 14.2, 13.2, 14.1, 14.5, 13.4, 14.3, None, None, 13.9, 16.6]
proteins["Forefront"] = [ 15.4, None, None, 14.1, 14.4, None, None, None, None, None, None, None, None, None, None, None, None, None, 15.4]
proteins["Freyr"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.3]
proteins["Glenn"] = [ 15.3, None, 13.5, 14.9, 14.7, 13.7, 14.8, 14.7, None, None, None, None, 15.3, 14.9, 15.0, 13.9, 14.5, 13.9, 16.2]
proteins["HRS 3100"] = [ None, None, None, None, None, None, None, 13.7, 14.1, 13.7, 13.0, 13.6, None, None, None, None, None, 14.0, None]
proteins["HRS 3361"] = [ 15.3, None, 12.9, 13.6, 14.1, 13.5, 14.3, 13.8, 14.2, 13.8, 12.9, 13.3, 14.0, 13.6, 14.4, None, None, 13.8, None]
proteins["HRS 3419"] = [ 14.7, None, 13.0, 13.8, 14.0, 13.0, 13.8, 13.3, 13.5, 13.1, 12.5, 14.4, 12.2, 13.4, 13.3, 13.4, 13.6, 14.0, 13.4]
proteins["HRS 3504"] = [ 14.8, None, 12.7, 13.6, 13.2, 13.8, 14.3, 13.4, 13.8, 13.2, 13.2, 13.9, 12.7, 13.4, 14.5, None, None, 13.3, None]
proteins["HRS 3530"] = [ 16.2, None, 13.4, 14.3, 14.8, 14.4, 15.0, 14.3, 14.5, 14.4, 13.5, 14.2, 14.4, 14.2, 14.2, 13.0, 13.3, 14.0, 13.9]
proteins["HRS 3616"] = [ 15.8, None, None, 15.8, 15.0, 14.4, 15.9, 15.3, 15.9, 15.5, 14.8, 14.7, 14.3, 14.3, 15.4, None, None, 14.7, 16.0]
proteins["Jenna"] = [ 15.7, None, None, 14.9, 14.1, None, None, None, None, None, None, None, None, None, None, None, None, None, 15.5]
proteins["Kelby"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.3]
proteins["LCS Anchor"] = [ 15.3, None, None, 14.6, 14.5, None, None, 14.7, 15.0, 14.7, 14.3, 14.1, 15.5, 13.9, 14.9, None, None, 14.6, 16.0]
proteins["LCS Breakaway"] = [ 16.1, None, 14.0, 14.8, 14.6, 14.3, 15.4, 14.1, 14.5, 14.7, 13.6, 14.4, 13.4, 13.6, 15.0, None, None, 14.9, None]
proteins["LCS Iguacu"] = [ 13.9, None, None, None, None, 12.3, 13.3, 12.4, None, None, None, None, 12.8, 12.3, 13.7, None, None, 13.1, 14.0]
proteins["LCS Nitro"] = [ 15.3, None, 13.5, 13.4, 12.9, 13.1, 14.0, 13.3, None, None, None, None, 13.8, 13.4, 13.3, 12.2, 11.8, 13.5, 14.1]
proteins["LCS Powerplay"] = [ 15.6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
proteins["LCS Prime"] = [ 14.4, None, 11.5, 13.2, 12.9, 13.1, 13.9, 13.5, 13.6, 13.1, 12.6, 13.1, 13.3, 13.0, 13.0, 11.3, 12.1, 12.8, 15.1]
proteins["LCS Pro"] = [ 15.4, None, None, None, None, 14.4, 15.4, 14.4, None, None, None, None, 13.7, 14.0, 14.9, 12.5, 13.9, 13.5, None]
proteins["LCS Trigger"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, 12.4, None, None, None, None, None]
proteins["Linkert"] = [ 16.0, None, 14.0, 14.4, 14.2, 14.3, 15.2, 15.1, 14.9, 14.7, 14.2, 14.3, 14.7, 14.7, 15.4, 14.5, 15.4, 14.6, 16.6]
proteins["MN10261-1"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, 14.4, None, None, None, 13.6, None]
proteins["Mott"] = [ 15.8, None, None, None, 14.4, 13.9, 14.9, None, None, None, None, None, 15.0, 14.5, 14.7, None, None, 15.1, 15.2]
proteins["MS Chevelle"] = [ 14.8, None, 12.4, 14.1, 13.5, 13.0, 14.3, 13.4, None, None, None, None, 12.5, 12.9, 13.4, None, None, 13.2, 14.1]
proteins["MS Stingray"] = [ 13.3, None, None, None, None, 11.6, 12.8, 11.6, None, None, None, None, 12.6, 12.6, 12.2, None, None, 12.3, None]
proteins["ND901CL Plus"] = [ None, None, None, None, None, 14.9, 15.8, None, None, None, None, None, 14.9, 15.2, 16.6, None, None, 15.5, None]
proteins["Prestige"] = [ 15.4, None, None, None, None, 14.0, 14.7, 14.5, None, None, None, None, 13.8, 13.4, 14.7, 13.4, 13.4, 14.1, 13.6]
proteins["Prevail"] = [ 15.3, None, 13.3, 13.8, 13.9, 13.3, 14.3, 14.3, 13.8, 13.7, 13.3, 13.5, 13.7, 13.6, 13.9, 13.3, 13.4, 13.6, 15.4]
proteins["Prosper"] = [ 15.4, None, 13.0, 14.3, 13.8, 13.3, 14.3, 13.8, 14.0, 13.9, 13.1, 13.9, 14.2, 13.3, 14.2, 12.5, 13.3, 13.9, 15.4]
proteins["RB07"] = [ 16.2, None, None, None, None, None, None, None, None, None, None, None, 15.3, None, 15.0, None, None, None, 16.3]
proteins["Redstone"] = [ 14.9, None, None, None, None, 13.6, 14.8, 13.4, None, None, None, None, 12.4, 13.4, 13.2, 12.3, 13.1, 13.7, 15.9]
proteins["Reeder"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.0]
proteins["Rollag"] = [ 16.1, None, 14.2, 15.0, 14.8, 14.2, 14.2, 14.8, 15.3, 14.6, 14.3, 15.0, 14.2, 14.5, 15.2, None, None, 14.7, 16.2]
proteins["Shelly"] = [ 15.5, None, 13.5, 14.1, 13.9, 13.0, 13.0, 14.0, 14.1, 13.8, 13.1, 14.4, None, 13.7, 14.0, 12.8, 13.4, 13.4, None]
proteins["Steele-ND"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.2]
proteins["Surpass"] = [ 14.8, None, 12.5, 13.9, 13.9, 13.9, 13.9, 14.2, 14.1, 14.1, 13.0, 14.0, None, 13.4, 13.9, None, None, 13.5, None]
proteins["SY Ingmar"] = [ 15.7, None, None, None, 12.5, 14.1, 14.1, 15.1, 15.3, 14.9, 14.1, 14.4, 14.0, 14.3, 14.4, 13.3, 14.3, 14.5, 15.6]
proteins["SY-Rowyn"] = [ 15.7, None, None, 13.9, None, 13.9, 13.9, 14.1, 14.3, 14.2, 13.3, 13.7, 13.6, 13.8, 14.3, None, None, 14.0, None]
proteins["SY-Soren"] = [ 15.7, None, 13.9, 14.8, 14.1, 14.0, 14.0, 14.5, 14.8, 14.8, 13.9, 13.6, 14.5, 14.5, 14.8, 13.5, 13.5, 14.6, 15.3]
proteins["SY-Tyra"] = [ None, None, None, None, None, 13.7, 13.7, None, None, None, None, None, 13.3, 13.3, 13.6, None, None, 13.6, None]
proteins["SY-Valda"] = [ 15.3, None, 12.2, 14.0, 13.4, 13.5, 13.5, 13.9, 14.6, 13.9, 13.3, 14.0, 12.9, 13.4, 14.0, 12.6, 12.8, 13.6, 15.7]
proteins["SY605CL"] = [ None, None, None, None, None, 14.4, 14.4, None, None, None, None, None, 14.1, 14.2, 14.7, None, None, 14.2, None]
proteins["TCG-Cornerstone"] = [ 15.8, None, None, None, None, 14.4, 14.4, 14.5, 14.6, 14.7, 14.2, 14.2, 14.8, 14.3, 14.8, None, None, 15.4, None]
proteins["TCG-Spitfire"] = [ 15.3, None, None, None, None, 13.9, 13.9, 14.2, None, None, None, None, 14.3, 13.8, 14.3, None, None, 14.0, None]
proteins["TCG-Wildfire"] = [ 15.9, None, None, None, None, 14.2, 14.2, 14.2, None, None, None, None, 14.2, 13.7, 14.9, None, None, 14.1, None]
proteins["Vantage"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.3]
proteins["Velva"] = [ 15.2, None, None, None, None, 14.2, 14.9, 14.8, None, None, None, None, 14.3, 13.7, 14.4, None, None, 13.8, 15.4]
proteins["Vida"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.1]
proteins["WB-Digger"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.0]
proteins["WB-Mayville"] = [ 16.3, None, 13.4, 14.2, 14.4, 14.6, 15.3, 14.7, 14.7, 14.9, 14.2, 14.3, 15.1, 13.9, 14.9, None, None, 14.6, 16.6]
proteins["WB-Mayville (1.8 M PLS)"] = [ 16.6, None, None, 14.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
proteins["WB9312"] = [ None, None, None, None, None, 12.6, 12.8, None, None, None, None, None, 12.8, 12.2, 12.8, None, None, 13.2, None]
proteins["WB9507"] = [ 15.5, None, 14.0, 14.3, 13.7, 13.7, 14.5, 13.7, 13.5, 14.2, 12.5, 14.0, 13.7, 13.3, 15, 13.1, 13.3, 14.1, 15.4]
proteins["WB9653"] = [ 15.5, None, 12.1, 13.8, 13.5, 13.3, 14.1, 13.4, 13.9, 13.3, 12.7, 13.9, 14.3, 13.2, 14, None, None, 13.7, 15.3]


planted = models.Date.objects.filter(date__year=2016, date__month=5)[0]
harvested = models.Date.objects.filter(date__year=2016, date__month=8)[0]

for vname in yields:
	for i in range(len(yield_lsds)):
		tags = None
		hidden = False
		bushels = yields[vname][i]
		if bushels is None:
			continue
		lname, lsd10, lsd5 = yield_lsds[i]
		if lname in rename_locations:
			lname, tags = rename_locations[lname]
		if tags is not None and tags is not "dryland":
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
