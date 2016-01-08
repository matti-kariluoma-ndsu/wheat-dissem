#$ python manage.py shell
#from variety_trials_data import models

## source "15 Location Means for WHIP.xlsx" sent Jan/7/2016, 11:20 CST

locations = [
		"Saint Paul",
		"Waseca",
		"Lamberton",
		"Morris",
		"Crookston",
		"Roseau",
		"Fergus Falls",
		"Perley",
		"Oklee",
		"Stephen",
		"Strathcona",
		"Hallock",
		"Benson",
		"Le Center",
		"Kimball",
	]

fail = False
for lname in locations:
	try:
		location = models.Location.objects.filter(name=lname)[0]
	except:
		fail = True
		print 'Missing Location record: ', lname

varieties = [
		"Barlow",
		"Bolles",
		"Boost",
		"Chevelle",
		"Elgin-ND",
		"Faller",
		"Focus",
		"Forefront",
		"Glenn",
		"HRS 3361",
		"HRS 3419",
		"HRS 3504",
		"HRS 3530",
		"Knudson",
		"LCS Albany",
		"LCS Breakaway",
		"LCS Iguacu",
		"LCS Nitro",
		"LCS Prime",
		"Linkert",
		"Marshall",
		"MS Stingray",
		"Norden",
		"Prevail",
		"Prosper",
		"RB07",
		"Rollag",
		"Samson",
		"Surpass",
		"SY Ingmar",
		"SY Rowyn",
		"SY Soren",
		"SY Valda",
		"WB9507",
		"WB9653",
		"WB-Mayville",
	]

rename_varieties = {}
rename_varieties["Elgin-ND"] = "Elgin"

for vname in varieties:
	try:
		variety = models.Variety.objects.filter(name=vname)[0]
	except:
		fail = True
		print 'Missing Variety record: ', vname
		#models.Variety.objects.filter(name__contains=vname)
		
if fail:
	print "ERROR: Missing records. See preceding output. Exiting..."
	import sys
	sys.exit(1)

# location name, yield lsd10, yield lsd5
yield_lsds = [
	]
# None given!

# regexps to help transform tab-delimited copy+paste from source workbook
# s/\t/, /
# s/$/]/
# s/^/yields["/
# s/^([^,]+), /\1"]=[/
yields_proteins = {}
saintpaul = yields_proteins["Saint Paul"] = {}
saintpaul["Barlow"]=[82.3, 14.6] # [yield, protein]
saintpaul["Bolles"]=[91.5, 14.5]
saintpaul["Boost"]=[83.6, 15.3]
saintpaul["Chevelle"]=[91.0, 12.4]
saintpaul["Elgin-ND"]=[88.0, 14.0]
saintpaul["Faller"]=[86.5, 13.6]
saintpaul["Focus"]=[84.1, 14.4]
saintpaul["Forefront"]=[76.2, 14.8]
saintpaul["Glenn"]=[66.4, 14.9]
saintpaul["HRS 3361"]=[87.8, 13.4]
saintpaul["HRS 3419"]=[102.8, 13.5]
saintpaul["HRS 3504"]=[90.0, 13.3]
saintpaul["HRS 3530"]=[92.6, 13.6]
saintpaul["Knudson"]=[89.7, 13.5]
saintpaul["LCS Albany"]=[102.2, 13.1]
saintpaul["LCS Breakaway"]=[87.9, 14.0]
saintpaul["LCS Iguacu"]=[104.4, 13.4]
saintpaul["LCS Nitro"]=[106.3, 13.3]
saintpaul["LCS Prime"]=[75.0, 12.8]
saintpaul["Linkert"]=[90.0, 14.5]
saintpaul["Marshall"]=[66.1, 13.7]
saintpaul["MS Stingray"]=[107.8, 11.6]
saintpaul["Norden"]=[89.4, 14.6]
saintpaul["Prevail"]=[92.7, 13.6]
saintpaul["Prosper"]=[86.9, 13.0]
saintpaul["RB07"]=[87.4, 13.7]
saintpaul["Rollag"]=[81.7, 14.2]
saintpaul["Samson"]=[100.7, 13.6]
saintpaul["Surpass"]=[68.6, 14.1]
saintpaul["SY Ingmar"]=[79.5, 14.6]
saintpaul["SY Rowyn"]=[88.9, 13.5]
saintpaul["SY Soren"]=[87.9, 14.2]
saintpaul["SY Valda"]=[94.4, 13.4]
saintpaul["WB9507"]=[101.5, 13.4]
saintpaul["WB9653"]=[95.9, 13.0]
saintpaul["WB-Mayville"]=[94.1, 14.5]


