from django.db import models

# Create your models here.
class Variety(models.Model):
  name = models.CharField(max_length=200)
  
  def __unicode__(self):
    return self.name

class Coordinate(models.Model):
  degree = models.SmallIntegerField()
  minute = models.SmallIntegerField()
  second = models.SmallIntegerField()
  millisecond = models.SmallIntegerField()
  
  def __unicode__(self):
    return str(self.degree)+" degrees "+str(self.minute)+"'"+str(self.second)+"."+str(self.millisecond)+"\""
    
class Location(models.Model):
  name = models.CharField(max_length=200)
  latitude  = models.ForeignKey(Coordinate, related_name="latitude")
  longitude = models.ForeignKey(Coordinate, related_name="longitude")
  
  def __unicode__(self):
    return str(self.name)+": "+str(self.latitude)+", "+str(self.longitude)

class Date(models.Model):
  year = models.SmallIntegerField()
  
  def __unicode__(self):
    return str(self.year)
  
class Entry(models.Model):
  bushels = models.DecimalField(decimal_places=5, max_digits=10)
  weight  = models.DecimalField(decimal_places=5, max_digits=10)
  protein = models.DecimalField(decimal_places=5, max_digits=8)
  year    = models.ForeignKey(Date)
  location= models.ForeignKey(Location)
  name    = models.ForeignKey(Variety)

  def __unicode__(self):
    return str(self.name)+" at "+str(self.location)+", "+str(self.year)
