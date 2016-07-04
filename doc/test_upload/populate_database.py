#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from __future__ import print_function
import os, sys
import django

sys.path.append('../../')
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whip.settings')
django.setup()

from hrsw import models

models.Date.objects.all().delete()
models.Zipcode.objects.all().delete()
models.Location.objects.all().delete()
models.Variety.objects.all().delete()
models.TrialEntry.objects.all().delete()
models.SignificanceEntry.objects.all().delete()
models.PlantingMethod.objects.all().delete()

locations = [
		'Carrington',
		'Minot',
		'Dazey',
		'Prosper',
		'Steele',
	]

varieties = [
		'Advance',
		'Agawam',
		'Alpine',
		'Brick',
		'Briggs',
		'Cardale',
		'Barlow',
		'Bolles',
		'Boost',
		'Chevelle',
		'Faller',
		'Mayville',
	]

zipcode = 11111
state = 'ND'
latitude = -76.1111
longitude = 78.2222
timezone = -6
daylight_savings = 1
for loc in locations:
	zipcode += 3
	latitude -= .05
	longitude += .10
	zip = models.Zipcode(zipcode=zipcode, city=loc, state=state,
			latitude=latitude, longitude=longitude, 
			timezone=timezone, daylight_savings=daylight_savings)
	zip.save()
	location = models.Location(name=loc, zipcode=zip)
	location.save()

print(models.Location.objects.all())

for name in varieties:
	variety = models.Variety(name=name)
	variety.save()

print(models.Variety.objects.all())

normal_planting = models.PlantingMethod(planting_methods='')
normal_planting.save()

print(models.PlantingMethod.objects.all())