waseca = yields_proteins["Waseca"] = {}
waseca["Barlow"]=[44.7, 16.0]
waseca["Bolles"]=[47.9, 17.0]
waseca["Boost"]=[54.7, 14.9]
waseca["Chevelle"]=[44.4, 13.7]
waseca["Elgin-ND"]=[38.8, 15.7]
waseca["Faller"]=[52.0, 14.0]
waseca["Focus"]=[45.9, 15.7]
waseca["Forefront"]=[48.8, 15.2]
waseca["Glenn"]=[49.1, 15.4]
waseca["HRS 3361"]=[55.4, 13.9]
waseca["HRS 3419"]=[55.8, 13.3]
waseca["HRS 3504"]=[48.3, 14.9]
waseca["HRS 3530"]=[67.2, 14.8]
waseca["Knudson"]=[39.2, 14.2]
waseca["LCS Albany"]=[53.3, 14.1]
waseca["LCS Breakaway"]=[47.8, 15.3]
waseca["LCS Iguacu"]=[36.9, 15.0]
waseca["LCS Nitro"]=[47.0, 13.7]
waseca["LCS Prime"]=[37.0, 13.7]
waseca["Linkert"]=[49.1, 15.3]
waseca["Marshall"]=[18.9, 14.8]
waseca["MS Stingray"]=[42.1, 12.2]
waseca["Norden"]=[49.2, 14.7]
waseca["Prevail"]=[58.3, 14.5]
waseca["Prosper"]=[50.5, 14.4]
waseca["RB07"]=[49.8, 15.8]
waseca["Rollag"]=[41.8, 15.2]
waseca["Samson"]=[50.1, 14.3]
waseca["Surpass"]=[49.0, 15.4]
waseca["SY Ingmar"]=[38.0, 15.2]
waseca["SY Rowyn"]=[48.4, 14.2]
waseca["SY Soren"]=[37.1, 15.6]
waseca["SY Valda"]=[46.7, 14.2]
waseca["WB9507"]=[41.4, 13.8]
waseca["WB9653"]=[53.2, 14.0]
waseca["WB-Mayville"]=[52.6, 14.8]


lambert = yields_proteins["Lamberton"] = {}
lambert["Barlow"]=[91.5, 15.4]
lambert["Bolles"]=[87.3, 16.3]
lambert["Boost"]=[87.1, 14.5]
lambert["Chevelle"]=[99.0, 13.8]
lambert["Elgin-ND"]=[91.2, 15.1]
lambert["Faller"]=[104.8, 13.3]
lambert["Focus"]=[103.8, 15.2]
lambert["Forefront"]=[101.6, 14.8]
lambert["Glenn"]=[96.5, 15.4]
lambert["HRS 3361"]=[95.9, 13.8]
lambert["HRS 3419"]=[107.9, 13.3]
lambert["HRS 3504"]=[105.7, 14.4]
lambert["HRS 3530"]=[100.5, 15.1]
lambert["Knudson"]=[96.1, 13.6]
lambert["LCS Albany"]=[98.3, 13.4]
lambert["LCS Breakaway"]=[87.9, 15.1]
lambert["LCS Iguacu"]=[96.9, 12.8]
lambert["LCS Nitro"]=[100.1, 13.7]
lambert["LCS Prime"]=[103.6, 13.2]
lambert["Linkert"]=[87.4, 15.1]
lambert["Marshall"]=[70.4, 13.5]
lambert["MS Stingray"]=[84.3, 12.3]
lambert["Norden"]=[94.2, 13.9]
lambert["Prevail"]=[99.2, 13.7]
lambert["Prosper"]=[97.9, 13.7]
lambert["RB07"]=[93.2, 15.1]
lambert["Rollag"]=[89.2, 14.7]
lambert["Samson"]=[100.2, 13.9]
lambert["Surpass"]=[96.7, 14.9]
lambert["SY Ingmar"]=[97.4, 14.8]
lambert["SY Rowyn"]=[102.6, 13.9]
lambert["SY Soren"]=[88.1, 14.4]
lambert["SY Valda"]=[106.3, 14.2]
lambert["WB9507"]=[91.3, 12.7]
lambert["WB9653"]=[102.8, 14.4]
lambert["WB-Mayville"]=[90.1, 15.2]


