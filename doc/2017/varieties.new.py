#$ python manage.py shell
#from variety_trials_data import models


new_varieties = [
		"AFK Astro",
		"Caliber",
		"Lang-MN",
		"LCS Rebel",
		"LCS Trigger",
		"MS Camaro",
		"ND VitPro",
		"Mix (Proper / ND VitPro)",
		"Mix (Shelly / Bolles)",
		"SY Rustler",
		"TCG Climax",
		"WB9479",
		"WB9590",
		"WB9719",
	]

for vname in new_varieties:
	variety = models.Variety(name=vname)
	variety.save()

ambush = models.Variety.objects.filter(name="Dyna-Gro Ambush")[0]
ambush.name = "Ambush"
ambush.save()

rock = models.Variety.objects.filter(name="SY Rockford 07S0027-3")[0]
rock.name = "SY Rockford"
rock.save()

