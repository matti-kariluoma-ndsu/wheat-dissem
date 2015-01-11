#$ python manage.py shell
#from variety_trials_data import models

# (name)
ls = [("Crookston"), 
("Roseau"),
("Morris"),
("Lamberton")]

ys = {}
ys["Advance"]=[104.4, 106.2, 90.2, 93.4]
ys["Barlow"]=[100.0, 102.8, 83.9, 82.0]
ys["Breaker"]=[96.6, 110.7, 84.9, 84.7]
ys["Elgin"]=[99.5, 105.6, 83.7, 89.0]
ys["Faller"]=[122.0, 112.2, 88.6, 92.0]
ys["Forefront"]=[107.9, 104.2, 89.1, 80.3]
ys["Glenn"]=[97.8, 101.2, 87.2, 83.6]
ys["HRS 3361"]=[107.4, 112.7, 80.7, 87.3]
ys["HRS 3378"]=[99.2, 107.2, 79.1, 84.1]
ys["HRS 3419"]=[119.9, 116.3, 92.2, 95.9]
ys["Jenna"]=[97.9, 106.5, 84.1, 86.7]
ys["Knudson"]=[101.9, 109.9, 84.6, 80.6]
ys["Albany"]=[116.4, 105.6, 80.8, 93.3]
ys["Breakaway"]=[100.3, 108.5, 85.6, 90.1]
ys["Iguacu"]=[109.4, 114.4, 86.2, 90.8]
ys["Powerplay"]=[110.2, 111.5, 88.8, 83.0]
ys["Linkert"]=[102.8, 104.6, 78.6, 78.5]
ys["Marshall"]=[101.8, 109.5, 80.1, 84.4]
ys["Norden"]=[103.4, 102.6, 82.9, 85.1]
ys["Prevail"]=[99.9, 106.4, 87.4, 77.9]
ys["Prosper"]=[115.2, 115.8, 89.4, 90.6]
ys["RB07"]=[110.6, 107.3, 81.3, 86.7]
ys["Rollag"]=[106.7, 100.8, 79.4, 79.9]
ys["Samson"]=[97.8, 110.3, 81.5, 90.6]
ys["SY Ingmar"]=[100.9, 105.1, 90.3, 87.0]
ys["SY Rowyn"]=[109.7, 104.1, 92.9, 90.9]
ys["SY Soren"]=[104.0, 110.3, 86.4, 86.2]
ys["Vantage"]=[93.9, 96.9, 80.9, 84.3]
ys["WB-Digger"]=[106.6, 109.2, 85.6, 83.0]
ys["WB-Mayville"]=[95.1, 115.2, 78.1, 83.1]
ys["WB9507"]=[108.2, 112.5, 92.4, 93.4]

expected_size = len(ys.values()[0])
for value in ys.values():
 assert(expected_size == len(value))

twils = [("Lamberton"),
("Morris")]

twis  = {}
twis["Advance"]=[61.7, 61.2]
twis["Barlow"]=[62.0, 60.7]
twis["Breaker"]=[62.0, 61.7]
twis["Elgin"]=[61.1, 59.2]
twis["Faller"]=[60.8, 59.6]
twis["Forefront"]=[60.8, 60.9]
twis["Glenn"]=[63.5, 62.8]
twis["HRS 3361"]=[60.0, 57.8]
twis["HRS 3378"]=[62.6, 60.1]
twis["HRS 3419"]=[58.9, 59.9]
twis["Jenna"]=[60.0, 59.9]
twis["Knudson"]=[61.4, 59.4]
twis["Albany"]=[60.9, 59.3]
twis["Breakaway"]=[61.6, 61.2]
twis["Iguacu"]=[60.6, 59.5]
twis["Powerplay"]=[61.9, 60.1]
twis["Linkert"]=[60.6, 59.6]
twis["Marshall"]=[61.1, 58.1]
twis["Norden"]=[61.7, 60.0]
twis["Prevail"]=[60.6, 62.0]
twis["Prosper"]=[61.3, 59.0]
twis["RB07"]=[60.8, 59.3]
twis["Rollag"]=[60.7, 60.4]
twis["Samson"]=[60.1, 56.7]
twis["SY Ingmar"]=[61.9, 61.6]
twis["SY Rowyn"]=[60.8, 61.2]
twis["SY Soren"]=[62.2, 60.8]
twis["Vantage"]=[60.7, 62.5]
twis["WB-Digger"]=[59.4, 58.4]
twis["WB-Mayville"]=[60.5, 58.9]
twis["WB9507"]=[59.6, 59.0]

pis = {}
pis["Advance"]=[13.7, 13.8]
pis["Barlow"]=[14.9, 15.3]
pis["Breaker"]=[14.9, 14.5]
pis["Elgin"]=[15.1, 15.0]
pis["Faller"]=[13.9, 13.8]
pis["Forefront"]=[15.6, 15.6]
pis["Glenn"]=[15.4, 16.9]
pis["HRS 3361"]=[14.1, 15.1]
pis["HRS 3378"]=[13.9, 15.0]
pis["HRS 3419"]=[13.2, 13.9]
pis["Jenna"]=[15.0, 14.7]
pis["Knudson"]=[13.7, 14.3]
pis["Albany"]=[14.1, 14.0]
pis["Breakaway"]=[14.5, 15.3]
pis["Iguacu"]=[12.6, 13.4]
pis["Powerplay"]=[14.3, 14.7]
pis["Linkert"]=[15.3, 14.7]
pis["Marshall"]=[14.0, 14.5]
pis["Norden"]=[14.1, 14.8]
pis["Prevail"]=[14.2, 13.9]
pis["Prosper"]=[14.3, 14.5]
pis["RB07"]=[14.9, 14.8]
pis["Rollag"]=[14.6, 15.6]
pis["Samson"]=[14.0, 14.8]
pis["SY Ingmar"]=[14.6, 14.4]
pis["SY Rowyn"]=[14.3, 13.7]
pis["SY Soren"]=[14.9, 14.5]
pis["Vantage"]=[15.4, 15.7]
pis["WB-Digger"]=[14.3, 14.7]
pis["WB-Mayville"]=[15.5, 15.1]
pis["WB9507"]=[14.8, 14.6]

plant, harvest =  models.Date.objects.filter(date__year=2014)
tags = "intensive"
hide=True
for v in ys:
 for i in range(len(ls)):
  l = ls[i]
  y = ys[v][i]
  if l in twils:
   tw = twis[v][twils.index(l)]
   p = pis[v][twils.index(l)]
   t = models.Trial_Entry(bushels_acre=y, test_weight=tw, protein_percent=p, plant_date=plant, harvest_date=harvest, location=models.Location.objects.filter(name=l)[0], variety=models.Variety.objects.filter(name=v)[0], hidden=hide, planting_method_tags=tags)
  else:
   t = models.Trial_Entry(bushels_acre=y, plant_date=plant, harvest_date=harvest, location=models.Location.objects.filter(name=l)[0], variety=models.Variety.objects.filter(name=v)[0], hidden=hide, planting_method_tags=tags)
  #t.save()