morris = yields_proteins["Morris"] = {}
morris["Barlow"]=[64.4, 14.8]
morris["Bolles"]=[63.4, 15.5]
morris["Boost"]=[59.5, 15.2]
morris["Chevelle"]=[71.1, 13.4]
morris["Elgin-ND"]=[65.6, 13.6]
morris["Faller"]=[62.5, 13.3]
morris["Focus"]=[60.5, 14.8]
morris["Forefront"]=[68.7, 15.6]
morris["Glenn"]=[56.7, 14.8]
morris["HRS 3361"]=[67.9, 13.8]
morris["HRS 3419"]=[74.2, 13.3]
morris["HRS 3504"]=[75.3, 12.9]
morris["HRS 3530"]=[56.8, 13.6]
morris["Knudson"]=[64.9, 13.3]
morris["LCS Albany"]=[65.7, 12.8]
morris["LCS Breakaway"]=[55.4, 15.1]
morris["LCS Iguacu"]=[63.8, 12.1]
morris["LCS Nitro"]=[73.3, 13.5]
morris["LCS Prime"]=[57.8, 12.6]
morris["Linkert"]=[64.2, 15.2]
morris["Marshall"]=[62.8, 13.5]
morris["MS Stingray"]=[63.9, 11.3]
morris["Norden"]=[66.4, 14.2]
morris["Prevail"]=[65.5, 13.7]
morris["Prosper"]=[58.1, 13.0]
morris["RB07"]=[61.8, 14.8]
morris["Rollag"]=[67.7, 15.7]
morris["Samson"]=[68.7, 13.1]
morris["Surpass"]=[64.1, 14.3]
morris["SY Ingmar"]=[60.8, 15.0]
morris["SY Rowyn"]=[72.9, 13.5]
morris["SY Soren"]=[53.9, 14.8]
morris["SY Valda"]=[72.6, 12.8]
morris["WB9507"]=[55.7, 12.0]
morris["WB9653"]=[79.7, 13.5]
morris["WB-Mayville"]=[74.1, 14.6]


crook = yields_proteins["Crookston"] = {}
crook["Barlow"]=[77.6, 15.0]
crook["Bolles"]=[76.8, 16.1]
crook["Boost"]=[70.1, 14.8]
crook["Chevelle"]=[84.3, 13.0]
crook["Elgin-ND"]=[82.3, 14.9]
crook["Faller"]=[76.5, 13.5]
crook["Focus"]=[83.0, 14.5]
crook["Forefront"]=[84.4, 14.3]
crook["Glenn"]=[73.7, 15.2]
crook["HRS 3361"]=[82.1, 13.4]
crook["HRS 3419"]=[94.4, 12.6]
crook["HRS 3504"]=[83.6, 13.7]
crook["HRS 3530"]=[88.8, 14.1]
crook["Knudson"]=[78.8, 13.4]
crook["LCS Albany"]=[84.8, 12.6]
crook["LCS Breakaway"]=[85.7, 14.6]
crook["LCS Iguacu"]=[83.5, 12.3]
crook["LCS Nitro"]=[86.1, 12.2]
crook["LCS Prime"]=[71.4, 12.7]
crook["Linkert"]=[88.8, 15.5]
crook["Marshall"]=[72.7, 12.8]
crook["MS Stingray"]=[84.7, 11.4]
crook["Norden"]=[81.0, 13.7]
crook["Prevail"]=[84.4, 13.8]
crook["Prosper"]=[82.1, 13.5]
crook["RB07"]=[82.5, 14.2]
crook["Rollag"]=[89.1, 15.0]
crook["Samson"]=[90.9, 13.7]
crook["Surpass"]=[84.9, 14.2]
crook["SY Ingmar"]=[78.0, 14.9]
crook["SY Rowyn"]=[83.8, 13.4]
crook["SY Soren"]=[85.6, 14.6]
crook["SY Valda"]=[88.1, 13.9]
crook["WB9507"]=[77.4, 13.5]
crook["WB9653"]=[79.7, 13.7]
crook["WB-Mayville"]=[80.1, 14.5]


