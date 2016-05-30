#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django.db import models

class Date(models.Model):
	date	= models.DateField(help_text='Format: MM/DD/YYYY')
	def __unicode__(self):
		return str(self.date)

class PlantingMethod(models.Model):
	planting_methods = models.CharField(max_length=256, help_text='comma separated keywords')
	def __unicode__(self):
		pms = self.planting_methods
		if pms == '':
			return 'Normal'
		return pms

class Zipcode(models.Model):
	zipcode         	= models.PositiveIntegerField()
	city            	= models.CharField(max_length=200)
	state           	= models.CharField(max_length=2)
	latitude        	= models.DecimalField(decimal_places=10, max_digits=13)
	longitude       	= models.DecimalField(decimal_places=10, max_digits=13)
	timezone        	= models.SmallIntegerField()
	daylight_savings	= models.SmallIntegerField()
	def __unicode__(self):
		return str(self.zipcode).zfill(5) + ": " + self.city + ", " + self.state

class Location(models.Model):
	name     	= models.CharField(max_length=200, help_text='')
	zipcode  	= models.ForeignKey(Zipcode, 
			help_text='Format: 12345, The five-digit zipcode of this locaton.'
		)
	latitude	= models.DecimalField(decimal_places=10, max_digits=13, blank=True, null=True, 
			help_text='Format: 46.8772, Overrides the latitude value derived from the zipcode. The Equator is 0, south is negative.'
		)
	longitude	= models.DecimalField(decimal_places=10, max_digits=13, blank=True, null=True, 
			help_text='Format: -96.7894, Overrides the longitude value derived from the zipcode. The Grand Meridian is 0, west is negative.'
		)
	def __unicode__(self):
		return self.name

class Disease(models.Model):
	name = models.CharField(max_length=200, help_text='')
	def __unicode__(self):
		return self.name

class Variety(models.Model):
	name           	= models.CharField(max_length=200, help_text='')
	description_url	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='A link to a resource that describes this variety.'
		)
	picture_url    	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='A link to a small picture of this variety.'
		)
	agent_origin   	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='The name of the cultivar.'
		)
	year_released  	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='Format: YYYY, The year this variety was released.'
		)
	straw_length   	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='The length of the stems.'
		)
	maturity       	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='Type of maturity(?)'
		)
	grain_color    	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='Color of mature grain.'
		)
	seed_color     	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='Color of seed.'
		)
	beard          	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='Color(?) of beard.'
		)
	wilt           	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='Degree of wilt(?)'
		)
	diseases       	= models.ManyToManyField(Disease, through='DiseaseEntry')
	def __unicode__(self):
		return self.name
	def natural_key(self):
		return (self.name,);
	class Meta:
		ordering = ["-name"]

class VarietyManager(Variety):
	def get_by_natural_key(self, lookup):
		return self.get(name=lookup)

class DiseaseEntry(models.Model):
	disease				= models.ForeignKey(Disease, help_text='Name of disease')
	variety				= models.ForeignKey(Variety, help_text='Name of variety')
	susceptibility = models.DecimalField(decimal_places=5, max_digits=8, 
			help_text='Format: 5.00, Percentage of susceptibility of this variety to this disease.'
		)
	def __unicode__(self):
		return str(self.variety) + " has a " + str(self.susceptibility) 
		+ "% susceptibility to " + str(self.disease)

