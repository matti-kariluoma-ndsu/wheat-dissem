ls = [("Dazey", 5.9, 7.0),
("Wishek", 7.9, 9.4),
("Langdon", 4.8, 5.7),
("Lakota", 5.4, 6.5),
("Cavalier", 4.4, 5.3),
("Park River", 5.8, 6.9),
("Cando", 5.1, 6.1)]
ys = {}
ws = {}
ps = {}
ys["Advance"]=[60.2, 37.4, 96.5, 84.2, 87.8, 84.2, 78.0]
ys["Alpine"]=[ 65.8, None, 99.0, None, None, None, None]
ys["Barlow"]=[ 64.4, 30.1, 93.7, 81.2, 87.4, 73.0, 73.0]
ys["Breaker"]=[ None, None, 98.5, 89.5, 85.9, 85.5, 77.5]
ys["Brennan"]=[ 70.6, 34.1, 75.3, None, None, None, None]
ys["Brick"]=[ 62.9, 33.7, 81.3, None, None, None, None]
ys["Briggs"]=[ 65.6, 28.6, None, None, None, None, None]
ys["Elgin"]=[ 65.4, 33.5, 99.3, 91.4, 93.1, 79.6, 75.3]
ys["Faller"]=[ 63.1, 32.0, 111.8, 94.8, 99.5, 87.0, 84.5]
ys["Forefront"]=[ 70.4, 32.2, 88.7, 79.6, 80.6, 75.4, 58.4]
ys["Freyr"]=[ 64.0, None, None, None, None, None, None]
ys["Glenn"]=[ 62.5, 29.8, 90.9, 79.2, 82.0, 68.5, 69.8]
ys["Jenna"]=[ 69.4, 43.4, 94.9, 91.7, 86.5, 80.2, 73.3]
ys["Kelby"]=[ 65.9, 27.1, None, None, None, None, None]
ys["Albany"]=[ None, None, 105.2, 102.9, 94.6, 89.9, 77.8]
ys["Breakaway"]=[ 61.7, 30.2, 88.0, 82.7, 85.9, 79.9, 72.1]
ys["Iguacu"]=[ None, None, 93.8, None, None, None, None]
ys["Powerplay"]=[ 59.9, 28.5, 100.7, 91.0, 91.9, 80.9, 80.6]
ys["Linkert"]=[ 67.5, 37.0, 81.4, 76.8, 79.6, 77.2, 69.5]
ys["Mott"]=[ None, 41.8, None, None, None, None, None]
ys["ND 901CL Plus"]=[ None, 30.5, None, None, None, None, None]
ys["Norden"]=[ 64.4, None, 89.7, 89.3, 80.3, 77.8, 74.0]
ys["Prosper"]=[ 67.8, 36.3, 109.7, 88.4, 98.7, 81.2, 79.4]
ys["RB07"]=[46.6, 24.4, 96.4, 81.4, 88.2, 85.9, 75.2]
ys["Rollag"]=[ 64.9, 34.7, 83.0, 85.0, 85.1, 80.4, 68.3]
ys["Sabin"]=[ 65.5, None, None, None, None, None, None]
ys["Samson"]=[ None, None, 91.5, 87.3, 83.4, 91.7, 76.7]
ys["Select"]=[ 71.1, 37.7, 84.0, None, None, None, None]
ys["Steele-ND"]=[ 64.1, 31.8, None, None, None, None, None]
ys["SY Rowyn"]=[ 58.0, 31.1, 94.7, 85.7, 90.0, 75.8, 73.4]
ys["SY Soren"]=[64.2, 31.1, 86.1, 84.6, 81.5, 82.0, 71.3]
ys["SY Tyra"]=[ None, 34.8, None, None, None, None, None]
ys["SY605 CL"]=[ None, 33.7, None, None, None, None, None]
ys["Vantage"]=[ 60.7, 33.8, 85.9, 85.6, 78.5, 79.8, 69.5]
ys["Velva"]=[ 65.2, 41.5, 99.0, None, None, None, None]
ys["WB-Digger"]=[ 70.3, 35.7, 98.5, 98.8, 93.5, 89.3, 84.7]
ys["WB-Mayville"]=[ 64.4, 35.5, 86.0, 85.0, 83.4, 79.1, 68.2]