roseau = yields_proteins["Roseau"] = {}
roseau["Barlow"]=[82.8, 15.1]
roseau["Bolles"]=[85.2, 17.1]
roseau["Boost"]=[86.1, 14.9]
roseau["Chevelle"]=[70.8, 13.5]
roseau["Elgin-ND"]=[70.0, 15.1]
roseau["Faller"]=[88.3, 14.6]
roseau["Focus"]=[92.2, 15.2]
roseau["Forefront"]=[79.7, 14.7]
roseau["Glenn"]=[90.0, 15.3]
roseau["HRS 3361"]=[77.6, 14.2]
roseau["HRS 3419"]=[94.9, 14.0]
roseau["HRS 3504"]=[79.6, 14.3]
roseau["HRS 3530"]=[86.2, 15.0]
roseau["Knudson"]=[74.6, 13.9]
roseau["LCS Albany"]=[87.1, 13.4]
roseau["LCS Breakaway"]=[86.7, 15.1]
roseau["LCS Iguacu"]=[94.1, 13.0]
roseau["LCS Nitro"]=[83.2, 13.2]
roseau["LCS Prime"]=[92.3, 13.5]
roseau["Linkert"]=[84.6, 15.2]
roseau["Marshall"]=[60.3, 13.4]
roseau["MS Stingray"]=[111.1, 13.1]
roseau["Norden"]=[96.1, 14.5]
roseau["Prevail"]=[91.0, 14.6]
roseau["Prosper"]=[88.5, 14.7]
roseau["RB07"]=[77.3, 14.9]
roseau["Rollag"]=[73.2, 15.8]
roseau["Samson"]=[87.8, 14.4]
roseau["Surpass"]=[89.6, 15.3]
roseau["SY Ingmar"]=[86.2, 15.3]
roseau["SY Rowyn"]=[76.4, 14.1]
roseau["SY Soren"]=[93.3, 15.4]
roseau["SY Valda"]=[83.0, 14.7]
roseau["WB9507"]=[78.1, 15.3]
roseau["WB9653"]=[80.3, 14.1]
roseau["WB-Mayville"]=[80.7, 14.8]


fergus = yields_proteins["Fergus Falls"] = {}
fergus["Barlow"]=[104.5, 14.4]
fergus["Bolles"]=[106.8, 15.1]
fergus["Boost"]=[99.5, 15.4]
fergus["Chevelle"]=[108.2, 13.7]
fergus["Elgin-ND"]=[107.2, 15.2]
fergus["Faller"]=[124.3, 13.4]
fergus["Focus"]=[101.4, 14.9]
fergus["Forefront"]=[101.0, 14.4]
fergus["Glenn"]=[101.1, 15.1]
fergus["HRS 3361"]=[113.8, 14.2]
fergus["HRS 3419"]=[115.6, 13.6]
fergus["HRS 3504"]=[114.6, 13.9]
fergus["HRS 3530"]=[120.7, 14.9]
fergus["Knudson"]=[108.5, 13.4]
fergus["LCS Albany"]=[120.4, 14.1]
fergus["LCS Breakaway"]=[110.1, 14.2]
fergus["LCS Iguacu"]=[102.2, 13.8]
fergus["LCS Nitro"]=[113.0, 13.6]
fergus["LCS Prime"]=[128.0, 14.3]
fergus["Linkert"]=[102.8, 14.9]
fergus["Marshall"]=[100.0, 13.9]
fergus["MS Stingray"]=[119.5, 13.0]
fergus["Norden"]=[108.2, 14.1]
fergus["Prevail"]=[108.8, 14.0]
fergus["Prosper"]=[119.1, 14.0]
fergus["RB07"]=[104.8, 13.9]
fergus["Rollag"]=[109.1, 14.7]
fergus["Samson"]=[108.4, 14.0]
fergus["Surpass"]=[111.3, 14.6]
fergus["SY Ingmar"]=[108.0, 14.6]
fergus["SY Rowyn"]=[116.4, 14.0]
fergus["SY Soren"]=[98.1, 14.2]
fergus["SY Valda"]=[119.0, 14.6]
fergus["WB9507"]=[120.8, 14.4]
fergus["WB9653"]=[118.8, 14.1]
fergus["WB-Mayville"]=[105.2, 15.2]

