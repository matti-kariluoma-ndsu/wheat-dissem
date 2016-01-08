#$ python manage.py shell
#from variety_trials_data import models

# these varieties are named something similar in the database, let's 
# restore their full names

varieties = [
		"LCS Albany",
		"LCS Breakaway",
		"LCS Iguacu",
		"LCS Nitro",
		"LCS Powerplay",
		"LCS Pro",
		"MS Chevelle",
		"MS Stingray",
	]
	
for vname in varieties:
	variety = models.Variety.objects.filter(
			name__contains=vname.split()[1]
		)[0]
	variety.name = vname
	variety.save()
