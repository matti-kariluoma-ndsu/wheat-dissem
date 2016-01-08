#$ python manage.py shell
#from variety_trials_data import models

## source "Selection tool data for ND.xlsx" sent Jan/7/2016, 11:20 CST

locations = [
		"Carrington-Dry", 
		"Carrington-Irrigated", 
		"CarringtonElite", 
		"CREC-Dazey", 
		"CREC-Wishek", 
		"Casselton", 
		"Prosper", 
		"Forman", 
		"Steele", 
		"Langdon", 
		"LREC-Cando", 
		"LREC-Cavalier", 
		"LREC-Park River", 
		"LREC-Pekin", 
		"Dickinson", 
		"Hettinger", 
		"Minot", 
		"Williston", 
		"Williston-Irr.",
	]

varieties = [
		"Advance",
		"Agawam",
		"Alpine",
		"Alsen",
		"Barlow",
		"Bolles",
		"Breaker",
		"Brennan",
		"Brick",
		"Briggs",
		"Cardale",
		"Choteau",
		"Dapps",
		"Duclair",
		"Elgin-ND",
		"Faller",
		"Focus",
		"Forefront",
		"Freyr",
		"Glenn",
		"Howard",
		"HRS 13-04",
		"HRS 3361",
		"HRS 3378",
		"HRS 3419",
		"HRS 3504",
		"HRS 3530",
		"Jenna",
		"Kelby",
		"LCS Albany",
		"LCS Breakaway",
		"LCS Iguacu",
		"LCS Nitro",
		"LCS Powerplay",
		"LCS Pro",
		"Linkert",
		"Mott",
		"MS Chevelle",
		"MS Stingray",
		"ND901CL Plus",
		"Norden",
		"Prestige",
		"Prevail",
		"Prosper",
		"RB07",
		"Redstone",
		"Reeder",
		"Rollag",
		"Sabin",
		"Samson",
		"Select",
		"Steele-ND",
		"SY Ingmar",
		"SY-Rowyn",
		"SY-Soren",
		"SY-Tyra",
		"SY-Valda",
		"SY605CL",
		"Velva",
		"Vida",
		"WB-Mayville",
		"WB-Vantage",
		"WB9507",
		"WB9653",
		"WB9879CLP+",
	]

# location name, yield lsd10, yield lsd5
yield_lsds = [
		('Carrington-Dry', 7.4, 8.9),
		('Carrington-Irrigated', 4.5, 5.4),
		('CarringtonElite', 6.3, 7.5),
		('CREC-Dazey', 5.4, 6.5),
		('CREC-Wishek', 6.8, 8.1),
		('Casselton', 6.9, None),
		('Prosper', 11.1, None),
		('Forman', None, 6.9),
		('Steele', None, 10.7),
		('Langdon', 5.0, 5.9),
		('LREC-Cando', 5.5, 6.6),
		('LREC-Cavalier', 6.0, 7.2),
		('LREC-Park River', 7.0, 8.4),
		('LREC-Pekin', 3.7, 4.4),
		('Dickinson', 5.9, 5.9),
		('Hettinger', 4.0, 4.7),
		('Minot', 6.3, 7.5),
		('Williston', 4.7, 5.6),
		('Williston-Irr.', 17.1, 20.4),
	]