# missing Boost, LCS Prime, Surpass
perley = yields_proteins["Perley"] = {}
perley["Barlow"]=[100.8, None]
perley["Bolles"]=[103.1, None]
perley["Chevelle"]=[104.7, None]
perley["Elgin-ND"]=[96.3, None]
perley["Faller"]=[111.0, None]
perley["Focus"]=[105.8, None]
perley["Forefront"]=[112.7, None]
perley["Glenn"]=[99.4, None]
perley["HRS 3361"]=[104.6, None]
perley["HRS 3419"]=[114.3, None]
perley["HRS 3504"]=[108.3, None]
perley["HRS 3530"]=[123.5, None]
perley["Knudson"]=[101.9, None]
perley["LCS Albany"]=[114.5, None]
perley["LCS Breakaway"]=[116.5, None]
perley["LCS Iguacu"]=[120.6, None]
perley["LCS Nitro"]=[107.3, None]
perley["Linkert"]=[103.8, None]
perley["Marshall"]=[92.5, None]
perley["MS Stingray"]=[125.1, None]
perley["Norden"]=[104.3, None]
perley["Prevail"]=[112.2, None]
perley["Prosper"]=[113.4, None]
perley["RB07"]=[103.0, None]
perley["Rollag"]=[111.8, None]
perley["Samson"]=[120.2, None]
perley["SY Ingmar"]=[109.2, None]
perley["SY Rowyn"]=[105.5, None]
perley["SY Soren"]=[103.5, None]
perley["SY Valda"]=[119.9, None]
perley["WB-Mayville"]=[104.3, None]
perley["WB9507"]=[115.7, None]
perley["WB9653"]=[100.4, None]


oklee = yields_proteins["Oklee"] = {}
oklee["Barlow"]=[103.4, 14.4]
oklee["Bolles"]=[99.8, 14.8]
oklee["Boost"]=[100.4, 14.4]
oklee["Chevelle"]=[113.9, 14.8]
oklee["Elgin-ND"]=[98.0, 14.3]
oklee["Faller"]=[100.1, 13.3]
oklee["Focus"]=[112.7, 14.2]
oklee["Forefront"]=[104.2, 14.5]
oklee["Glenn"]=[106.7, 15.1]
oklee["HRS 3361"]=[106.9, 14.4]
oklee["HRS 3419"]=[102.4, 14.9]
oklee["HRS 3504"]=[102.7, 14.7]
oklee["HRS 3530"]=[106.4, 12.8]
oklee["Knudson"]=[105.0, 13.5]
oklee["LCS Albany"]=[106.0, 14.1]
oklee["LCS Breakaway"]=[102.5, 14.6]
oklee["LCS Iguacu"]=[103.4, 14.5]
oklee["LCS Nitro"]=[105.5, 14.0]
oklee["LCS Prime"]=[105.5, 14.0]
oklee["Linkert"]=[106.4, 13.9]
oklee["Marshall"]=[106.6, 13.9]
oklee["MS Stingray"]=[102.2, 13.8]
oklee["Norden"]=[102.5, 14.1]
oklee["Prevail"]=[111.0, 14.3]
oklee["Prosper"]=[108.8, 13.5]
oklee["RB07"]=[109.3, 13.9]
oklee["Rollag"]=[112.0, 14.2]
oklee["Samson"]=[106.9, 14.4]
oklee["Surpass"]=[108.1, 14.0]
oklee["SY Ingmar"]=[103.2, 14.9]
oklee["SY Rowyn"]=[98.2, 14.3]
oklee["SY Soren"]=[104.3, 13.4]
oklee["SY Valda"]=[100.8, 13.6]
oklee["WB9507"]=[94.8, 12.5]
oklee["WB9653"]=[102.8, 14.2]
oklee["WB-Mayville"]=[100.5, 13.0]


