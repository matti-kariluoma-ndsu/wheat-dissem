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

class Zipcode(models.Model):
  zipcode          = models.PositiveIntegerField()
  city             = models.CharField(max_length=200)
  state            = models.CharField(max_length=2)
  latitude         = models.DecimalField(decimal_places=10, max_digits=13)
  longitude        = models.DecimalField(decimal_places=10, max_digits=13)
  timezone         = models.SmallIntegerField()
  daylight_savings = models.SmallIntegerField()
  
  def __unicode__(self):
    return str(self.zipcode).zfill(5) + ": " + self.city + ", " + self.state

class Location(models.Model):
  name      = models.CharField(max_length=200)
  zipcode   = models.ForeignKey(Zipcode)
  latitude  = models.DecimalField(decimal_places=10, max_digits=13, blank=True, null=True)
  longitude = models.DecimalField(decimal_places=10, max_digits=13, blank=True, null=True)

  
  def __unicode__(self):
    return self.name

class Date(models.Model):
  date  = models.DateField()
  
  def __unicode__(self):
    return str(self.date)
  
class Trial_Entry(models.Model):
  bushels_acre         = models.DecimalField(decimal_places=5, max_digits=10)
  protein_percent      = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  test_weight          = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  kernel_weight        = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  plant_height         = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  days_to_head         = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  lodging_factor       = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  jday_of_head         = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  winter_survival_rate = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  shatter              = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  seeds_per_round      = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  canopy_density       = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  canopy_height        = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  days_to_flower       = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  seed_oil_percent     = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  planting_method_tags = models.CharField(max_length=200, blank=True, null=True)
  seeding_rate         = models.DecimalField(decimal_places=5, max_digits=8, blank=True, null=True)
  previous_crop        = models.CharField(max_length=200, blank=True, null=True)
  moisture_basis       = models.DecimalField(decimal_places=5, max_digits=10, blank=True, null=True)
  plant_date           = models.ForeignKey(Date, related_name='plant_date', blank=True, null=True)
  harvest_date         = models.ForeignKey(Date, related_name='harvest_date')
  location             = models.ForeignKey(Location)
  variety              = models.ForeignKey(Variety)

  def __unicode__(self):
    return str(self.variety)+" at "+str(self.location)+", "+str(self.harvest_date.date.year)

# Now add custom forms to populate these data:
class VarietyForm(ModelForm):
  class Meta:
    model = Variety
    # exclude any ForeignKey or ManyToMany fields
    exclude = ('diseases',)
    
class Trial_EntryForm(ModelForm):
  class Meta:
    model = Trial_Entry