ws["Advance"]=[ 60.8, 60.1, 61.7, 64.0, 62.0, 61.2, 61.7]
ws["Alpine"]=[ 60.4, None, 59.8, None, None, None, None]
ws["Barlow"]=[ 60.3, 59.4, 61.7, 63.3, 62.2, 60.8, 60.8]
ws["Breaker"]=[ None, None, 61.9, 63.5, 62.8, 61.5, 62.4]
ws["Brennan"]=[ 61.6, 58.2, 59.6, None, None, None, None]
ws["Brick"]=[ 60.6, 59.5, 61.5, None, None, None, None]
ws["Briggs"]=[ 59.8, 55.8, None, None, None, None, None]
ws["Elgin"]=[ 59.3, 57.3, 61.1, 62.7, 61.0, 60.4, 60.8]
ws["Faller"]=[ 58.6, 56.0, 60.7, 63.2, 61.4, 59.9, 61.1]
ws["Forefront"]=[ 61.3, 57.6, 60.5, 63.1, 61.3, 59.7, 60.7]
ws["Freyr"]=[59.4, None, None, None, None, None, None]
ws["Glenn"]=[ 63.0, 60.3, 63.0, 64.7, 63.1, 62.7, 63.2]
ws["Jenna"]=[ 60.0, 57.1, 59.0, 62.3, 60.5, 58.0, 59.5]
ws["Kelby"]=[ 60.8, 56.6, None, None, None, None, None]
ws["Albany"]=[ None, None, 61.4, 63.5, 61.4, 60.9, 61.0]
ws["Breakaway"]=[ 60.2, 58.7, 62.2, 63.9, 62.9, 61.8, 62.0]
ws["Iguacu"]=[ None, None, 60.2, None, None, None, None]
ws["Powerplay"]=[ 59.0, 57.2, 61.0, 63.7, 61.8, 60.5, 61.3]
ws["Linkert"]=[ 60.9, 58.9, 60.8, 62.9, 61.7, 60.8, 60.1]
ws["Mott"]=[ None, 59.5, None, None, None, None, None]
ws["ND 901CL Plus"]=[ None, 58.5, None, None, None, None, None]
ws["Norden"]=[ 61.1, None, 62.2, 64.1, 62.9, 61.9, 61.9]
ws["Prosper"]=[ 59.8, 57.0, 60.3, 63.2, 61.4, 59.8, 61.3]
ws["RB07"]=[ 59.1, 55.7, 60.4, 63.0, 61.1, 60.0, 60.3]
ws["Rollag"]=[ 60.6, 59.0, 61.6, 63.8, 62.3, 61.6, 61.4]
ws["Sabin"]=[ 60.0, None, None, None, None, None, None]
ws["Samson"]=[ None, None, 59.8, 61.9, 60.5, 59.8, 59.2]
ws["Select"]=[ 61.0, 59.1, 61.7, None, None, None, None]
ws["Steele-ND"]=[ 60.1, 57.9, None, None, None, None, None]
ws["SY Rowyn"]=[ 59.1, 56.5, 60.7, 62.4, 61.1, 59.6, 61.1]
ws["SY Soren"]=[ 60.9, 57.9, 61.4, 63.6, 61.6, 60.9, 61.2]
ws["SY Tyra"]=[ None, 59.2, None, None, None, None, None]
ws["SY605 CL"]=[ None, 58.5, None, None, None, None, None]
ws["Vantage"]=[ 61.3, 60.3, 62.1, 63.6, 63.3, 62.1, 62.7]
ws["Velva"]=[ 58.8, 59.0, 60.2, None, None, None, None]
ws["WB-Digger"]=[ 59.0, 57.9, 60.4, 62.1, 61.2, 59.6, 60.4]
ws["WB-Mayville"]=[ 59.0, 58.2, 60.3, 62.8, 61.7, 59.6, 60.0]

