#$ python manage.py shell
from variety_trials_data import models

## source "Selection tool data 2017.xlsx" sent Nov/13/2017, 09:29 CST

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
		"LREC-Park",
		"LREC-Pekin",
		"Dickinson",
		"Hettinger",
		"Minot",
		"Garrison",
		"Mohall",
		"Williston",
		"Williston-Irr",
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
rename_locations["LREC-Park"] = ("Park River", None)
rename_locations["LREC-Pekin"] = ("Pekin", None)
rename_locations["Garrison"] = ("McLean County", None)
rename_locations["Williston"] = ("Williston", "dryland")
rename_locations["Williston-Irr"] = ("Williston", "irrigated")

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
		"AFK-Astro",
		"Ambush",
		"Barlow",
		"Bolles",
		"Boost",
		"Caliber",
		"Egan",
		"Elgin-ND",
		"Faller",
		"Faller (1.8M PLS)",
		"Glenn",
		"HRS 3100",
		"HRS 3419",
		"HRS 3504",
		"HRS 3530",
		"HRS 3616",
		"Lang-MN",
		"LCS Anchor",
		"LCS Breakaway",
		"LCS Nitro",
		"LCS Prime",
		"LCS Rebel",
		"LCS Trigger",
		"Linkert",
		"Mott",
		"MS Camaro",
		"MS Chevelle",
		"ND901CL Plus",
		"ND VitPro",
		"Prestige",
		"Prevail",
		"Prosper",
		"Prosper/ND VitPro",
		"Redstone",
		"Rollag",
		"Shelly",
		"Shelly/Bolles",
		"Surpass",
		"SY Ingmar",
		"SY Rockford",
		"SY-Rowyn",
		"SY-Rustler",
		"SY-Soren",
		"SY-Valda",
		"TCG-Climax",
		"TCG-Cornerstone",
		"TCG-Spitfire",
		"Velva",
		"WB9479",
		"WB9590",
		"WB9653",
		"WB9719",
		"WB-Mayville",
		"WB-Mayville (1.8 M PLS)",
	]

rename_varieties = {}
rename_varieties["AFK-Astro"] = "AFK Astro"
rename_varieties["Prosper/ND VitPro"] = "Mix (Proper / ND VitPro)"
rename_varieties["Shelly/Bolles"] = "Mix (Shelly / Bolles)"
rename_varieties["Elgin-ND"] = "Elgin"
rename_varieties["SY-Rustler"] = "SY Rustler"
rename_varieties["SY-Rowyn"] = "SY Rowyn"
rename_varieties["SY-Soren"] = "SY Soren"
rename_varieties["SY-Tyra"] = "SY Tyra"
rename_varieties["SY-Valda"] = "SY Valda"
rename_varieties["SY-Valda"] = "SY Valda"
rename_varieties["ND901CL Plus"] = "ND 901CL Plus"
rename_varieties["SY605CL"] = "SY605 CL"
rename_varieties["WB9879CLP+"] = "WB9879CLP Plus"
rename_varieties["07S0027-3 (SY Rockford)"] = "SY Rockford 07S0027-3"
rename_varieties["TCG-Climax"] = "TCG Climax"
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
		("Carr-Dry", None, None),
		("Carr-Irr", None, None),
		("Carr-Elite", None, None),
		("CREC-Dazey", None, None),
		("CREC-Wishek", None, None),
		("Casselton", None, None),
		("Prosper", None, None),
		("Langdon", None, None),
		("LREC-Cando", None, None),
		("LREC-Cavalier", None, None),
		("LREC-Park", None, None),
		("LREC-Pekin", None, None),
		("Dickinson", None, None),
		("Hettinger", None, None),
		("Minot", None, None),
		("Garrison", None, None),
		("Mohall", None, None),
		("Williston", None, None),
		("Williston-Irr", None, None),
	]