stephen = yields_proteins["Stephen"] = {}
stephen["Barlow"]=[82.8, 15.1]
stephen["Bolles"]=[80.2, 17.1]
stephen["Boost"]=[79.5, 14.9]
stephen["Chevelle"]=[86.7, 13.5]
stephen["Elgin-ND"]=[75.9, 15.1]
stephen["Faller"]=[89.9, 14.6]
stephen["Focus"]=[83.0, 15.2]
stephen["Forefront"]=[77.8, 14.7]
stephen["Glenn"]=[84.2, 15.3]
stephen["HRS 3361"]=[78.1, 14.2]
stephen["HRS 3419"]=[96.5, 14.0]
stephen["HRS 3504"]=[92.9, 14.3]
stephen["HRS 3530"]=[96.2, 15.0]
stephen["Knudson"]=[82.5, 13.9]
stephen["LCS Albany"]=[87.4, 13.4]
stephen["LCS Breakaway"]=[88.9, 15.1]
stephen["LCS Iguacu"]=[94.8, 13.0]
stephen["LCS Nitro"]=[85.7, 13.2]
stephen["LCS Prime"]=[91.8, 13.5]
stephen["Linkert"]=[89.5, 15.2]
stephen["Marshall"]=[80.8, 13.4]
stephen["MS Stingray"]=[92.7, 13.1]
stephen["Norden"]=[82.5, 14.5]
stephen["Prevail"]=[83.2, 14.6]
stephen["Prosper"]=[89.6, 14.7]
stephen["RB07"]=[82.4, 14.8]
stephen["Rollag"]=[74.9, 15.8]
stephen["Samson"]=[86.8, 14.3]
stephen["Surpass"]=[97.6, 15.3]
stephen["SY Ingmar"]=[88.5, 15.3]
stephen["SY Rowyn"]=[86.9, 14.1]
stephen["SY Soren"]=[84.9, 15.4]
stephen["SY Valda"]=[94.2, 14.7]
stephen["WB9507"]=[83.5, 15.3]
stephen["WB9653"]=[97.5, 14.1]
stephen["WB-Mayville"]=[80.0, 14.8]

# missing Boost, LCS Prime, Surpass
strath = yields_proteins["Strathcona"] = {}
strath["Barlow"]=[64.0, None]
strath["Bolles"]=[69.7, None]
strath["Chevelle"]=[60.5, None]
strath["Elgin-ND"]=[61.8, None]
strath["Faller"]=[65.6, None]
strath["Focus"]=[65.7, None]
strath["Forefront"]=[66.5, None]
strath["Glenn"]=[65.4, None]
strath["HRS 3361"]=[68.1, None]
strath["HRS 3419"]=[71.4, None]
strath["HRS 3504"]=[63.7, None]
strath["HRS 3530"]=[73.7, None]
strath["Knudson"]=[70.3, None]
strath["LCS Albany"]=[65.2, None]
strath["LCS Breakaway"]=[68.0, None]
strath["LCS Iguacu"]=[67.1, None]
strath["LCS Nitro"]=[73.9, None]
strath["Linkert"]=[69.3, None]
strath["Marshall"]=[56.3, None]
strath["MS Stingray"]=[81.3, None]
strath["Norden"]=[54.2, None]
strath["Prevail"]=[64.2, None]
strath["Prosper"]=[68.8, None]
strath["RB07"]=[62.7, None]
strath["Rollag"]=[64.5, None]
strath["Samson"]=[79.7, None]
strath["SY Ingmar"]=[64.5, None]
strath["SY Rowyn"]=[71.3, None]
strath["SY Soren"]=[68.0, None]
strath["SY Valda"]=[67.9, None]
strath["WB-Mayville"]=[57.4, None]
strath["WB9507"]=[71.1, None]
strath["WB9653"]=[68.5, None]


