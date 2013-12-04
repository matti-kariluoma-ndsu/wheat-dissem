plant, harvest =  models.Date.objects.filter(date__year=2013)
l, lsd10, lsd5 = ("Carrington", 5.4, 6.4)
tags = "dryland"
hide = False
ys = {}
ys["Advance"]=[ 50.3, 63.3, 13.4]
ys["Alpine"]=[54.6, 62.8, 14.1]
ys["Alsen"]=[ 54.7, 63.6, 14.3]
ys["Barlow"]=[ 57.1, 64.1, 14.8]
ys["Breaker"]=[ 53.4, 64.3, 13.9]
ys["Brennan"]=[ 53.2, 64.3, 14.2]
ys["Brick"]=[ 54.7, 63.5, 13.3]
ys["Briggs"]=[ 54.4, 63.0, 13.8]
ys["Elgin"]=[ 55.4, 62.3, 14.2]
ys["Faller"]=[ 57.5, 62.6, 13.9]
ys["Forefront"]=[ 57.2, 63.2, 13.9]
ys["Freyr"]=[ 52.8, 62.7, 13.8]
ys["Glenn"]=[ 50.5, 64.8, 14.7]
ys["Howard"]=[ 54.3, 63.5, 14.6]
ys["Jenna"]=[ 55.9, 62.5, 13.7]
ys["Kelby"]=[ 53.7, 63.4, 14.9]
ys["Albany"]=[ 53.2, 62.9, 13.0]
ys["Breakaway"]=[ 53.1, 64.5, 14.8]
ys["Iguacu"]=[ 59.4, 63.7, 12.7]
ys["Powerplay"]=[ 60.9, 64.0, 13.5]
ys["Linkert"]=[ 52.1, 63.1, 14.6]
ys["Mott"]=[ 56.4, 63.0, 14.0]
ys["Stingray"]=[ 60.7, 62.2, 11.4]
ys["ND 901CL Plus"]=[ 53.4, 63.0, 15.0]
ys["Norden"]=[ 50.6, 64.4, 13.4]
ys["Prosper"]=[ 57.7, 63.2, 14.0]
ys["RB07"]=[ 50.7, 60.5, 13.9]
ys["Rollag"]=[ 55.8, 63.9, 15.1]
ys["Sabin"]=[ 52.7, 62.4, 13.6]
ys["Samson"]=[ 54.2, 62.5, 14.0]
ys["Select"]=[ 54.1, 63.5, 13.0]
ys["Steele-ND"]=[ 53.0, 64.2, 14.5]
ys["SY Rowyn"]=[55.9, 62.4, 13.6]
ys["SY Soren"]=[ 52.2, 63.0, 14.9]
ys["SY Tyra"]=[ 58.6, 64.3, 13.6]
ys["SY605 CL"]=[ 56.4, 62.9, 13.8]
ys["Vantage"]=[ 48.3, 62.9, 14.5]
ys["Velva"]=[ 49.4, 61.8, 14.2]
ys["WB-Digger"]=[ 57.0, 62.5, 13.7]
ys["WB-Mayville"]=[ 55.5, 62.4, 15.0]
for v in ys:
  y, w, p = ys[v]
  t = models.Trial_Entry(bushels_acre=y, protein_percent=p, test_weight = w, lsd_10=lsd10, lsd_05=lsd5, plant_date=plant, harvest_date=harvest, location=models.Location.objects.filter(name=l)[0], variety=models.Variety.objects.filter(name=v)[0], hidden=hide, planting_method_tags=tags)
  t.save()
  
