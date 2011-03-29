from django.db import models
from django.forms import ModelForm

# Create your models here.
class Disease(models.Model):
  name = models.CharField(max_length=200)

  def __unicode__(self):
    return self.name

class Variety(models.Model):
  name            = models.CharField(max_length=200)
  description_url = models.CharField(max_length=200, blank=True, null=True)
  picture_url     = models.CharField(max_length=200, blank=True, null=True)
  agent_origin    = models.CharField(max_length=200, blank=True, null=True)
  year_released   = models.CharField(max_length=200, blank=True, null=True)
  straw_length    = models.CharField(max_length=200, blank=True, null=True)
  maturity        = models.CharField(max_length=200, blank=True, null=True)
  grain_color     = models.CharField(max_length=200, blank=True, null=True)
  seed_color      = models.CharField(max_length=200, blank=True, null=True)
  beard           = models.CharField(max_length=200, blank=True, null=True)
  wilt            = models.CharField(max_length=200, blank=True, null=True)
  diseases        = models.ManyToManyField(Disease, through='Disease_Entry', blank=True, null=True)
  
  def __unicode__(self):
    return self.name
  
  class Meta:
    ordering = ["-name"]

class Disease_Entry(models.Model):
  disease        = models.ForeignKey(Disease)
  variety        = models.ForeignKey(Variety)
  susceptibility = models.DecimalField(decimal_places=5, max_digits=8)
  
  def __unicode__(self):
    return str(self.variety) + " has a " + str(self.susceptibility) 
    + "% susceptibility to " + str(self.disease)

class Location(models.Model):
  name                  = models.CharField(max_length=200)
  zipcode               = models.CharField(max_length=10)
  latitude_degree       = models.SmallIntegerField(blank=True)
  latitude_minute       = models.SmallIntegerField(blank=True)
  latitude_second       = models.SmallIntegerField(blank=True)
  latitude_millisecond  = models.SmallIntegerField(blank=True)
  longitude_degree      = models.SmallIntegerField(blank=True)
  longitude_minute      = models.SmallIntegerField(blank=True)
  longitude_second      = models.SmallIntegerField(blank=True)
  longitude_millisecond = models.SmallIntegerField(blank=True)
  
  def __unicode__(self):
    return self.name

class Date(models.Model):
  year  = models.SmallIntegerField()
  month = models.SmallIntegerField()
  day   = models.SmallIntegerField()
  date  = models.DateField()
  
  def __unicode__(self):
    return str(self.date)
  
class Trial_Entry(models.Model):
  bushels_acre    = models.DecimalField(decimal_places=5, max_digits=10)
  lodging_factor  = models.SmallIntegerField(blank=True, null=True)
  test_weight     = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  protein_percent = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  plant_height    = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  moisture_basis  = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  previous_crop   = models.CharField(max_length=200, blank=True, null=True)
  seeding_rate    = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  days_to_head    = models.SmallIntegerField(blank=True, null=True)
  jday_of_head    = models.SmallIntegerField(blank=True, null=True)
  winter_survival_rate    = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  kernel_weight   = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  shatter         = models.SmallIntegerField(blank=True, null=True)
  seeds_per_round = models.SmallIntegerField(blank=True, null=True)
  canopy_density  = models.SmallIntegerField(blank=True, null=True)
  canopy_height   = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  days_to_flower  = models.SmallIntegerField(blank=True, null=True)
  seed_oil_percent= models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  plant_date      = models.ForeignKey(Date, related_name='plant_date', blank=True, null=True)
  harvest_date    = models.ForeignKey(Date, related_name='harvest_date')
  location        = models.ForeignKey(Location)
  variety         = models.ForeignKey(Variety)

  def __unicode__(self):
    return str(self.variety)+" at "+str(self.location)+", "+str(self.harvest_date.year)

# Now add custom forms to populate these data:
class VarietyForm(ModelForm):
  class Meta:
    model = Variety