# regexps to help transform tab-delimited copy+paste from source workbook
# s/\t/, /
# s/$/]/
# s/^/yields["/
# s/^([^,]+), /\1"]=[/
yields = {}
yields["AFK-Astro"] = [55.6, 76.3, None, None, None, 101.7, 79.7, 56.1, None, None, None, None, 37.6, 37.9, 56.6, None, None, 25.2, None]
yields["Ambush"] = [ 59.7, 70.8, None, None, None, 86.5, 77.5, 71.6, None, None, None, None, 34.1, 36.3, 48.1, None, None, 26.6, None]
yields["Barlow"] = [ 57.1, 68.1, 53.7, 84.4, 36.5, 91.5, 78.9, 74.3, None, None, None, None, 38.1, 40.1, 48.2, 16.4, 82.8, 28.0, 101.8]
yields["Bolles"] = [ 60.0, 70.6, 53.3, 83.5, 37.1, 97.8, 74.8, 74.1, 50.3, 76.2, 85.5, 81.0, 34.4, 32.8, 48.6, 18.6, 68.7, 25.7, 107.6]
yields["Boost"] = [ 58.4, 72.1, 52.0, 86.2, 35.3, 88.2, 79.4, 78.9, 60.1, 77.6, 86.1, 77.8, 34.7, 31.2, 49.3, 17.5, 79.2, 29.2, 96.1]
yields["Caliber"] = [ 54.7, 73.5, None, None, None, 84.6, 74.4, 63.1, None, None, None, None, 31.6, 32.5, 48.0, None, None, 29.0, None]
yields["Egan"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, 48.3, None, None, 29.4, 96.5]
yields["Elgin-ND"] = [ 57.7, 70.4, 53.6, 90.5, 32.8, 91.3, 81.5, 81.4, 61.2, 80.3, 90.0, 75.9, 36.2, 38.4, 50.8, 20.3, 79.1, 28.7, 103.5]
yields["Faller"] = [ 58.6, 83.5, 51.5, 91.2, 30.0, 94.6, 92.0, 82.2, 59.2, 96.3, 88.8, 94.2, 34.5, 41.5, 49.9, 17.5, 74.2, 25.1, 116.9]
yields["Faller (1.8M PLS)"] = [ 57.9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
yields["Glenn"] = [ 56.5, 75.6, 49.6, 83.6, 29.2, 88.4, 70.6, 71.1, None, None, None, None, 34.9, 32.1, 50.6, 18.9, 73.8, 29.3, 98.3]
yields["HRS 3100"] = [ 59.3, 78.5, None, 91.9, 40.7, 100.3, 88.6, 75.3, 51.2, 79.0, 83.1, 84.8, 34.3, 36.3, 38.9, None, None, 29.4, None]
yields["HRS 3419"] = [ 58.7, 83.0, 64.5, 100.8, 37.2, 103.8, 73.7, 92.4, 47.5, 93.8, 98.4, 85.8, 30.7, 41.2, 53.4, 14.3, 68.5, 24.9, 105.5]
yields["HRS 3504"] = [ 61.2, 80.0, None, 88.6, 38.3, 100.0, 90.1, 76.8, 43.2, 74.8, 81.8, 81.4, 34.8, 32.7, 43.6, None, None, 230.8, 103.2]
yields["HRS 3530"] = [ 57.9, 90.9, 58.7, 94.1, 37.5, 97.1, 85.6, 78.9, 51.3, 88.0, 93.5, 91.6, 33.1, 35.9, 51.3, 19.6, 71.2, 27.7, None]
yields["HRS 3616"] = [ 61.1, 70.7, 60.0, 92.1, 35.7, 97.3, 74.2, 75.6, 58.1, 79.1, 86.4, 77.8, 32.7, 38.7, 48.3, None, None, 29.0, None]
yields["Lang-MN"] = [ 58.8, 83.2, 60.7, 86.4, 39.3, 93.0, 81.5, 77.6, 57.9, 80.4, 82.2, 70.5, 35.7, 36.3, 46.9, 21.8, 75.3, 27.5, None]
yields["LCS Anchor"] = [ 51.5, 71.0, 54.1, None, None, 91.9, 74.8, 69.0, None, None, None, None, 34.3, 35.7, 34.6, None, None, 31.9, 108.4]
yields["LCS Breakaway"] = [ 50.4, 77.7, 49.7, 84.4, 30.6, 92.3, 84.9, 75.4, 48.8, 60.1, 82.9, 78.6, 32.7, 34.8, 34.9, None, None, 28.4, None]
yields["LCS Nitro"] = [ 57.2, 76.6, None, None, None, 95.9, 65.6, 92.4, None, None, None, None, 32.8, 35.4, 49.0, 20.3, 66.7, 28.6, 104.8]
yields["LCS Prime"] = [ 60.8, 81.6, None, None, None, 100.5, 91.3, 87.5, 54.7, 65.7, 94.0, 89.0, 36.2, 39.2, 44.7, 22.4, 83.4, 28.6, 116.3]
yields["LCS Rebel"] = [ 57.1, 75.7, 59.5, 88.4, 39.2, 97.7, 89.0, 84.2, 59.5, 82.9, 84.4, 84.6, 33.3, 36.8, 46.8, None, None, 27.6, 98.8]
yields["LCS Trigger"] = [ 63.6, 77.4, 63.3, 94.0, 41.2, 115.2, 98.8, 98.3, None, None, None, None, 34.0, 44.5, 49.2, None, None, 21.3, 108.7]
yields["Linkert"] = [ 57.0, 76.8, 53.5, 81.3, 36.6, 88.0, 76.5, 63.8, 47.5, 68.8, 81.7, 72.7, 32.8, 34.0, 39.2, 20.1, 83.4, 27.5, 111.3]
yields["Mott"] = [ 58.6, None, None, None, 37.4, 97.8, 76.1, None, None, None, None, None, 29.8, 36.6, 42.9, None, None, 21.9, 102.7]
yields["MS Camaro"] = [ 53.0, 72.6, None, None, None, 85.4, 74.7, 66.6, 48.4, 73.1, 86.2, 76.2, 33.5, 31.4, 46.9, None, None, 30.3, 107.4]
yields["MS Chevelle"] = [ 60.5, 71.3, None, None, None, 98.2, 85.6, 86.2, 68.1, 83.6, 88.3, 88.1, 35.3, 37.5, 45.2, None, None, 29.4, 109.2]
yields["ND901CL Plus"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, 54.5, None, None, None, None]
yields["ND VitPro"] = [ 56.4, 74.3, 55.5, 83.4, 35.1, 88.8, 68.5, 71.6, 49.0, 73.0, 79.6, 70.6, 28.8, 31.9, 35.2, 24.2, 75.8, 27.8, 102.7]
yields["Prestige"] = [ 59.7, None, None, None, None, None, None, None, None, None, None, None, None, 32.6, None, None, None, 29.7, 105.2]
yields["Prevail"] = [ 62.4, 84.6, 52.7, 86.5, 37.7, 93.8, 87.7, 76.0, None, None, None, None, 38.4, 38.3, 48.9, None, None, 30.3, 106.1]
yields["Prosper"] = [ 63.1, 82.1, 55.0, 95.4, 35.0, 97.5, 88.4, 82.5, 58.1, 93.2, 90.5, 85.7, 33.6, 39.5, 55.4, 17.6, 65.1, 25.0, 113.8]
yields["Prosper/ND VitPro"] = [ 59.9, 70.8, 53.5, 89.3, 36.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
yields["Redstone"] = [ 63.5, None, None, None, None, None, None, None, None, None, None, None, None, 38.3, 55.6, 14.4, 68.3, 20.0, 109.9]
yields["Rollag"] = [ 58.6, 68.9, 45.3, 81.7, 36.7, 89.6, 82.8, 75.7, 48.9, 81.7, 80.5, 78.2, 37.1, 31.6, 53.6, None, None, 31.4, 108.8]
yields["Shelly"] = [ 66.3, 78.9, 51.8, 96.7, 42.3, 101.1, 93.6, 81.4, 62.8, 88.3, 86.9, 89.9, 39.3, 43.9, 47.1, 19.9, 82.4, 28.4, None]
yields["Shelly/Bolles"] = [ 64.7, 74.0, None, 86.1, 32.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
yields["Surpass"] = [ 60.6, 72.9, 52.0, 83.6, 34.1, 99.8, 93.5, 80.2, 57.2, 79.2, 89.3, 80.6, 35.6, 36.7, 40.7, 10.4, 88.3, 30.1, 110.3]
yields["SY Ingmar"] = [ 57.0, 68.1, 59.0, 80.9, 42.0, 93.6, 83.4, 74.0, 42.8, 78.1, 79.9, 78.7, 37.0, 39.9, 47.7, 17.2, 80.3, 28.0, 111.4]
yields["SY Rockford"] = [ None, None, None, None, None, None, None, None, None, None, None, None, 38.6, 39.3, 50.6, None, None, 33.2, 115.4]
yields["SY-Rowyn"] = [ 55.7, 71.3, None, None, 42.9, 87.3, 81.0, 85.6, 47.2, 85.6, 88.6, 85.1, 29.1, 33.3, 46.6, 17.7, 71.1, 28.8, None]
yields["SY-Rustler"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, 34.9, None, None, None, None, None]
yields["SY-Soren"] = [ 60.0, 64.3, 61.1, 87.6, None, 92.5, 84.7, 75.9, 41.9, 77.6, 82.4, 78.3, 32.5, 36.5, 50.8, 17.1, 75.6, 30.1, 111.3]
yields["SY-Valda"] = [ 66.9, 87.5, 55.1, 92.2, 45.6, 100.3, 99.1, 84.5, 54.0, 85.7, 90.3, 90.8, 38.7, 35.1, 43.7, 22.8, 84.4, 29.3, 112.4]
yields["TCG-Climax"] = [ 63.0, 79.3, 57.3, None, None, 84.6, 71.5, 71.9, None, None, None, None, 33.9, 34.5, 48.8, None, None, 25.5, 100.8]
yields["TCG-Cornerstone"] = [ 55.2, 67.9, None, None, None, 89.2, 85.3, 63.7, None, None, None, None, 36.5, 362.1, 44.0, None, None, 26.8, 97.1]
yields["TCG-Spitfire"] = [ 66.3, 68.4, None, None, None, 96.7, 85.6, 76.2, None, None, None, None, 35.0, 37.6, 64.0, None, None, 29.3, 115.9]
yields["Velva"] = [ None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 30.7, 101.6]
yields["WB9479"] = [ 57.5, 80.2, 57.5, 90.1, 35.8, 98.6, 80.5, 75.4, 57.0, 76.8, 83.2, 88.3, 28.4, 34.4, 54.2, None, None, 29.1, None]
yields["WB9590"] = [ 63.4, 81.6, 56.1, 91.0, 36.5, 94.2, 83.2, 72.1, 42.3, 79.4, 84.0, 89.5, 34.3, 37.6, 51.6, None, None, 26.3, None]
yields["WB9653"] = [ 64.9, 76.3, None, None, None, 103.8, 90.8, 82.7, None, None, None, None, 37.3, 39.4, 47.7, 22.2, 76.1, 31.6, None]
yields["WB9719"] = [ 58.6, 67.5, 66.8, 96.5, 46.8, 89.6, 91.5, 69.5, None, None, None, None, 38.7, 43.4, 58.3, None, None, 28.1, None]
yields["WB-Mayville"] = [ 54.9, 72.2, 51.8, 88.7, 37.9, 89.4, 81.9, 57.5, 43.2, 66.9, 83.0, 79.4, 37.6, 32.6, 49.8, None, None, 38.8, None]
yields["WB-Mayville (1.8 M PLS)"] = [ 58.8, 73.3, None, 89.5, 36.6, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

weights = {}
weights["AFK-Astro"]=[55.5, 56.8, None, None, None, 58.2, 59.4, 54.3, None, None, None, None, 60.0, 61.1, 58.4, None, None, 48.2, None]
weights["Ambush"]=[60, 61.3, None, None, None, 61.9, 62.2, 61.5, None, None, None, None, 60.3, 61.6, 60.5, None, None, 49.5, None]
weights["Barlow"]=[59.7, 60.6, 60.2, 61.1, 59.9, 61.3, 62.0, 61.5, None, None, None, None, 61.5, 62.2, 61.1, 55.5, 60.9, 50.4, 61.9]
weights["Bolles"]=[58.7, 58.9, 58.6, 59.7, 57.4, 60.2, 60.4, 61.2, 55.6, 61.4, 60.9, 61.8, 57.8, 59.3, 58.8, 53.0, 58.2, 50.9, 60]
weights["Boost"]=[58.7, 59.4, 59.2, 60.2, 57.3, 61.2, 60.9, 60.7, 58.4, 60.0, 61.2, 61.1, 59.0, 59.0, 59.4, 54.4, 60.3, 49.6, 59.4]
weights["Caliber"]=[59.1, 60.5, None, None, None, 61.1, 61.5, 59.8, None, None, None, None, 60.9, 61.6, 59.2, None, None, 50.8, None]
weights["Egan"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 57.3, None, None, 48.3, 58.8]
weights["Elgin-ND"]=[57.9, 59.8, 59.3, 59.9, 57.5, 60.5, 61.7, 61.1, 57.3, 61.1, 61.9, 61.5, 58.6, 60.9, 58.9, 52.1, 58.1, 47.3, 60.1]
weights["Faller"]=[58.0, 60.1, 58.1, 60.7, 57.3, 60.3, 61.4, 61.5, 57.1, 62.5, 60.3, 62.1, 58.1, 60.3, 58.4, 52.2, 56.9, 47.1, 59.5]
weights["Faller (1.8M PLS)"]=[58.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
weights["Glenn"]=[61.2, 62.9, 62.4, 62.7, 61.1, 63.1, 63.4, 63.8, None, None, None, None, 61.9, 60.8, 60.8, 55.2, 61.4, 52.7, 63.0]
weights["HRS 3100"]=[57.4, 58.9, None, 59.4, 57.1, 60.6, 60.4, 60.1, 53.8, 59.9, 59.9, 60.6, 58.9, 60.6, 59.7, None, None, 48.4, None]
weights["HRS 3419"]=[55.6, 58.8, 57.8, 59.7, 56.7, 59.7, 60.6, 61.6, 54.5, 60.7, 60.6, 61.8, 56.9, 59.7, 58.7, 52.4, 57.1, 48.9, 58.4]
weights["HRS 3504"]=[56.2, 57.9, None, 58.2, 57.3, 60.4, 59.1, 59.0, 51.8, 59.6, 58.3, 60.7, 59.9, 61.3, 59.3, None, None, 48.8, 58.6]
weights["HRS 3530"]=[57.4, 60.3, 59.3, 60.4, 58.6, 60.5, 61.4, 61.3, 55.5, 61.3, 61.7, 62.2, 56.9, 59.8, 57.7, 53.1, 57.5, 48.1, 59.3]
weights["HRS 3616"]=[57.7, 58.4, 59.3, 59.9, 57.0, 60.5, 60.2, 61.5, 56.1, 60.6, 59.7, 60.6, 58.5, 60.4, 58.7, None, None, 50.6, None]
weights["Lang-MN"]=[59.2, 61.8, 60.8, 61.6, 58.7, 62.1, 61.8, 63.3, 60.4, 63.0, 62.9, 62.5, 59.4, 61.1, 59.1, 54.4, 60.2, 50.1, None]
weights["LCS Anchor"]=[59.2, 60.0, 59.8, None, None, 61.0, 59.8, 61.8, None, None, None, None, 60.8, 61.9, 61.0, None, None, 51.5, 60.8]
weights["LCS Breakaway"]=[59.7, 61.5, 60.6, 61.8, 59.3, 60.8, 62.2, 61.8, 56.8, 61.6, 62.2, 63.0, 61.6, 62.6, 59.8, None, None, 51.6, None]
weights["LCS Nitro"]=[56.7, 58.0, None, None, None, 58.9, 61.3, 62.2, None, None, None, None, 57.4, 59.5, 57.6, 53.5, 56.1, 50.3, 59.2]
weights["LCS Prime"]=[60.0, 60.8, None, None, None, 61.7, 62.9, 61.4, 58.3, 62.5, 62.0, 62.1, 61.4, 63.2, 60.7, 56.5, 59.4, 51.7, 61.3]
weights["LCS Rebel"]=[59.7, 61.0, 61.2, 61.7, 59.8, 61.7, 63.0, 62.4, 59.5, 62.1, 62.5, 63.4, 60.5, 61.9, 55.7, None, None, 51.4, 61.3]
weights["LCS Trigger"]=[57.7, 59.0, 59.4, 61.3, 58.7, 61.8, 61.9, 62.3, None, None, None, None, 56.3, 61.8, 57.3, None, None, 45.8, 58.5]
weights["Linkert"]=[58.9, 59.9, 59.1, 60.6, 57.9, 59.7, 61.3, 60.8, 55.7, 61.0, 61.3, 61.5, 60.4, 62.4, 61.0, 56.7, 60.2, 50.5, 60.6]
weights["Mott"]=[57.8, None, None, None, 57.8, 60.7, 60.6, None, None, None, None, None, 60.3, 60.3, 58.8, None, None, 49.8, 59.8]
weights["MS Camaro"]=[59.5, 59.8, None, None, None, 61.3, 61.0, 61.6, 57.5, 61.3, 59.9, 61.5, 60.3, 60.8, 59.6, None, None, 52.2, 60.7]
weights["MS Chevelle"]=[58.6, 57.9, None, None, None, 60.8, 61.0, 61.3, 57.3, 61.1, 59.4, 61.8, 59.9, 60.9, 60.2, None, None, 51.1, 58.8]
weights["ND901CL Plus"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0.4, None, None, None, None]
weights["ND VitPro"]=[60.0, 61.8, 61.5, 62.0, 59.9, 62.1, 63.0, 62.7, 59.0, 63.0, 62.8, 62.9, 61.6, 62.1, 61.2, 55.3, 60.5, 49.7, 61.5]
weights["Prestige"]=[58.1, None, None, None, None, None, None, None, None, None, None, None, None, 60.7, None, None, None, 49.4, 59.1]
weights["Prevail"]=[58.9, 59.4, 59.3, 60.1, 57.4, 59.8, 61.6, 61.4, None, None, None, None, 59.1, 62.3, 60.6, None, None, 49.2, 59.8]
weights["Prosper"]=[58.4, 59.3, 58.9, 60.7, 57.2, 60.2, 61.5, 60.8, 57.2, 62.1, 60.7, 61.9, 58.3, 60.6, 59.1, 51.8, 56.3, 47.7, 60.1]
weights["Prosper/ND VitPro"]=[58.6, 60.1, 59.7, 61.5, 58.1, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
weights["Redstone"]=[57.4, None, None, None, None, None, None, None, None, None, None, None, None, 60.7, 58.8, 53.8, 57.4, 49.1, 59.3]
weights["Rollag"]=[59.1, 60.1, 59.6, 61.4, 58.8, 61.2, 62.3, 62.4, 57.6, 62.4, 62.2, 62.6, 60.1, 61.1, 60.2, None, None, 50.0, 61.6]
weights["Shelly"]=[58.4, 59.4, 59.1, 61.4, 59.2, 60.9, 61.1, 61.9, 59.4, 62.7, 61.1, 62.4, 59.9, 62.2, 60.2, 53.7, 60.1, 50.4, None]
weights["Shelly/Bolles"]=[58.5, 58.4, None, 60.5, 58.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
weights["Surpass"]=[58.0, 58.2, 58.4, 59.4, 58.3, 59.3, 60.4, 60.9, 58.6, 61.6, 60.1, 61.4, 60.8, 61.2, 60.6, 53.7, 59.7, 49.9, 59.4]
weights["SY Ingmar"]=[59.6, 59.6, 60.3, 60.6, 58.8, 61.8, 62.0, 61.1, 54.4, 61.3, 61.6, 61.8, 58.3, 62.0, 60.5, 54.0, 60.1, 49.2, 60.4]
weights["SY Rockford"]=[None, None, None, None, None, None, None, None, None, None, None, None, 57.9, 59.1, 56.9, None, None, 48.7, 58.9]
weights["SY-Rowyn"]=[58.2, 59.0, None, None, None, 59.8, 61.3, 62.0, 55.8, 61.7, 60.9, 61.7, 58.4, 61.6, 59.0, 53.5, 58.2, 50.3, None]
weights["SY-Rustler"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, 59.6, None, None, None, None, None]
weights["SY-Soren"]=[59.3, 59.4, 59.7, 60.6, 59.2, 61.2, 61.7, 61.3, 54.8, 61.3, 61.4, 61.4, 60.5, 61.4, 61.0, 54.0, 58.9, 49.8, 61.2]
weights["SY-Valda"]=[58.6, 60.4, 59.7, 60.4, 60.2, 60.7, 62.1, 60.3, 56.3, 60.6, 61.7, 61.6, 59.6, 61.1, 58.9, 55.1, 60.3, 49.9, 60]
weights["TCG-Climax"]=[61.0, 62.6, 62.0, None, None, 62.4, 63.2, 62.8, None, None, None, None, 60.1, 59.9, 60.6, None, None, 52.5, 62.1]
weights["TCG-Cornerstone"]=[58.4, 60.1, None, None, None, 61.3, 61.0, 58.9, None, None, None, None, 60.4, 60.3, 57.8, None, None, 50.0, 60.2]
weights["TCG-Spitfire"]=[58.4, 59.0, None, None, None, 60.8, 62.0, 59.8, None, None, None, None, 58.0, 60.4, 58.4, None, None, 49.2, 59.6]
weights["Velva"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 48.7, None]
weights["WB9479"]=[58.5, 60.6, 59.4, 60.8, 58.2, 61.8, 61.8, 61.0, 55.9, 60.6, 61.5, 62.8, 60.6, 62.3, 57.7, None, None, 49.9, None]
weights["WB9590"]=[57.7, 59.4, 58.8, 60.6, 58.0, 60.5, 61.8, 60.4, 54.1, 60.6, 60.9, 62.0, 60.3, 61.3, 59.2, None, None, 49.8, None]
weights["WB9653"]=[56.3, 57.6, None, None, None, 60.0, 59.5, 58.8, None, None, None, None, 59.5, 61.7, 58.9, 54.0, 56.9, 47.9, None]
weights["WB9719"]=[60.7, 62.2, 62.0, 62.7, 61.9, 62.0, 63.5, 61.9, None, None, None, None, 62.3, 62.3, 61.5, None, None, 51.2, None]
weights["WB-Mayville"]=[58.9, 59.7, 58.7, 60.6, 58.4, 61.3, 61.6, 58.5, 53.8, 59.4, 61.3, 61.6, 60.8, 61.5, 59.3, None, None, 49.5, 60.4]
weights["WB-Mayville (1.8 M PLS)"]=[59.5, 59.8, None, 60.8, 58.2, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

proteins = {}
proteins["AFK-Astro"]=[13.8, 13.0, None, None, None, 12.3, 12.8, 12.3, None, None, None, None, 14.8, 11.5, 14.3, None, None, 17.4, None]
proteins["Ambush"]=[14.6, 15.4, None, None, None, 15, 14.7, 13.8, None, None, None, None, 17.1, 13.7, 16.1, None, None, 18.8, None]
proteins["Barlow"]=[14.7, 16.0, 13.6, 15.1, 36.5, 14.6, 14.7, 13.8, None, None, None, None, 17.3, 13.6, 16.0, 16.1, 14.0, 18.6, 15.3]
proteins["Bolles"]=[16.1, 16.3, 14.7, 16.9, 37.1, 16.6, 16.3, 15.0, 16.3, 15.3, 14.9, 15.3, 18.3, 15.5, 17.3, 16.7, 15.5, 19.7, 15.0]
proteins["Boost"]=[15.1, 15.4, 13.9, 14.6, 35.3, 15.2, 14.7, 13.3, 14.8, 14.1, 14.1, 14.2, 17.4, 14.9, 16.3, 15.8, 14.3, 18.3, 14.9]
proteins["Caliber"]=[15.6, 15.6, None, None, None, 15.4, 15.4, 14.7, None, None, None, None, 16.8, 14.1, 16.1, None, None, 17.7, None]
proteins["Egan"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 17.4, None, None, 19.5, 15.7]
proteins["Elgin-ND"]=[14.8, 15.3, 13.4, 14.9, 32.8, 14.9, 14.9, 13.5, 14.3, 13.8, 14.3, 13.9, 17.0, 13.8, 15.8, 15.5, 14.0, 18.9, 15.6]
proteins["Faller"]=[13.6, 14.3, 13.0, 13.5, 30.0, 13.2, 13.0, 11.7, 14.3, 13.0, 12.5, 13.1, 16.4, 13.8, 15.7, 15.4, 13.0, 18.2, 14.4]
proteins["Faller (1.8M PLS)"]=[13.7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
proteins["Glenn"]=[14.4, 16.0, 14.1, 15.5, 29.2, 15.3, 14.4, 14.3, None, None, None, None, 17.0, 14.3, 16.1, 15.6, 14.8, 18.0, 15.5]
proteins["HRS 3100"]=[14.7, 14.5, None, 14.1, 40.7, 14.5, 14.0, 13.0, 14.6, 12.9, 13.2, 13.5, 17.1, 14.1, 16.8, None, None, 18.3, None]
proteins["HRS 3419"]=[14.4, 13.1, 12.0, 13.1, 37.2, 13.4, 12.9, 12.3, 14.3, 12.5, 12.5, 12.9, 17.8, 13.4, 15.2, 16.1, 13.2, 20.4, 14.6]
proteins["HRS 3504"]=[15.0, 14.0, None, 13.8, 38.3, 14.1, 14.1, 12.8, 14.7, 13.1, 13.3, 13.4, 16.5, 14.7, 16.3, None, None, 17.4, 14.5]
proteins["HRS 3530"]=[14.7, 15.2, 12.7, 14.7, 37.5, 14.4, 15.0, 12.7, 15.0, 14.0, 13.4, 14.4, 17.7, 13.9, 15.7, 15.7, 13.9, 18.9, 15.1]
proteins["HRS 3616"]=[15.6, 16.0, 14.0, 15.8, 35.7, 15.1, 15.7, 14.3, 15.4, 14.6, 15.1, 15.0, 17.3, 13.9, 16.5, None, None, 18.3, None]
proteins["Lang-MN"]=[15.6, 16.0, 13.5, 15.5, 39.3, 14.7, 15.1, 14.7, 15.4, 14.6, 15.0, 14.9, 17.6, 13.5, 16.2, 15.3, 14.6, 19.9, None]
proteins["LCS Anchor"]=[15.7, 15.6, 14.0, None, None, 14.9, 14.9, 13.7, None, None, None, None, 16.8, 13.4, 15.9, None, None, 17.9, 15.7]
proteins["LCS Breakaway"]=[16.7, 15.1, 13.8, 14.9, 30.6, 14.6, 14.9, 13.2, 15.2, 13.8, 13.9, 13.8, 17.2, 13.0, 16.8, None, None, 17.8, None]
proteins["LCS Nitro"]=[13.4, 13.6, None, None, None, 13.1, 13.1, 11.2, None, None, None, None, 16.3, 13.1, 14.6, 14.3, 13.3, 17.7, 15.3]
proteins["LCS Prime"]=[13.3, 13.9, None, None, None, 13.5, 13.6, 11.8, 13.2, 12.6, 12.5, 12.6, 15.1, 13.3, 14.7, 13.6, 12.7, 16.6, 15.2]
proteins["LCS Rebel"]=[14.9, 15.9, 12.9, 14.7, 39.2, 14.8, 14.4, 13.2, 14.0, 13.8, 13.7, 14.1, 17.6, 14.4, 16.3, None, None, 18.9, 15.0]
proteins["LCS Trigger"]=[13.3, 13.2, 11.7, 12.1, 41.2, 12.9, 12.9, 11.0, None, None, None, None, 16.4, 12.1, 14.2, None, None, 21.0, 15.6]
proteins["Linkert"]=[16.0, 15.4, 14.7, 15.3, 36.6, 14.9, 15.2, 14.7, 15.5, 14.3, 14.7, 14.7, 18.0, 13.9, 16.4, 15.5, 14.5, 18.4, 15.3]
proteins["Mott"]=[15.5, None, None, None, 37.4, 14.9, 14.3, None, None, None, None, None, 17.2, 14.0, 16.2, None, None, 19.7, 14.7]
proteins["MS Camaro"]=[15.6, 15.6, None, None, None, 14.9, 14.7, 13.6, 14.7, 13.6, 12.7, 14.3, 17.3, 13.9, 16.1, None, None, 17.4, 15.0]
proteins["MS Chevelle"]=[14.5, 14.7, None, None, None, 13.7, 13.8, 12.2, 13.5, 12.5, 12.9, 12.7, 16.3, 13.1, 15.2, None, None, 17.0, 14.4]
proteins["ND901CL Plus"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.7, None, None, None, None]
proteins["ND VitPro"]=[15.3, 15.8, 14.0, 15.6, 35.1, 15.6, 15.5, 14.2, 15.0, 14.4, 14.9, 14.5, 17.5, 14.8, 16.6, 15.5, 15.0, 18.0, 15.0]
proteins["Prestige"]=[14.7, None, None, None, None, None, None, None, None, None, None, None, None, 13.8, None, None, None, 18.3, 14.5]
proteins["Prevail"]=[14.0, 14.0, 13.5, 14.5, 37.7, 13.5, 14.4, 13.5, None, None, None, None, 16.2, 12.6, 15.6, None, None, 17.4, 15.3]
proteins["Prosper"]=[13.6, 14.7, 12.4, 13.6, 35.0, 14.0, 13.6, 11.9, 14.3, 13.3, 12.7, 13.1, 15.9, 12.8, 15.6, 15.9, 13.7, 18.1, 15.3]
proteins["Prosper/ND VitPro"]=[14.8, 15.2, 13.0, 14.6, 36.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
proteins["Redstone"]=[14.0, None, None, None, None, None, None, None, None, None, None, None, None, 13.3, 14.8, 15.6, 13.8, 21.4, 15.6]
proteins["Rollag"]=[15.8, 15.6, 14.5, 15.3, 36.7, 15.3, 15.0, 14.4, 15.7, 14.3, 14.4, 14.6, 17.4, 13.3, 15.8, None, None, 18.3, 15.2]
proteins["Shelly"]=[14.5, 14.8, 12.9, 13.6, 42.3, 13.7, 14.0, 13.0, 14.3, 13.2, 13.4, 13.3, 16.5, 13.0, 15.2, 15.5, 13.1, 18.4, None]
proteins["Shelly/Bolles"]=[15.2, 16.1, None, 15.5, 32.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
proteins["Surpass"]=[15.1, 15.1, 13.1, 14.7, 34.1, 14.3, 14.0, 12.9, 13.9, 13.6, 14.5, 13.4, 16.0, 13.1, 15.6, 14.6, 12.7, 17.0, 15.6]
proteins["SY Ingmar"]=[15.5, 15.2, 13.9, 15.2, 42.0, 14.8, 15.1, 14.1, 15.4, 14.1, 14.6, 14.1, 17.3, 14.4, 16.3, 15.3, 14.0, 18.8, 15.3]
proteins["SY Rockford"]=[None, None, None, None, None, None, None, None, None, None, None, None, 16.9, 13.6, 15.8, None, None, 18.2, 15.1]
proteins["SY-Rowyn"]=[14.1, 14.4, None, None, None, 13.7, 13.9, 12.3, 15.0, 12.9, 13.6, 13.2, 17.4, 13.7, 16.0, 15.4, 13.4, 18.2, None]
proteins["SY-Rustler"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, 13.6, None, None, None, None, None]
proteins["SY-Soren"]=[15.7, 15.7, 14.1, 14.8, 42.9, 14.7, 14.9, 13.6, 15.5, 13.7, 14.5, 14.0, 17.5, 14.1, 16.1, 15.8, 13.9, 18.5, 15.6]
proteins["SY-Valda"]=[14.7, 14.3, 12.7, 13.7, 45.6, 13.7, 13.9, 12.8, 14.7, 13.3, 13.5, 13.1, 16.8, 13.8, 15.8, 15.4, 13.1, 18.6, 15.9]
proteins["TCG-Climax"]=[16.3, 16.3, 14.9, None, None, 16.0, 16.1, 15.1, None, None, None, None, 18.2, 14.8, 16.6, None, None, 20.7, 15.3]
proteins["TCG-Cornerstone"]=[14.9, 14.8, None, None, None, 15.0, 15.1, 13.6, None, None, None, None, 17.0, 14.3, 15.8, None, None, 18.6, 15.3]
proteins["TCG-Spitfire"]=[14.3, 14.5, None, None, None, 14.3, 14.0, 13.2, None, None, None, None, 17.5, 13.7, 14.7, None, None, 18.0, 14.7]
proteins["Velva"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 18.2, 15.5]
proteins["WB9479"]=[15.8, 15.9, 13.5, 15.7, 35.8, 15.9, 15.0, 13.9, 15.7, 14.4, 14.4, 14.8, 17.4, 15.0, 16.2, None, None, 18.0, None]
proteins["WB9590"]=[15.0, 15.7, 13.4, 15.3, 36.5, 14.8, 15.1, 13.3, 15.9, 13.8, 13.9, 14.2, 17.4, 14.6, 16.0, None, None, 17.7, None]
proteins["WB9653"]=[14.3, 14.1, None, None, None, 14.2, 14.3, 12.6, None, None, None, None, 17.1, 14.4, 16.1, 14.8, 13.7, 17.6, None]
proteins["WB9719"]=[14.5, 15.0, 12.6, 14.6, 46.8, 15.0, 14.7, 13.1, None, None, None, None, 16.4, 13.5, 15.3, None, None, 18.2, None]
proteins["WB-Mayville"]=[14.9, 15.4, 13.7, 15.3, 37.9, 15.5, 15.2, 13.9, 15.3, 13.8, 14.4, 14.6, 16.5, 14.2, 15.7, None, None, 17.4, 15.1]
proteins["WB-Mayville (1.8 M PLS)"]=[15.4, 15.2, None, 15.4, 36.6, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

# insure consistency in sizing of arrays
for dic in (yields, weights, proteins):
	assert(len(dic.keys()) == len(varieties))
	for key in dic:
		assert(len(dic[key]) == len(locations))
	
planted = models.Date.objects.filter(date__year=2017, date__month=5)[0]
harvested = models.Date.objects.filter(date__year=2017, date__month=8)[0]

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