hallock = yields_proteins["Hallock"] = {}
hallock["Barlow"]=[87.6, 14.7]
hallock["Bolles"]=[85.9, 16.6]
hallock["Boost"]=[90.1, 14.6]
hallock["Chevelle"]=[85.8, 13.1]
hallock["Elgin-ND"]=[77.9, 15.5]
hallock["Faller"]=[100.1, 13.9]
hallock["Focus"]=[86.0, 15.3]
hallock["Forefront"]=[92.7, 14.8]
hallock["Glenn"]=[81.3, 15.1]
hallock["HRS 3361"]=[87.0, 14.4]
hallock["HRS 3419"]=[104.7, 13.7]
hallock["HRS 3504"]=[88.3, 14.2]
hallock["HRS 3530"]=[104.0, 15.2]
hallock["Knudson"]=[88.9, 13.6]
hallock["LCS Albany"]=[98.7, 13.0]
hallock["LCS Breakaway"]=[82.8, 14.2]
hallock["LCS Iguacu"]=[93.2, 12.9]
hallock["LCS Nitro"]=[90.4, 12.5]
hallock["LCS Prime"]=[97.7, 13.5]
hallock["Linkert"]=[91.7, 15.3]
hallock["Marshall"]=[84.0, 13.8]
hallock["MS Stingray"]=[109.4, 12.3]
hallock["Norden"]=[87.9, 14.0]
hallock["Prevail"]=[92.8, 14.2]
hallock["Prosper"]=[99.0, 14.2]
hallock["RB07"]=[84.8, 14.2]
hallock["Rollag"]=[92.2, 15.4]
hallock["Samson"]=[98.7, 14.3]
hallock["Surpass"]=[88.8, 15.0]
hallock["SY Ingmar"]=[89.8, 15.3]
hallock["SY Rowyn"]=[94.3, 14.2]
hallock["SY Soren"]=[83.2, 14.9]
hallock["SY Valda"]=[107.3, 14.2]
hallock["WB9507"]=[100.2, 14.5]
hallock["WB9653"]=[78.7, 13.5]
hallock["WB-Mayville"]=[89.0, 14.9]


benson = yields_proteins["Benson"] = {}
benson["Barlow"]=[96.8, 14.3]
benson["Bolles"]=[103.7, 15.4]
benson["Boost"]=[98.8, 14.8]
benson["Chevelle"]=[119.7, 12.6]
benson["Elgin-ND"]=[107.3, 14.4]
benson["Faller"]=[107.5, 13.4]
benson["Focus"]=[98.5, 14.9]
benson["Forefront"]=[97.1, 13.6]
benson["Glenn"]=[89.4, 14.9]
benson["HRS 3361"]=[90.6, 14.7]
benson["HRS 3419"]=[102.0, 12.2]
benson["HRS 3504"]=[110.8, 13.8]
benson["HRS 3530"]=[118.3, 15.0]
benson["Knudson"]=[102.2, 14.1]
benson["LCS Albany"]=[115.9, 12.9]
benson["LCS Breakaway"]=[100.8, 14.8]
benson["LCS Iguacu"]=[104.0, 13.2]
benson["LCS Nitro"]=[110.0, 13.2]
benson["LCS Prime"]=[113.0, 13.3]
benson["Linkert"]=[95.2, 15.3]
benson["Marshall"]=[103.8, 13.4]
benson["MS Stingray"]=[105.5, 12.0]
benson["Norden"]=[97.8, 13.9]
benson["Prevail"]=[95.4, 14.7]
benson["Prosper"]=[119.0, 13.8]
benson["RB07"]=[104.1, 14.6]
benson["Rollag"]=[103.4, 15.3]
benson["Samson"]=[98.3, 13.8]
benson["Surpass"]=[107.2, 14.1]
benson["SY Ingmar"]=[105.9, 14.8]
benson["SY Rowyn"]=[104.7, 13.4]
benson["SY Soren"]=[97.0, 15.0]
benson["SY Valda"]=[113.2, 13.5]
benson["WB9507"]=[113.1, 14.6]
benson["WB9653"]=[115.1, 12.7]
benson["WB-Mayville"]=[94.5, 15.3]


