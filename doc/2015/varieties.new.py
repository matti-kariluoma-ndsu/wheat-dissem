#$ python manage.py shell
#from variety_trials_data import models

new_varieties = [
		"Bolles",
		"Focus",
		"HRS 13-04",
		"HRS 3504",
		"HRS 3530",
		"Prestige",
		"Prosper",
		"Redstone",
		"SY Valda",
		"WB9653",
		"WB9879CLP Plus",
		"Boost",
		"LCS Prime",
		"Surpass",
	]

for vname in new_varieties:
	variety = models.Variety(name=vname)
	variety.save()
