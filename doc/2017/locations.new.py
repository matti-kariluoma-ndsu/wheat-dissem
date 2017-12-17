#$ python manage.py shell
#from variety_trials_data import models

'''
lzipcode = models.Zipcode.objects.filter(zipcode=58761)[0]
location = models.Location(name="Mohall", zipcode=lzipcode)
location.save()
'''

lzipcode = models.Zipcode.objects.filter(zipcode=56073)[0]
location = models.Location(name="New Ulm", zipcode=lzipcode)
location.save()

lzipcode = models.Zipcode.objects.filter(zipcode=55901)[0]
location = models.Location(name="Rochester", zipcode=lzipcode)
location.save()

loc_latlong = {}
loc_latlong["Roseau"] = (48.847517,	-95.789709)
loc_latlong["Fergus Falls"] = (	46.122287	,-96.164292)
loc_latlong["Perley"] = (	47.167045,	-96.795353)
loc_latlong["Oklee"] = (	47.778944	,-95.859375)
loc_latlong["Stephen"] = (	48.470977	,-96.869744)
loc_latlong["Strathcona"] = (	48.572609	,-96.154839)
loc_latlong["Hallock"] = (	48.910165,	-97.107035)
loc_latlong["Benson"] = (	45.166997	,-95.452258)
loc_latlong["Le Center"] = (	44.457075	,-93.679328)
loc_latlong["Kimball"] = (	45.418133,	-94.323614)
loc_latlong["New Ulm"] = (	44.333814,	-94.494537)
loc_latlong["Rochester"] = (	44.390048	,-94.329771)

for name, (lat, lon) in loc_latlong.items():
  zipc = models.Location.objects.filter(name=name)[0].zipcode
  zipc.latitude = type(zipc.latitude)(lat)
  zipc.longitude = type(zipc.longitude)(lon)
  zipc.save()