center = yields_proteins["Le Center"] = {}
center["Barlow"]=[86.2, 14.7]
center["Bolles"]=[75.7, 17.0]
center["Boost"]=[78.9, 14.9]
center["Chevelle"]=[90.1, 13.1]
center["Elgin-ND"]=[80.2, 14.5]
center["Faller"]=[91.8, 13.6]
center["Focus"]=[80.7, 15.4]
center["Forefront"]=[93.0, 14.2]
center["Glenn"]=[72.2, 15.0]
center["HRS 3361"]=[91.1, 13.7]
center["HRS 3419"]=[102.9, 13.1]
center["HRS 3504"]=[95.6, 13.6]
center["HRS 3530"]=[93.5, 13.9]
center["Knudson"]=[88.0, 13.2]
center["LCS Albany"]=[92.1, 13.4]
center["LCS Breakaway"]=[84.3, 14.5]
center["LCS Iguacu"]=[84.5, 12.7]
center["LCS Nitro"]=[95.0, 13.1]
center["LCS Prime"]=[88.0, 13.4]
center["Linkert"]=[90.1, 14.9]
center["Marshall"]=[60.2, 13.7]
center["MS Stingray"]=[87.3, 10.9]
center["Norden"]=[82.9, 14.2]
center["Prevail"]=[91.9, 14.2]
center["Prosper"]=[86.7, 13.7]
center["RB07"]=[76.7, 14.6]
center["Rollag"]=[78.8, 14.5]
center["Samson"]=[93.7, 13.6]
center["Surpass"]=[86.7, 15.0]
center["SY Ingmar"]=[94.8, 14.9]
center["SY Rowyn"]=[84.9, 13.6]
center["SY Soren"]=[74.6, 15.2]
center["SY Valda"]=[100.1, 13.7]
center["WB9507"]=[97.7, 13.3]
center["WB9653"]=[94.0, 13.7]
center["WB-Mayville"]=[92.4, 13.9]


kimball = yields_proteins["Kimball"] = {}
kimball["Barlow"]=[80.9, 14.5]
kimball["Bolles"]=[95.2, 15.2]
kimball["Boost"]=[94.0, 15.5]
kimball["Chevelle"]=[110.8, 13.5]
kimball["Elgin-ND"]=[87.0, 15.5]
kimball["Faller"]=[84.5, 14.0]
kimball["Focus"]=[83.8, 15.8]
kimball["Forefront"]=[100.1, 14.1]
kimball["Glenn"]=[86.8, 15.0]
kimball["HRS 3361"]=[95.1, 13.6]
kimball["HRS 3419"]=[123.1, 12.5]
kimball["HRS 3504"]=[99.9, 14.2]
kimball["HRS 3530"]=[93.3, 14.6]
kimball["Knudson"]=[92.7, 14.3]
kimball["LCS Albany"]=[114.5, 13.6]
kimball["LCS Breakaway"]=[89.0, 15.1]
kimball["LCS Iguacu"]=[101.0, 12.6]
kimball["LCS Nitro"]=[112.2, 13.4]
kimball["LCS Prime"]=[105.4, 12.5]
kimball["Linkert"]=[93.5, 14.4]
kimball["Marshall"]=[76.1, 12.8]
kimball["MS Stingray"]=[96.4, 12.6]
kimball["Norden"]=[93.4, 14.2]
kimball["Prevail"]=[111.2, 14.3]
kimball["Prosper"]=[92.8, 13.2]
kimball["RB07"]=[98.9, 13.7]
kimball["Rollag"]=[96.4, 14.5]
kimball["Samson"]=[102.5, 13.7]
kimball["Surpass"]=[87.1, 14.4]
kimball["SY Ingmar"]=[105.6, 15.0]
kimball["SY Rowyn"]=[103.8, 14.6]
kimball["SY Soren"]=[95.4, 14.8]
kimball["SY Valda"]=[100.8, 13.5]
kimball["WB9507"]=[89.0, 12.5]
kimball["WB9653"]=[107.9, 13.6]
kimball["WB-Mayville"]=[90.9, 14.1]

