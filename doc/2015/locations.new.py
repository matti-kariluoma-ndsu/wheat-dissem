#$ python manage.py shell
#from variety_trials_data import models

lzipcode = models.Zipcode.objects.filter(zipcode=58482)[0]
location = models.Location(name="Steele", zipcode=lzipcode)
location.save()
