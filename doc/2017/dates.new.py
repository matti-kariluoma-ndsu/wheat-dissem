#$ python manage.py shell
#from variety_trials_data import models

plant_date = models.Date(date="2017-05-01")
plant_date.save()
harvest_date = models.Date(date="2017-08-01")
harvest_date.save()