class TrialEntry(models.Model):
	measures = ('bushels_acre', 'protein_percent', 'test_weight', )
	# Database fields
	lsd_05               = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True, help_text='Bushels per Acre LSD at a=0.05 (for the entire location in this year)')
	lsd_10               = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True, help_text='Bushels per Acre LSD at a=0.10 (for the entire location in this year)')
	hsd_10               = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True, help_text='Bushels per Acre HSD at a=0.05 (for the entire location in this year)')
	bushels_acre        	= models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True,
			help_text='Format: 37.4, Bushels per Acre'
		)
	protein_percent     	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format: 12.1, Percentage of protein per pound'
		)
	test_weight         	= models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True, 
			help_text='Format: 50.1, Pounds per bushel'
		)
	location            	= models.ForeignKey(Location, on_delete=models.DO_NOTHING,
			help_text='Name of location'
		)
	variety             	= models.ForeignKey(Variety, on_delete=models.DO_NOTHING,
			help_text='Name of variety'
		)
	harvest_date        	= models.ForeignKey(Date, related_name='harvest_date', on_delete=models.DO_NOTHING,
			help_text='Date this trial was harvested'
		)
	# Optional, often reported
	plant_date          	= models.ForeignKey(Date, related_name='plant_date', on_delete=models.DO_NOTHING, blank=True, null=True, 
			help_text='Date this trial was planted'
		)
	planting_method_tags_new= models.ForeignKey(PlantingMethod, related_name='planting_method_tags', on_delete=models.DO_NOTHING, blank=True, null=True,
			help_text='Comma-separated list of planting methods'
		)
	planting_method_tags = models.CharField(max_length=200, blank=True, null=True, help_text='Comma-separated list of planting methods')

	# Optional, usually not reported
	seeding_rate        	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format: 2.1, Number of seeds (in 1000s) per foot'
		)
	previous_crop       	= models.CharField(max_length=200, blank=True, null=True, 
			help_text='Name of the previous crop at this location'
		)
	moisture_basis      	= models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True, 
			help_text='Format: 3, Ranking: 1 (Dry) to 9 (Flooded)'
		)
	plant_height        	= models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True, 
			help_text='Format: 24.5, Height of plant in inches'
		)
	days_to_head        	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format: 57, Days from planting to head'
		)
	lodging_factor      	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format: 4, Ranking: 1 (No Lodging) to 9 (Heavy Lodging)'
		)
	jday_of_head        	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format: 265, Julian day of head'
		)
	winter_survival_rate	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format: 20.5, Percentage that survive winter'
		)
	shatter             	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format: 4, Ranking: 1 (Least Shatter) to 9 (Most Shatter)'
		)
	seeds_per_round     	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format: 1.2, Number of seeds (in 1000s) per round'
		)
	canopy_density      	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format 4, Ranking: 1 (Least Dense) to 9 (Most Dense)'
		)
	canopy_height       	= models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True, 
			help_text='Format: 26.2, Height of canopy in inches'
		)
	days_to_flower      	= models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True, 
			help_text='Format: 28, Days from planting to flower'
		)
	seed_oil_percent    	= models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True, 
			help_text='Format: 5.6, Percentage of mass'
		)
	kernel_weight       	= models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True, 
			help_text='Format: 30.5, Grams per 1000 kernels'
		)
	# Bookkeeping
	hidden              	= models.BooleanField(default=False, 
			help_text='Should we hide this trial from the public-facing website?'
		)
	def __unicode__(self):
		return '{year}: {variety} at {location} using {method} planting'.format(
				year = str(self.harvest_date.date.year),
				variety = str(self.variety),
				location = str(self.location),
				method = str(self.planting_method_tags),
			)
		
class SignificanceEntry(models.Model):
	method_lsd = 'LSD'
	method_hsd = 'HSD'
	method_mean = 'Mean'
	method_cv = 'CV'
	methods = (method_lsd, method_hsd, method_mean, method_cv, )
	levels = (None, 0.1, 0.05, )
	
	trials    = models.ManyToManyField(TrialEntry)
	comparing	= models.CharField(max_length=200,
			help_text='Field in TrialEntry this LSD compares (one of bushels_acre, protein_percent, test_weight)'
		)
	method   = models.CharField(max_length=16, 
			help_text='Method of comparison, one of ' + ', '.join(methods)
		)
	alpha    = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True,
			help_text='Significance level of reported value'
		)
	value    = models.DecimalField(decimal_places=5, max_digits=10, 
			help_text='Value to compare other TrialEntries against'
		)
	def __unicode__(self):
		return str(self.comparing)+' '+str(self.method)+' '+str(self.alpha)+': '+str(self.value)

