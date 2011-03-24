from django.db import models

# Create your models here.
class Variety(models.Model):
  name = models.CharField(max_length=200)
  description_url = models.CharField(max_length=200)
  picture_url = models.CharField(max_length=200)
  
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
  bushels = models.DecimalField(decimal_places=5, max_digits=10)
  weight  = models.DecimalField(decimal_places=5, max_digits=10)
  protein = models.DecimalField(decimal_places=5, max_digits=8)
  year    = models.ForeignKey(Date)
  location= models.ForeignKey(Location)
  name    = models.ForeignKey(Variety)

  def __unicode__(self):
    return str(self.name)+" at "+str(self.location)+", "+str(self.year)
