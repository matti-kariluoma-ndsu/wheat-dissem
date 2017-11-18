#$ python manage.py shell
#from variety_trials_data import models

new_varieties = [
		"SY Rockford 07S0027-3",
		"Egan",
		"Faller (1.8M PLS)",
		"Filler (Glenn)",
		"HRS 3100",
		"HRS 3616",
		"LCS Anchor",
		"MN10261-1",
		"Shelly",
		"TCG Cornerstone",
		"TCG Spitfire",
		"TCG Wildfire",
		"WB-Mayville (1.8M PLS)",
		"WB9312",
		"Dyna-Gro Ambush",
	]

for vname in new_varieties:
	variety = models.Variety(name=vname)
	variety.save()