# regexps to help transform tab-delimited copy+paste from source workbook
# s/\t/, /
# s/$/]/
# s/^/yields["/
# s/^([^,]+), /\1"]=[/
yields = {}
yields["Advance"]=[59.7, 56.5, 38.2, 55.8, 44.8, 60.3, 62.2, None, 54.5, 74.6, None, None, None, None, 66.8, 79.1, 80.4, 33.1, None]
yields["Agawam"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 31.2, None]
yields["Alpine"]=[54.4, 48.3, None, 59.1, None, None, None, None, None, 72.6, None, None, None, None, None, None, 65.5, 32.5, None]
yields["Alsen"]=[56.8, 55.6, None, None, None, 63.7, 59.4, None, None, None, None, None, None, None, None, None, None, 31.6, None]
yields["Barlow"]=[56.6, 50.9, 34.2, 71.2, 48.8, 63.6, 63.5, 53.6, 64.4, 73.5, 47.2, 42.8, 58.8, 63.2, 69.1, 65.2, 68.5, 26.3, 85.9]
yields["Bolles"]=[50.0, 57.5, 37.4, 68.5, 57.8, 64.1, 60.7, 52.7, 59.7, 73.0, 46.0, 43.8, 58.9, 53.8, 68.9, 70.5, 68.6, 33.5, 80.0]
yields["Breaker"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 36.6, None]
yields["Brennan"]=[62.3, 53.9, 36.5, 68.6, 50.5, 58.9, 56.1, None, None, None, None, None, None, None, None, None, 73.3, 32.6, 73.5]
yields["Brick"]=[59.8, 50.7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
yields["Briggs"]=[55.4, 55.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 32.8, 84.6]
yields["Cardale"]=[None, None, None, None, None, None, None, None, None, 61.2, 47.5, 48.1, 50.8, 60.0, None, None, None, None, None]
yields["Choteau"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 30.6, None]
yields["Dapps"]=[None, None, None, None, None, 60.4, 61.1, None, None, None, None, None, None, None, None, None, None, 29.4, None]
yields["Duclair"]=[None, None, None, None, None, 61.4, 52.2, None, None, None, None, None, None, None, 63.9, 64.5, 72.5, 32.9, None]
yields["Elgin-ND"]=[59.6, 59.6, 42.6, 70.0, 49.8, 64.3, 57.1, 55.7, 60.6, 72.9, 58.8, 43.6, 56.3, 63.4, 71.4, 74.5, 72.5, 30.8, 86.2]
yields["Faller"]=[56.2, 49.4, 36.8, 72.9, 46.3, 60.6, 49.7, None, None, 74.1, 56.2, 49.9, 61.7, 60.1, 68.1, 79.5, 82.4, 31.4, 79.5]
yields["Focus"]=[56.6, 59.5, 30.8, 79.0, 60.0, 64.1, 72.3, 53.8, 75.3, 72.5, 57.6, 49.7, 61.6, 70.0, None, 66.3, None, 33.0, None]
yields["Forefront"]=[55.6, 58.4, 29.3, 78.1, 59.5, 69.3, 70.7, 51.3, 67.1, 71.6, 49.9, 53.4, 59.8, 61.6, 52.3, 64.8, 72.9, 34.6, 66.7]
yields["Freyr"]=[58.8, 55.7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 30.7, 97.4]
yields["Glenn"]=[57.9, 51.8, 29.6, 75.0, 53.1, 58.8, 64.9, None, None, 74.8, None, None, None, None, 67.8, 63.1, 68.0, 28.4, 81.2]
yields["Howard"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 68.1, None, None, 34.3, None]
yields["HRS 13-04"]=[None, None, None, None, None, None, None, None, 56.9, None, None, None, None, None, None, None, None, None, None]
yields["HRS 3361"]=[53.3, 52.8, None, 64.6, 39.6, None, None, None, 60.9, 66.4, 49.8, 58.2, 65.9, 52.1, 64.1, 65.5, 70.6, 32.9, None]
yields["HRS 3378"]=[51.2, 47.3, None, 61.1, 42.2, None, None, None, None, 71.6, None, None, None, None, 74.6, 73.1, 69.2, 36.4, None]
yields["HRS 3419"]=[51.9, 68.1, None, 83.3, 70.1, None, None, 66.9, 65.1, 82.7, 52.9, 59.8, 67.9, 70.9, 76.6, 86.8, 82.2, 36.0, 77.1]
yields["HRS 3504"]=[None, None, None, None, None, None, None, None, None, 75.4, 62.3, 50.9, 70.2, 58.0, None, None, 74.1, None, None]
yields["HRS 3530"]=[62.9, 59.7, None, 75.5, 46.1, None, None, None, 66.1, 77.0, 57.1, 61.8, 66.7, 63.0, 72.2, 79.6, 90.2, 35.5, 98.9]
yields["Jenna"]=[53.9, 62.1, 37.7, 68.6, 65.8, None, None, None, None, None, None, None, None, None, None, None, None, 33.5, 89.8]
yields["Kelby"]=[52.5, 54.2, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 29.7, 75.1]
yields["LCS Albany"]=[63.3, 51.8, None, None, None, 58.0, 68.2, 56.8, 48.4, 68.2, None, None, None, None, None, 82.3, None, 32.2, 80.8]
yields["LCS Breakaway"]=[55.4, 53.3, None, None, None, 65.4, 62.0, 50.2, 64.4, 73.6, 48.9, 43.8, 57.3, 59.1, 7.6, 64.1, 70.2, 26.9, None]
yields["LCS Iguacu"]=[53.2, 52.4, 38.7, 70.4, 51.9, 68.0, 63.1, 56.8, 64.8, 73.3, 44.8, 62.3, 70.7, 61.8, 80.9, 72.9, 78.6, 34.0, 96.1]
yields["LCS Nitro"]=[50.5, 54.6, 35.8, 76.9, 69.5, 58.9, 60.2, 57.3, 60.9, 75.0, 52.6, 49.1, 65.2, 65.8, 85.2, 82.6, 83.3, 32.1, 94.1]
yields["LCS Powerplay"]=[63.8, 57.4, 32.9, None, None, 62.5, 62.2, 53.5, 66.2, 70.9, 55.5, 38.2, 62.0, 62.9, 73.2, 68.6, 76.5, 36.2, 94.1]
yields["LCS Pro"]=[None, None, None, None, None, 62.5, 60.0, None, None, 75.6, None, None, None, None, 77.7, 60.4, 69.1, 35.5, None]
yields["Linkert"]=[58.4, 64.0, 44.6, 59.9, 60.9, 69.0, 66.7, 54.4, 58.2, 76.1, 49.5, 52.7, 65.4, 70.0, 71.2, 63.7, 68.6, 32.9, 78.1]
yields["Mott"]=[60.0, None, None, None, 52.6, 62.1, 57.2, None, None, None, None, None, None, None, 64.1, 66.4, 78.0, 35.7, 83.6]
yields["MS Chevelle"]=[53.0, 52.6, 32.2, 76.4, 55.4, 61.4, 66.5, None, None, 80.1, None, None, None, None, 75.9, 76.1, 68.8, 35.1, None]
yields["MS Stingray"]=[61.5, 49.1, 38.7, 61.2, 43.7, 58.5, 53.4, None, None, 62.0, None, None, None, None, 68.8, 73.8, 84.9, 34.4, None]
yields["ND901CL Plus"]=[56.6, None, None, None, None, 66.8, 62.4, None, None, None, None, None, None, None, 67.1, 59.2, 74.7, 31.7, None]
yields["Norden"]=[61.9, 56.5, 39.6, 69.4, None, 70.9, 61.9, None, 59.0, 72.9, None, None, None, None, 70.5, 70.0, 73.4, 30.4, None]
yields["Prestige"]=[55.7, None, None, None, None, None, None, None, None, 77.7, None, None, None, None, 77.1, 72.6, 71.6, 32.3, None]
yields["Prevail"]=[63.0, 65.1, 36.4, 82.3, 65.8, 74.3, 72.4, 57.9, 75.8, 73.6, 55.3, 47.1, 65.3, 69.8, 53.4, 75.2, 76.5, 35.3, 83.4]
yields["Prosper"]=[56.0, 46.7, 41.1, 71.4, 41.5, 62.2, 52.1, 53.1, 64.7, 70.8, 54.9, 49.3, 52.8, 59.3, 71.1, 70.4, 78.8, 31.7, 85.3]
yields["RB07"]=[55.5, 49.9, 29.9, None, None, 65.5, 57.2, None, None, 74.3, None, None, None, None, 73.7, 70.2, 73.5, 30.6, 81.1]
yields["Redstone"]=[54.8, None, None, None, None, None, None, None, None, 79.1, None, None, None, None, 71.0, 80.2, 74.8, 29.8, None]
yields["Reeder"]=[55.5, 51.2, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 29.8, 91.0]
yields["Rollag"]=[56.7, 59.3, 35.2, 74.1, 62.6, 78.7, 65.5, 53.7, 66.8, 75.0, 54.1, 49.7, 62.4, 73.9, 75.4, 71.8, 81.8, 29.3, 81.6]
yields["Sabin"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 33.6, None]
yields["Samson"]=[53.7, None, None, 71.6, 59.9, 62.0, 54.5, None, None, 79.4, 52.9, 49.3, 71.5, 61.0, None, None, None, None, None]
yields["Select"]=[61.7, 53.9, 30.8, 79.0, 55.6, 69.2, 50.0, None, None, None, None, None, None, None, 74.5, None, None, 35.2, None]
yields["Steele-ND"]=[66.5, 55.7, None, 64.3, 49.7, 63.7, 67.2, None, None, None, None, None, None, None, 64.1, None, 67.2, 29.1, 76.5]
yields["SY Ingmar"]=[57.7, 54.5, 32.9, 68.0, 47.1, 68.5, 61.6, 56.9, 71.0, 74.2, 50.6, 56.2, 68.2, 61.9, 75.7, 67.0, 81.3, 32.3, None]
yields["SY-Rowyn"]=[65.9, 60.0, 43.6, 72.3, None, 64.2, 56.6, 53.8, 75.1, 77.6, 49.9, 53.0, 62.6, 62.6, 72.4, 74.3, 80.3, 30.6, None]
yields["SY-Soren"]=[50.4, 47.1, 37.6, 73.7, 32.8, 56.4, 55.9, 54.2, 57.8, 74.0, 45.2, 45.9, 54.7, 49.6, 70.6, 71.9, 74.1, 30.4, 87.5]
yields["SY-Tyra"]=[None, None, None, None, None, 49.0, 49.5, None, None, None, None, None, None, None, 73.1, 66.5, None, 31.9, None]
yields["SY-Valda"]=[56.5, 55.1, 32.0, 66.4, 48.9, 70.3, 66.1, 56.0, 78.4, 79.3, 55.5, 46.5, 66.4, 63.7, 78.3, 71.5, 88.3, 37.5, None]
yields["SY605CL"]=[59.4, None, None, None, None, 71.6, 74.3, None, None, None, None, None, None, None, 72.0, 71.5, 78.3, 31.8, None]
yields["Velva"]=[55.4, 42.9, 28.0, 50.5, 34.5, 50.8, 49.1, None, None, None, None, None, None, None, 67.0, None, 65.7, 34.7, 98.3]
yields["Vida"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 38.0, 86.6]
yields["WB-Mayville"]=[53.5, 45.6, 30.0, 64.0, 51.4, 59.3, 57.4, None, None, 65.9, 46.6, 44.8, 56.4, 58.6, 73.5, 60.1, 66.2, 34.2, 92.4]
yields["WB-Vantage"]=[60.9, 49.0, 35.7, None, None, 67.1, 65.2, None, None, 67.8, None, None, None, None, 62.7, None, 67.6, 26.6, 81.0]
yields["WB9507"]=[45.0, 44.4, 35.9, 65.4, 37.0, 52.3, 54.6, 45.7, 58.8, 60.8, 53.6, 44.6, 59.2, 55.5, 71.3, 65.6, 74.0, 31.0, None]
yields["WB9653"]=[68.1, None, None, 65.4, 50.1, 66.1, 67.8, None, None, 73.8, 60.9, 41.9, 69.3, 54.2, 69.5, 77.9, 73.0, 38.5, None]
yields["WB9879CLP+"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 74.0, 65.5, 62.9, 32.2, None]

weights = {}
weights["Advance"]=[62.7, 58.1, 59.4, 59.7, 59.1, 60.0, 58.2, None, 55.2, 61.9, None, None, None, None, 57.0, 62.5, 60.1, 59.2, None]
weights["Agawam"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 59.4, None]
weights["Alpine"]=[62.0, 57.4, None, 57.2, None, None, None, None, None, 61.0, None, None, None, None, None, None, 57.5, 58.3, None]
weights["Alsen"]=[62.4, 59.0, None, None, None, 61.0, 58.5, None, None, None, None, None, None, None, None, None, None, 59.7, None]
weights["Barlow"]=[62.5, 59.0, 58.3, 60.3, 58.1, 61.0, 58.7, 59.8, 51.9, 62.1, 60.8, 56.3, 59.0, 59.5, 58.4, 63.1, 57.5, 60.1, 62.3]
weights["Bolles"]=[61.3, 58.7, 58.9, 58.8, 58.5, 60.2, 58.4, 58.2, 53.6, 60.9, 59.0, 56.0, 57.3, 58.0, 55.5, 60.8, 59.1, 57.4, 61.1]
weights["Breaker"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 60.7, None]
weights["Brennan"]=[62.3, 60.0, 58.0, 60.2, 59.3, 59.4, 57.5, None, None, None, None, None, None, None, None, None, 59.5, 58.5, 61.6]
weights["Brick"]=[63.0, 61.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
weights["Briggs"]=[62.1, 59.6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 58.1, 61.6]
weights["Cardale"]=[None, None, None, None, None, None, None, None, None, 57.2, 58.5, 55.8, 55.4, 55.3, None, None, None, None, None]
weights["Choteau"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 57.9, None]
weights["Dapps"]=[None, None, None, None, None, 60.0, 57.8, None, None, None, None, None, None, None, None, None, None, 56.8, None]
weights["Duclair"]=[None, None, None, None, None, 58.4, 56.3, None, None, None, None, None, None, None, 54.1, 59.6, 56.9, 56.9, None]
weights["Elgin-ND"]=[61.2, 57.5, 58.8, 59.1, 56.7, 59.8, 57.2, 57.2, 55.1, 60.8, 60.2, 55.0, 56.4, 58.7, 55.4, 61.8, 57.5, 58.5, 61]
weights["Faller"]=[61.0, 56.8, 58.4, 59.7, 55.6, 59.2, 56.8, None, None, 60.5, 59.6, 56.0, 57.3, 57.6, 52.8, 61.6, 58.9, 57.7, 60.9]
weights["Focus"]=[62.8, 61.0, 60.4, 62.0, 60.3, 61.4, 59.5, 58.9, 56.0, 62.4, 61.8, 58.3, 59.2, 61.4, None, 62.3, None, 59.1, None]
weights["Forefront"]=[62.2, 60.2, 60.9, 61.6, 60.5, 61.2, 59.8, 63.8, 58.8, 62.7, 61.0, 57.6, 58.5, 61.8, 54.5, 61.6, 60.3, 57.9, 61.1]
weights["Freyr"]=[62.1, 59.0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 59.0, 61.4]
weights["Glenn"]=[63.3, 61.8, 59.9, 63.3, 61.5, 63.3, 60.9, None, None, 64.5, None, None, None, None, 57.3, 63.5, 58.4, 61.0, 63.3]
weights["Howard"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 55.3, None, None, 58.3, None]
weights["HRS 13-04"]=[None, None, None, None, None, None, None, None, 52.5, None, None, None, None, None, None, None, None, None, None]
weights["HRS 3361"]=[61.5, 57.9, None, 58.3, 52.7, None, None, None, 55.5, 58.6, 58.6, 56.7, 57.1, 56.4, 55.7, 60.7, 58.9, 57.3, None]
weights["HRS 3378"]=[62.3, 58.9, None, 59.3, 58.0, None, None, None, None, 61.7, None, None, None, None, 60.1, 63.1, 58.9, 58.8, None]
weights["HRS 3419"]=[60.8, 58.0, None, 59.1, 57.3, None, None, 61.7, 57.1, 60.6, 58.9, 56.0, 57.8, 57.6, 56.1, 60.9, 59.5, 56.2, None]
weights["HRS 3504"]=[None, None, None, None, None, None, None, None, None, 58.2, 59.3, 55.2, 57.1, 54.7, None, None, 57.3, None, None]
weights["HRS 3530"]=[61.6, 57.9, None, 60.2, 55.2, None, None, None, 52.8, 60.3, 60.3, 57.8, 58.3, 58.4, 53.1, 61.8, 59.1, 57.9, None]
weights["Jenna"]=[61.3, 58.1, 57.1, 58.9, 58.4, None, None, None, None, None, None, None, None, None, None, None, None, 56.8, 61.3]
weights["Kelby"]=[62.1, 59.3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 58.8, 61.4]
weights["LCS Albany"]=[60.7, 57.6, None, None, None, 58.4, 57.3, 61.5, 52.2, 60.0, None, None, None, None, None, 61.1, None, 57.2, 61.3]
weights["LCS Breakaway"]=[62.7, 60.5, None, None, None, 61.0, 59.6, 57.5, 52.1, 62.2, 61.8, 55.5, 58.0, 59.5, 59.6, 62.3, 58.4, 59.6, None]
weights["LCS Iguacu"]=[62.0, 59.0, 59.6, 60.5, 59.3, 60.5, 58.7, 62.0, 58.9, 61.9, 60.4, 59.0, 59.6, 60.2, 60.0, 61.8, 61.1, 58.2, 62.3]
weights["LCS Nitro"]=[60.4, 56.8, 56.4, 60.5, 58.2, 57.9, 56.1, 60.9, 52.8, 60.5, 58.9, 55.2, 56.7, 58.1, 56.8, 60.8, 59.8, 56.1, 61.1]
weights["LCS Powerplay"]=[62.9, 59.0, 58.2, None, None, 60.1, 57.9, 58.9, 53.2, 61.2, 61.3, 54.3, 58.9, 58.8, 58.3, 61.9, 59.4, 59.0, 61.7]
weights["LCS Pro"]=[None, None, None, None, None, 60.6, 57.9, None, None, 62.0, None, None, None, None, 59.7, 62.6, 59.1, 58.7, None]
weights["Linkert"]=[61.6, 59.8, 59.2, 59.6, 59.1, 59.5, 58.1, 59.2, 50.9, 61.1, 59.9, 56.9, 58.7, 60.2, 58.6, 61.5, 59.9, 58.1, 61.4]
weights["Mott"]=[61.8, None, None, None, 59.6, 60.7, 58.2, None, None, None, None, None, None, None, 55.9, 61.5, 59.9, 58.0, 61.3]
weights["MS Chevelle"]=[61.7, 57.0, 56.1, 60.1, 56.6, 58.2, 56.3, None, None, 60.5, None, None, None, None, 57.1, 61.4, 57.5, 58.6, None]
weights["MS Stingray"]=[59.9, 54.1, 57.4, 56.1, 54.3, 56.9, 54.7, None, None, 56.6, None, None, None, None, 51.7, 60.0, 58.0, 57.2, None]
weights["ND901CL Plus"]=[60.8, None, None, None, None, 60.2, 58.3, None, None, None, None, None, None, None, 59.2, 60.8, 58.3, 59.4, None]
weights["Norden"]=[63.1, 58.4, 58.4, 60.4, None, 62.0, 59.3, None, 45.9, 61.7, None, None, None, None, 58.9, 62.6, 59.7, 59.8, None]
weights["Prestige"]=[61.4, None, None, None, None, None, None, None, None, 61.2, None, None, None, None, 56.5, 60.1, 58.3, 57.6, None]
weights["Prevail"]=[61.9, 59.7, 58.2, 60.7, 59.4, 60.0, 57.9, 61.4, 58.6, 61.7, 59.7, 55.1, 57.5, 60.7, 55.3, 61.1, 59.5, 57.3, 60.7]
weights["Prosper"]=[61.4, 57.4, 59.0, 59.9, 55.1, 59.5, 57.2, 59.6, 45.6, 60.4, 60.4, 55.7, 56.6, 58.0, 54.7, 61.2, 58.7, 58.0, 61.3]
weights["RB07"]=[62.0, 58.6, 56.9, None, None, 59.8, 56.9, None, None, 61.5, None, None, None, None, 57.7, 60.4, 59.1, 58.2, 60.8]
weights["Redstone"]=[60.6, None, None, None, None, None, None, None, None, 61.2, None, None, None, None, 57.1, 61.0, 58.9, 57.2, None]
weights["Reeder"]=[61.5, 57.6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 58.7, 61.3]
weights["Rollag"]=[62.2, 59.2, 58.8, 61.2, 59.7, 61.5, 59.2, 58.5, 56.4, 61.5, 61.3, 57.6, 59.3, 60.9, 59.4, 62.3, 60.1, 58.7, 62.4]
weights["Sabin"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 58.2, None]
weights["Samson"]=[60.9, None, None, 58.5, 55.2, 57.5, 55.7, None, None, 60.4, 58.4, 53.8, 56.6, 56.1, None, None, None, None, None]
weights["Select"]=[63.1, 60.5, 58.2, 61.9, 58.1, 61.2, 56.9, None, None, None, None, None, None, None, 61.1, None, None, 59.6, None]
weights["Steele-ND"]=[62.9, 57.5, None, 59.2, 57.1, 60.2, 59.1, None, None, None, None, None, None, None, 59.1, None, 59.0, 58.4, 62.0]
weights["SY Ingmar"]=[62.2, 58.2, 58.8, 59.3, 57.9, 61.1, 58.2, 59.4, 56.5, 61.5, 60.9, 57.9, 60.0, 60.2, 59.2, 62.5, 58.6, 59.4, None]
weights["SY-Rowyn"]=[61.7, 58.7, 58.3, 61.0, None, 59.1, 57.2, 62.0, 57.4, 61.8, 60.3, 57.5, 58.0, 58.8, 55.9, 61.3, 60.0, 57.8, None]
weights["SY-Soren"]=[61.3, 58.3, 58.6, 60.1, 57.4, 59.2, 57.3, 55.9, 56.5, 61.8, 59.8, 56.8, 58.1, 57.4, 58.6, 62.3, 60.4, 58.3, 62.3]
weights["SY-Tyra"]=[None, None, None, None, None, 57.6, 54.5, None, None, None, None, None, None, None, 57.5, 60.8, None, 60.0, None]
weights["SY-Valda"]=[61.7, 57.8, 57.7, 58.6, 56.3, 60.1, 57.9, 58.2, 55.2, 60.7, 60.8, 55.6, 58.9, 58.1, 58.1, 62.3, 59.8, 58.3, None]
weights["SY605CL"]=[62.3, None, None, None, None, 60.9, 59.2, None, None, None, None, None, None, None, 59.5, 62.2, 59.9, 59.0, None]
weights["Velva"]=[59.9, 53.8, 55.0, 55.4, 53.2, 58.9, 54.3, None, None, None, None, None, None, None, 54.0, 60.0, 56.5, 58.9, 60.7]
weights["Vida"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 58.2, 60.3]
weights["WB-Mayville"]=[61.3, 57.1, 55.8, 57.4, 56.8, 59.5, 57.4, None, None, 60.3, 59.5, 54.7, 57.0, 58.9, 58.1, 60.7, 58.2, 58.9, 61.3]
weights["WB-Vantage"]=[61.7, 58.4, 59.8, None, None, 62.1, 60.6, None, None, 63.1, None, None, None, None, 60.2, None, 60.4, 59.3, 62.8]
weights["WB9507"]=[59.1, 55.3, 56.7, 57.2, 50.4, 56.9, 53.9, 56.3, 55.5, 57.7, 58.2, 52.9, 54.2, 56.1, 54.6, 59.1, 58.1, 57.0, None]
weights["WB9653"]=[62.2, None, None, 58.3, 53.9, 58.0, 56.2, None, None, 58.1, 58.5, 54.0, 57.0, 53.5, 54.6, 61.9, 57.7, 57.8, None]
weights["WB9879CLP"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 55.9, 60.6, 56.7, 58.1, None]

proteins = {}
proteins=["Advance"]=[13.6, 12.9, 12.1, 13.4, 12.7, 13.5, 13.9, None, 15.7, 12.5, None, None, None, None, 14.9, 13.3, 14.0, 12.5, None]
proteins=["Agawam"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 11.3, None]
proteins=["Alpine"]=[14.3, 13.2, None, 13.9, None, None, None, None, None, 13.3, None, None, None, None, None, None, 15.8, 12.0, None]
proteins=["Alsen"]=[15.5, 14.4, None, None, None, 14.6, 15.3, None, None, None, None, None, None, None, None, None, None, 12.3, None]
proteins=["Barlow"]=[16.0, 13.9, 13.5, 14.5, 14.1, 14.3, 14.6, 17.3, 16.7, 14.1, 14.6, None, 15.6, 14.0, 16.0, 15.2, 15.5, 13.0, 16.8]
proteins=["Bolles"]=[17.4, 15.1, 13.5, 16.1, 15.8, 15.4, 16.4, 19.8, 17.9, 15.1, 16.4, None, 16.6, 15.2, 17.7, 15.3, 16.0, 15.2, 19.1]
proteins=["Breaker"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 13.7, None]
proteins=["Brennan"]=[15.4, 14.4, 14.2, 14.2, 13.5, 14.8, 14.9, None, None, None, None, None, None, None, None, None, 14.5, 14.3, 17.1]
proteins=["Brick"]=[15.0, 13.4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
proteins=["Briggs"]=[14.9, 13.7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 13.1, 17.0]
proteins=["Cardale"]=[None, None, None, None, None, None, None, None, None, 13.8, 15.9, None, 17.2, 14..4, None, None, None, None, None]
proteins=["Choteau"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 13.5, None]
proteins=["Dapps"]=[None, None, None, None, None, 14.6, 15.0, None, None, None, None, None, None, None, None, None, None, 15.7, None]
proteins=["Duclair"]=[None, None, None, None, None, 14.5, 14.4, None, None, None, None, None, None, None, 15.8, 14.0, 14.0, 12.4, None]
proteins=["Elgin-ND"]=[15.4, 13.8, 12.8, 14.7, 13.7, 14.5, 14.7, 17.4, 16.1, 13.6, 14.4, None, 15.5, 13.6, 16.0, 14.6, 15.1, 13.7, 17.5]
proteins=["Faller"]=[13.9, 13.0, 12.3, 13.2, 13.3, 14.2, 14.2, None, None, 12.3, 14.1, None, 15.2, 13.0, 14.8, 12.4, 13.7, 12.2, 15.5]
proteins=["Focus"]=[15.0, 13.5, 12.2, 13.9, 13.6, 14.9, 14.5, 16.9, 16.1, 13.2, 13.8, None, 15.4, 13.0, None, 14.9, None, 12.6, None]
proteins=["Forefront"]=[14.9, 13.4, 13.4, 14.3, 14.0, 13.9, 14.3, 17.2, 15.6, 13.6, 14.2, None, 15.9, 13.4, 16.0, 14.5, 15.0, 13.5, 16.9]
proteins=["Freyr"]=[15.3, 13.5, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 13.5, 16.3]
proteins=["Glenn"]=[16.0, 13.7, 13.4, 15.0, 14.4, 14.6, 14.9, None, None, 14.3, None, None, None, None, 16.2, 15.6, 15.9, 13.5, 17.9]
proteins=["Howard"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 15.9, None, None, 12.8, None]
proteins=["HRS 13-04"]=[None, None, None, None, None, None, None, None, 15.9, None, None, None, None, None, None, None, None, None, None]
proteins=["HRS 3361"]=[14.8, 12.9, None, 12.5, 13.1, None, None, None, 16.0, 12.5, 13.7, None, 13.8, 12.2, 15.4, 14.0, 13.7, 13.4, None]
proteins=["HRS 3378"]=[14.1, 13.1, None, 13.1, 12.9, None, None, None, None, 12.4, None, None, None, None, 14.8, 13.3, 13.3, 12.2, None]
proteins=["HRS 3419"]=[13.3, 12.5, None, 12.2, 13.3, None, None, 15.8, 15.8, 12.5, 12.3, None, 13.2, 12.6, 15.1, 13.3, 13.1, 12.9, 14.0]
proteins=["HRS 3504"]=[None, None, None, None, None, None, None, None, None, 12.7, 13.3, None, 14.2, 12.8, None, None, 13.6, None, 16.0]
proteins=["HRS 3530"]=[14.8, 13.3, None, 14.5, 14.1, None, None, None, 16.2, 12.8, 14.8, None, 15.6, 13.2, 16.3, 14.3, 14.2, 13.5, None]
proteins=["Jenna"]=[15.4, 14.1, 13.0, 14.4, 13.9, None, None, None, None, None, None, None, None, None, None, None, None, 13.5, 16.1]
proteins=["Kelby"]=[15.8, 14.4, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 13.8, 17.8]
proteins=["LCS Albany"]=[13.5, 12.1, None, None, None, 14.3, 13.0, 16.0, 15.0, 12.3, None, None, None, None, None, 13.0, None, 11.4, 15.3]
proteins=["LCS Breakaway"]=[16.2, 13.8, None, None, None, 14.7, 14.6, 17.1, 16.1, 13.7, 14.9, None, 15.6, 13.6, 16.1, 14.7, 15.1, 13.3, None]
proteins=["LCS Iguacu"]=[12.7, 11.3, 11.1, 11.0, 11.3, 13.5, 12.2, 14.9, 13.8, 11.3, 12.7, None, 12.7, 11.7, 13.4, 12.2, 12.5, 12.5, 14.3]
proteins=["LCS Nitro"]=[14.2, 12.7, 12.0, 12.4, 12.7, 13.0, 13.3, 15.6, 15.3, 12.0, 12.7, None, 13.8, 11.9, 14.3, 12.6, 12.8, 13.1, 14.1]
proteins=["LCS Powerplay"]=[14.3, 13.4, 12.0, None, None, 14.2, 14.1, 17.0, 16.1, 12.9, 14.1, None, 14.6, 13.1, 15.4, 13.4, 14.5, 13.1, 16.0]
proteins=["LCS Pro"]=[None, None, None, None, None, 14.9, 14.7, None, None, 13.5, None, None, None, None, 16.0, 15.3, 15.6, 12.8, None]
proteins=["Linkert"]=[16.7, 14.7, 14.0, 14.6, 15.2, 14.8, 15.5, 18.7, 17.4, 14.5, 14.9, None, 15.9, 15.0, 16.9, 15.6, 15.1, 14.2, 17.3]
proteins=["Mott"]=[14.5, None, None, None, 14.2, 14.3, 14.2, None, None, None, None, None, None, None, 16.0, 14.3, 14.9, 14.1, 17.0]
proteins=["MS Chevelle"]=[14.3, 13.6, 12.5, 13.1, 13.2, 13.8, 14.1, None, None, 12.5, None, None, None, None, 14.6, 12.8, 14.1, 11.9, None]
proteins=["MS Stingray"]=[11.6, 11.2, 10.4, 10.9, 11.4, 13.6, 12.0, None, None, 10.9, None, None, None, None, 13.6, 10.9, 11.4, 11.2, None]
proteins=["ND901CL Plus"]=[13.4, None, None, None, None, 14.2, 15.0, None, None, None, None, None, None, None, 16.8, 15.3, 16.2, 13.6, None]
proteins=["Norden"]=[14.7, 14.0, 13.3, 13.9, None, 14.5, 14.8, None, 16.7, 13.5, None, None, None, None, 15.3, 14.4, 14.3, 12.5, None]
proteins=["Prestige"]=[15.0, None, None, None, None, None, None, None, None, 12.9, None, None, None, None, 15.0, 14.1, 14.2, 12.9, None]
proteins=["Prevail"]=[14.9, 13.1, 12.8, 13.4, 13.5, 14.1, 13.7, 16.1, 15.5, 13.0, 13.6, None, 14.7, 13.2, 15.5, 14.0, 13.7, 12.4, 16.4]
proteins=["Prosper"]=[14.4, 13.0, 12.4, 13.1, 13.5, 13.8, 13.9, 15.4, 16.0, 12.6, 13.9, None, 15.0, 13.0, 14.4, 12.8, 13.9, 12.2, 16.9]
proteins=["RB07"]=[15.4, 14.0, 13.7, None, None, 14.0, 14.4, None, None, 13.5, None, None, None, None, 15.7, 14.6, 14.0, 13.0, 17.3]
proteins=["Redstone"]=[13.4, None, None, None, None, None, None, None, None, 12.7, None, None, None, None, 15.4, 13.9, 13.7, 12.9, None]
proteins=["Reeder"]=[15.3, 14.1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 13.5, 17.4]
proteins=["Rollag"]=[16.2, 14.9, 13.3, 14.8, 15.1, 13.8, 15.4, 18.8, 17.9, 14.0, 15.0, None, 16.5, 15.0, 16.4, 14.7, 15.4, 13.1, 17.1]
proteins=["Sabin"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 12.8, None]
proteins=["Samson"]=[14.7, None, None, 13.4, 13.5, 14.0, 14.1, None, None, 12.5, 13.8, None, 14.2, 13.8, None, None, None, None, None]
proteins=["Select"]=[14.7, 13.3, 12.2, 12.9, 12.9, 14.0, 14.2, None, None, None, None, None, None, None, 16.3, None, None, 12.8, None]
proteins=["Steele-ND"]=[15.6, 14.4, None, 14.4, 14.3, 14.6, 14.8, None, None, None, None, None, None, None, 16.6, None, 15.3, 13.0, 16.4]
proteins=["SY Ingmar"]=[15.0, 14.4, 14.4, 14.4, 14.8, 14.4, 14.8, 18.0, 16.9, 13.9, 15.0, None, 15.4, 14.2, 16.3, 15.3, 14.9, 13.3, None]
proteins=["SY-Rowyn"]=[14.3, 13.5, 12.9, 13.1, None, 14.4, 13.7, 16.3, 15.7, 12.7, 14.4, None, 15.4, 13.1, 15.1, 14.0, 13.6, 12.9, None]
proteins=["SY-Soren"]=[15.1, 14.0, 13.9, 14.2, 14.6, 14.4, 15.0, 17.2, 16.9, 13.8, 15.0, None, 15.9, 14.1, 16.1, 15.1, 14.8, 13.5, 16.9]
proteins=["SY-Tyra"]=[None, None, None, None, None, 15.0, 14.7, None, None, None, None, None, None, None, 15.1, 13.3, None, 12.9, None]
proteins=["SY-Valda"]=[14.8, 13.4, 12.8, 13.6, 13.8, 13.9, 14.1, 17.0, 16.1, 13.0, 13.9, None, 14.9, 13.2, 15.9, 13.5, 13.7, 13.9, None]
proteins=["SY605CL"]=[15.4, None, None, None, None, 13.5, 15.0, None, None, None, None, None, None, None, 16.8, 14.5, 15.6, 13.9, None]
proteins=["Velva"]=[14.0, 13.4, 13.3, 14.2, 13.3, 13.8, 14.7, None, None, None, None, None, None, None, 15.2, 13.6, 14.6, 12.9, 16.7]
proteins=["Vida"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 13.4, 16.3]
proteins=["WB-Mayville"]=[16.0, 14.7, 13.8, 14.3, 14.2, 14.3, 15.1, None, None, 13.9, 15.2, None, 15.0, 14.1, 15.5, 14.7, 14.3, 14.0, 17.4]
proteins=["WB-Vantage"]=[15.4, 14.6, 13.7, None, None, 14.2, 15.8, None, None, 14.7, None, None, None, None, 17.4, None, 15.9, 14.8, 17.3]
proteins=["WB9507"]=[14.0, 12.8, 11.8, 12.8, 13.4, 13.8, 13.7, 15.7, 15.7, 11.9, 14.2, None, 15.5, 12.8, 15.2, 12.4, 14.1, 12.5, None]
proteins=["WB9653"]=[14.9, None, None, 13.4, 12.5, 13.7, 13.5, None, None, 12.5, 13.5, None, 14.0, 12.4, 15.2, 13.1, 14.0, 12.8, None]
proteins=["WB9879CLP+"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, None, 16.1, 14.1, 14.4, 12.9, None]

