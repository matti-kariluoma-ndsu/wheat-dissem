from django.db import models

# Create your models here.
class Disease(models.Model):
  name = models.CharField(max_length=200)

  def __unicode__(self):
    return self.name
 
class Variety(models.Model):
  name = models.CharField(max_length=200)
  description_url = models.CharField(max_length=200)
  picture_url = models.CharField(max_length=200)
  disease_risk = models.ForeignKey(Disease)
  
  def __unicode__(self):
    return self.name
    
class Location(models.Model):
  name = models.CharField(max_length=200)
  zipcode = models.CharField(max_length=10)
  latitude_degree = models.SmallIntegerField(blank=True)
  latitude_minute = models.SmallIntegerField(blank=True)
  latitude_second = models.SmallIntegerField(blank=True)
  latitude_millisecond = models.SmallIntegerField(blank=True)
  longitude_degree = models.SmallIntegerField(blank=True)
  longitude_minute = models.SmallIntegerField(blank=True)
  longitude_second = models.SmallIntegerField(blank=True)
  longitude_millisecond = models.SmallIntegerField(blank=True)
  
  def __unicode__(self):
    return self.name

class Date(models.Model):
  year = models.SmallIntegerField()
  month = models.SmallIntegerField()
  day = models.SmallIntegerField()
  date = models.DateField()
  
  def __unicode__(self):
    return str(self.date)
  
class Entry(models.Model):
  bushels_acre = models.DecimalField(decimal_places=5, max_digits=10)
  test_weight  = models.DecimalField(decimal_places=5, max_digits=10)
  protein_percent = models.DecimalField(decimal_places=5, max_digits=8)
  lodging_factor = models.SmallIntegerField()
  plant_height = models.DecimalField(decimal_places=5, max_digits=10)
  year    = models.ForeignKey(Date)
  location= models.ForeignKey(Location)
  name    = models.ForeignKey(Variety)

  def __unicode__(self):
    return str(self.name)+" at "+str(self.location)+", "+str(self.year)