ps["Advance"]=[ 13.9, 13.9, 12.9, 13.4, 13.2, 12.2, 13.7]
ps["Alpine"]=[ 14.5, None, 13.8, None, None, None, None]
ps["Barlow"]=[ 14.8, 15.7, 14.2, 14.9, 14.2, 12.5, 14.8]
ps["Breaker"]=[ None, None, 14.1, 14.1, 13.4, 13.2, 14.3]
ps["Brennan"]=[ 14.5, 15.9, 14.8, None, None, None, None]
ps["Brick"]=[ 13.8, 15.2, 13.9, None, None, None, None]
ps["Briggs"]=[ 14.6, 17.0, None, None, None, None, None]
ps["Elgin"]=[ 14.4, 15.3, 14.1, 15.0, 14.2, 13.5, 14.7]
ps["Faller"]=[ 14.5, 15.2, 13.4, 14.0, 13.6, 12.3, 13.9]
ps["Forefront"]=[ 13.9, 15.7, 14.3, 15.4, 14.4, 14.1, 15.0]
ps["Freyr"]=[14.5, None, None, None, None, None, None]
ps["Glenn"]=[ 14.7, 16.1, 14.6, 15.4, 14.8, 12.8, 15.3]
ps["Jenna"]=[ 14.7, 15.1, 13.8, 14.2, 13.5, 13.7, 15.0]
ps["Kelby"]=[ 15.0, 17.3, None, None, None, None, None]
ps["Albany"]=[ None, None, 12.8, 12.9, 12.5, 12.5, 13.2]
ps["Breakaway"]=[ 15.1, 16.4, 14.5, 15.0, 14.6, 13.8, 15.1]
ps["Iguacu"]=[ None, None, 12.4, None, None, None, None]
ps["Powerplay"]=[ 14.9, 16.2, 13.5, 13.9, 13.4, 13.2, 14.0]
ps["Linkert"]=[ 14.9, 16.2, 15.4, 15.6, 14.8, 13.6, 15.7]
ps["Mott"]=[ None, 14.8, None, None, None, None, None]
ps["ND 901CL Plus"]=[ None, 17.2, None, None, None, None, None]
ps["Norden"]=[ 14.2, None, 13.9, 14.1, 13.8, 12.9, 14.1]
ps["Prosper"]=[ 14.0, 14.7, 13.2, 13.7, 13.3, 12.2, 13.7]
ps["RB07"]=[ 13.2, 16.6, 14.5, 15.1, 14.5, 13.4, 14.9]
ps["Rollag"]=[15.3, 17.5, 14.8, 15.1, 14.6, 13.6, 15.4]
ps["Sabin"]=[ 14.4, None, None, None, None, None, None]
ps["Samson"]=[ None, None, 13.9, 14.2, 13.3, 13.0, 14.3]
ps["Select"]=[ 13.6, 15.3, 14.0, None, None, None, None]
ps["Steele-ND"]=[ 14.8, 16.4, None, None, None, None, None]
ps["SY Rowyn"]=[14.5, 16.0, 14.0, 14.2, 13.3, 13.1, 14.2]
ps["SY Soren"]=[ 14.8, 16.8, 14.8, 15.2, 14.1, 13.8, 15.2]
ps["SY Tyra"]=[ None, 15.0, None, None, None, None, None]
ps["SY605 CL"]=[ None, 16.0, None, None, None, None, None]
ps["Vantage"]=[ 16.3, 15.9, 15.8, 15.3, 14.4, 15.6, 16.5]
ps["Velva"]=[ 15.0, 14.1, 13.8, None, None, None, None]
ps["WB-Digger"]=[ 14.4, 15.3, 14.1, 14.3, 14.2, 12.8, 14.0]
ps["WB-Mayville"]=[ 15.3, 16.7, 14.5, 15.0, 14.7, 13.8, 14.9]

plant, harvest =  models.Date.objects.filter(date__year=2013)
for v in ys:
  for i in range(7):
   y = ys[v][i]
   if y is None:
    continue
   p = ps[v][i]
   w = ws[v][i]
   l, lsd10, lsd5 = ls[i]
   t = models.Trial_Entry(bushels_acre=y, lsd_05=lsd5, lsd_10=lsd10, plant_date=plant, harvest_date=harvest, location=models.Location.objects.filter(name=l)[0], variety=models.Variety.objects.filter(name=v)[0], hidden=False)
   if p:
    t.protein_percent = p
   if w:
    t.test_weight = w
   t.save()