l, lsd10, lsd5 = ("Carrington", 5.2, 6.2)
tags = "elite"
hide = True
del ys
ys = {}
ys["Advance"]=[ 33.3, 60.4, 13.9]
ys["Barlow"]=[ 46.7, 61.7, 15.3]
ys["Breaker"]=[ 40.3, 62.1, 14.9]
ys["Brennan"]=[ 37.1, 60.5, 16.3]
ys["Brick"]=[ 35.7, 61.7, 14.4]
ys["Briggs"]=[ 33.1, 60.4, 15.1]
ys["Elgin"]=[ 47.9, 60.6, 14.7]
ys["Faller"]=[ 43.7, 59.4, 14.2]
ys["Forefront"]=[ 42.6, 60.5, 15.6]
ys["Freyr"]=[ 39.5, 60.5, 15.0]
ys["Glenn"]=[ 43.9, 62.3, 15.4]
ys["Howard"]=[ 36.1, 60.8, 15.3]
ys["Jenna"]=[ 46.0, 59.1, 15.5]
ys["Kelby"]=[ 30.6, 60.1, 16.6]
ys["Linkert"]=[ 37.8, 61.4, 16.2]
ys["Norden"]=[ 35.7, 60.9, 14.1]
ys["Prosper"]=[ 37.6, 59.6, 14.6]
ys["RB07"]=[ 28.1, 58.7, 14.5]
ys["Rollag"]=[ 41.6, 61.6, 15.6]
ys["Select"]=[ 32.2, 61.1, 14.1]
ys["Steele-ND"]=[ 32.2, 60.8, 15.5]
ys["SY Rowyn"]=[ 30.9, 59.3, 14.6]
ys["SY Soren"]=[ 37.1, 60.8, 16.2]
ys["Vantage"]=[ 32.4, 59.7, 15.8]
ys["Velva"]=[ 40.3, 60.0, 14.3]
ys["WB-Digger"]=[ 43.7, 59.3, 13.9]
ys["WB-Mayville"]=[ 34.6, 59.4, 15.5]
for v in ys:
  y, w, p = ys[v]
  t = models.Trial_Entry(bushels_acre=y, protein_percent=p, test_weight = w, lsd_10=lsd10, lsd_05=lsd5, plant_date=plant, harvest_date=harvest, location=models.Location.objects.filter(name=l)[0], variety=models.Variety.objects.filter(name=v)[0], hidden=hide, planting_method_tags=tags)
  t.save()

l, lsd10, lsd5 = ("Carrington", 5.3, 6.4)
tags = "irrigated"
hide = True
del ys
ys = {}
ys["Advance"]=[ 75.9, 62.3, 12.6]
ys["Alsen"]=[ 66.6, 62.0, 14.7]
ys["Barlow"]=[ 70.4, 62.4, 14.1]
ys["Breaker"]=[ 72.5, 62.3, 13.3]
ys["Brennan"]=[ 66.9, 60.8, 14.6]
ys["Brick"]=[ 65.9, 62.4, 14.4]
ys["Briggs"]=[ 69.9, 61.4, 14.1]
ys["Elgin"]=[ 80.4, 61.2, 13.6]
ys["Faller"]=[ 73.0, 60.6, 12.7]
ys["Forefront"]=[ 72.5, 60.7, 13.8]
ys["Freyr"]=[ 71.1, 60.9, 14.0]
ys["Glenn"]=[ 74.3, 63.9, 14.1]
ys["Howard"]=[ 74.7, 62.4, 13.8]
ys["Jenna"]=[ 79.5, 60.1, 13.6]
ys["Kelby"]=[ 64.8, 60.9, 15.3]
ys["Albany"]=[ 83.6, 61.4, 12.2]
ys["Breakaway"]=[ 75.9, 62.9, 14.4]
ys["Iguacu"]=[ 68.7, 61.6, 11.8]
ys["Powerplay"]=[ 84.7, 62.1, 12.7]
ys["Linkert"]=[ 71.3, 62.2, 14.7]
ys["Norden"]=[ 71.9, 62.7, 13.0]
ys["Prosper"]=[ 81.9, 61.2, 12.9]
ys["RB07"]=[ 60.4, 59.0, 13.8]
ys["Rollag"]=[ 69.0, 62.2, 14.2]
ys["Samson"]=[ 75.8, 60.5, 13.2]
ys["Select"]=[ 67.9, 62.3, 13.2]
ys["Steele-ND"]=[ 70.5, 62.6, 14.3]
ys["SY Rowyn"]=[ 71.0, 60.3, 13.7]
ys["SY Soren"]=[ 73.3, 61.5, 14.7]
ys["SY Tyra"]=[ 71.6, 61.6, 12.9]
ys["Vantage"]=[ 68.7, 62.5, 14.3]
ys["Velva"]=[ 76.9, 60.9, 13.6]
ys["WB-Digger"]=[ 77.8, 60.7, 12.9]
ys["WB-Mayville"]=[ 65.2, 60.7, 14.5]
for v in ys:
  y, w, p = ys[v]
  t = models.Trial_Entry(bushels_acre=y, protein_percent=p, test_weight = w, lsd_10=lsd10, lsd_05=lsd5, plant_date=plant, harvest_date=harvest, location=models.Location.objects.filter(name=l)[0], variety=models.Variety.objects.filter(name=v)[0], hidden=hide, planting_method_tags=tags)
  t.save()
