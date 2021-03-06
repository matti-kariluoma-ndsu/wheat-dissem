#$ python manage.py shell
#from variety_trials_data import models

# name, lsd10, lsd5
ls = [("Carrington", 6.0, 7.1),
("Dazey", 7.1, 8.6),
("Wishek", 9.7, 11.5),
("Casselton", 4.9, None),
("Prosper", 7.4, None),
("Langdon", 5.5, 6.6),
("Pekin", 4.2, 5.0),
("Cavalier", 6.9, 8.3),
("Park River", 4.2, 5.0),
("Cando", 4.6, 5.5),
("Dickinson", 5.5, None),
("Hettinger", 5.2, None),
("Minot", 8.3, None),
("Williston", None, 4.5)]

ys = {}
ys["Advance"]=[88.9, 94.6, 65.1, 90.3, 83.8, 84.9, 85.1, 70.1, 83.4, 64.1, 88.1, 89.0, 67.1, 38.0]
ys["Agawam"]=[None, None, None, 75.8, 69.5, None, None, None, None, None, None, None, None, 35.2]
ys["Alpine"]=[85.8, 92.9, None, 79.0, 75.1, 91.5, None, None, None, None, 92.6, None, 55.7, 46.1]
ys["Alsen"]=[85.4, None, None, 74.6, 72.0, None, None, None, None, None, None, None, None, 41.2]
ys["Barlow"]=[87.4, 89.8, 80.5, 78.2, 77.3, 85.5, 87.6, 74.8, 80.5, 74.8, 91.1, 80.1, 62.2, 36.3]
ys["Breaker"]=[85.8, None, None, 89.4, 82.4, 83.1, None, None, None, None, 88.4, 84.5, 64.5, 39.0]
ys["Brennan"]=[83.3, 78.7, 68.5, 82.3, 77.3, 80.0, None, None, None, None, 84.9, 80.4, 54.1, 41.3]
ys["Brick"]=[92.1, 87.8, 73.0, None, None, 77.8, None, None, None, None, None, None, None, None]
ys["Briggs"]=[81.6, 87.6, 68.9, 81.0, 82.6, None, None, None, None, None, None, None, 56.4, 38.2]
ys["Cardale"]=[None, None, None, None, None, 83.7, None, None, None, None, None, None, None, None]
ys["Choteau"]=[None, None, None, 71.2, 68.1, None, None, None, None, None, None, None, 52.6, 37.1]
ys["Dapps"]=[None, None, None, 85.5, 68.3, None, None, None, None, None, None, None, None, 33.3]
ys["Duclair"]=[75.5, None, None, 83.9, 75.0, None, None, None, None, None, 88.5, None, 66.6, 40.3]
ys["Elgin"]=[93.2, 97.7, 71.9, 88.5, 78.8, 90.1, 90.7, 74.8, 82.7, 71.3, 88.9, 88.5, 62.3, 41.7]
ys["Faller"]=[110.9, 109.7, 74.3, 101.2, 92.0, 95.5, 102.1, 87.8, 92.9, 84.0, 95.1, 94.1, 76.4, 41.5]
ys["Forefront"]=[92.9, 90.1, 67.1, 91.5, 83.2, 74.3, 81.3, 68.2, 78.7, 76.3, 80.0, 85.2, 55.8, 45.0]
ys["Freyr"]=[90.0, 83.0, None, 86.1, 72.5, None, None, None, None, None, None, None, 60.9, 42.0]
ys["Glenn"]=[87.6, 95.5, 66.9, 76.5, 77.2, 75.8, None, None, None, None, 86.0, 77.1, 57.5, 33.7]
ys["Howard"]=[94.2, None, None, 86.8, 79.9, None, None, None, None, None, 91.2, 80.3, 72.0, 40.5]
ys["HRS 3361"]=[100.0, None, None, None, None, 84.6, 85.9, 81.2, 84.9, 73.1, 83.9, 88.2, 56.6, 38.0]
ys["HRS 3378"]=[85.6, None, None, None, None, 87.1, 86.8, 76.5, 85.3, 66.3, 92.7, 89.6, 58.7, 36.5]
ys["HRS 3419"]=[110.2, None, None, None, None, 88.9, 90.7, 87.0, 92.6, 77.4, 69.8, 97.9, 67.7, 41.9]
ys["Jenna"]=[100.0, 92.2, 72.5, 87.8, 77.6, 87.0, 83.2, 75.6, 88.7, 70.2, 93.3, 86.5, 67.5, 42.5]
ys["Kelby"]=[83.6, 72.2, 76.1, 72.9, 75.7, None, None, None, None, None, 81.3, None, 54.9, 37.8]
ys["Albany"]=[106.5, 90.7, 58.7, 93.7, 77.9, 95.2, 83.6, 84.1, 88.8, 67.0, 91.2, 95.4, 77.1, 44.0]
ys["Breakaway"]=[89.3, 83.2, 63.2, 82.3, 83.2, 77.1, 94.2, 63.3, 85.3, 72.3, 88.9, 86.4, 63.1, 37.1]
ys["Iguacu"]=[94.5, 81.7, 56.1, 94.6, 85.2, 90.6, 94.5, 75.0, 91.2, 73.6, 78.2, 88.2, 60.0, 39.6]
ys["Nitro"]=[102.6, 90.9, 80.5, None, None, 91.0, 98.7, 77.4, 93.9, 76.2, 80.9, None, None, None]
ys["Powerplay"]=[96.6, 88.6, 72.8, 87.8, 79.4, 88.1, 86.6, 74.7, 90.5, 73.6, 92.2, 82.9, 65.0, 40.9]
ys["Pro"]=[None, None, None, None, None, None, None, None, None, None, 92.2, None, None, None]
ys["Linkert"]=[92.3, 85.1, 71.6, 83.8, 77.5, 81.7, 82.6, 65.9, 78.5, 63.5, 87.2, 80.5, 61.1, 41.6]
ys["Mott"]=[97.2, None, 74.5, 89.5, 80.1, None, None, None, None, None, 87.0, 78.9, 60.6, 38.9]
ys["Chevelle"]=[102.6, 101.7, 79.1, 81.0, 81.7, 91.2, None, None, None, None, None, 91.3, 65.0, None]
ys["Stingray"]=[105.4, 95.1, 83.2, 102.1, 78.0, 93.4, None, None, None, None, 87.4, 95.9, 75.1, None]
ys["ND 901CL Plus"]=[83.3, None, None, 78.9, 76.3, None, None, None, None, None, 79.5, 73.5, 59.9, 37.0]
ys["Norden"]=[96.3, 91.4, None, 83.7, 78.5, 80.5, 92.3, 71.4, 82.8, 71.0, 87.4, 83.5, 54.3, 39.7]
ys["Prevail"]=[93.4, 93.3, 64.2, 86.3, 88.5, 84.8, 82.5, 78.5, 84.2, 73.7, 85.3, 87.2, 74.1, 43.3]
ys["Prosper"]=[105.2, 107.8, 81.8, 89.9, 90.1, 92.9, 99.6, 80.4, 95.5, 79.0, 88.7, 86.3, 74.7, 41.6]
ys["RB07"]=[92.2, None, None, 90.6, 79.2, 88.3, 92.8, 72.9, 87.5, 73.1, 61.1, 84.1, 61.1, 42.6]
ys["Reeder"]=[None, None, None, 80.6, 79.1, None, None, None, None, None, None, None, None, 44.3]
ys["Rollag"]=[97.5, 90.9, 66.3, 83.8, 80.8, 85.1, 85.2, 72.0, 81.5, 70.1, 86.5, 84.2, 63.2, 40.2]
ys["Sabin"]=[None, None, None, None, None, None, None, None, None, None, None, 81.2, None, 41.5]
ys["Samson"]=[72.6, 74.8, 70.2, 81.1, 82.7, 86.3, 97.5, 72.1, 88.4, 80.8, 87.6, 90.1, 65.0, 41.5]
ys["Select"]=[94.8, 90.0, 73.2, 80.9, 83.0, 77.3, None, None, None, None, 82.4, 82.6, 53.4, 36.1]
ys["Shaw"]=[None, None, None, 87.3, 70.0, None, None, None, None, None, None, None, None, None]
ys["Steele-ND"]=[89.8, 84.7, 68.2, 83.0, 76.4, None, None, None, None, None, 79.9, 80.9, 69.3, 41.3]
ys["SY Ingmar"]=[90.9, 85.9, 61.5, 89.6, 76.1, 86.8, 85.8, 66.6, 80.7, 74.4, 88.3, 82.1, 68.1, 44.2]
ys["SY Rowyn"]=[93.1, 92.4, 58.8, 93.1, 87.0, 87.0, 92.8, 66.4, 84.8, 77.6, 87.0, 85.0, 74.6, 37.3]
ys["SY Soren"]=[89.9, 93.0, 77.4, 83.1, 74.3, 85.1, 80.8, 65.9, 84.3, 66.8, 86.9, 86.2, 62.3, 37.2]
ys["SY Tyra"]=[85.0, None, 74.9, 78.6, 63.3, None, None, None, None, None, 90.8, 85.7, 56.7, 41.2]
ys["SY605 CL"]=[82.9, None, 65.3, 82.6, 85.5, None, None, None, None, None, 89.8, 83.1, 60.4, 37.9]
ys["Vantage"]=[92.3, 84.7, 59.3, 82.2, 70.0, 81.4, 78.4, 67.7, 82.1, 60.6, 83.1, 75.4, 56.3, 38.3]
ys["Velva"]=[90.0, 94.7, 71.9, 86.3, 70.5, 92.6, None, None, None, None, 96.0, 85.7, 66.2, 46.2]
ys["Vesper"]=[None, None, None, 87.5, 81.8, None, None, None, None, None, None, None, None, None]
ys["Vida"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, 46.7]
ys["WB-Digger"]=[94.8, 98.1, 74.8, 95.2, 80.1, 90.3, 94.3, 74.8, 88.0, 65.2, 96.0, 92.5, 68.8, 42.9]
ys["WB-Gunnison"]=[None, None, None, None, None, None, None, None, None, None, 86.4, 73.4, 60.2, 40.4]
ys["WB-Mayville"]=[77.9, 80.1, 63.6, 76.6, 80.8, 81.4, 86.2, 63.6, 77.2, 65.9, 93.2, 79.7, 66.6, 40.4]
ys["WB9507"]=[104.8, 103.2, 84.3, None, None, 86.8, 104.1, 77.9, 91.8, 93.2, 89.0, 92.8, 73.4, 45.0]
ys["WB9879CLP"]=[None, None, None, None, None, None, None, None, None, None, 90.8, 83.4, 56.9, 38.0]

tws = {}
tws["Advance"]=[61.0, 61.3, 53.3, 63.4, 62.1, 62.6, 60.9, 62.0, 61.9, 58.6, 57.5, 61.5, 62.4, 59.8]
tws["Agawam"]=[None, None, None, 62.6, 61.9, None, None, None, None, None, None, None, None, 61.7]
tws["Alpine"]=[57.9, 57.0, None, 61.0, 60.8, 61.1, None, None, None, None, 55.9, None, 60.0, 60.2]
tws["Alsen"]=[60.5, None, None, 63.6, 62.1, None, None, None, None, None, None, None, None, 60.1]
tws["Barlow"]=[60.9, 59.9, 50.0, 62.4, 61.9, 62.9, 61.4, 61.4, 62.2, 59.9, 57.4, 60.9, 61.1, 60.5]
tws["Breaker"]=[60.9, None, None, 63.9, 63.4, 62.7, None, None, None, None, 58.8, 61.5, 64.4, 61.5]
tws["Brennan"]=[60.3, 60.8, 54.6, 62.2, 61.4, 62.5, None, None, None, None, 55.9, 60.0, 59.7, 61.3]
tws["Brick"]=[60.8, 61.8, 55.9, None, None, 62.6, None, None, None, None, None, None, None, None]
tws["Briggs"]=[59.7, 59.4, 54.2, 62.1, 61.5, None, None, None, None, None, None, None, 60.0, 59.9]
tws["Cardale"]=[None, None, None, None, None, 61.4, None, None, None, None, None, None, None, None]
tws["Choteau"]=[None, None, None, 62.1, 60.7, None, None, None, None, None, None, None, 57.2, 59.6]
tws["Dapps"]=[None, None, None, 62.4, 61.2, None, None, None, None, None, None, None, None, 57.9]
tws["Duclair"]=[58.7, None, None, 61.5, 61.0, None, None, None, None, None, 54.6, None, 59.0, 58.2]
tws["Elgin"]=[60.4, 60.7, 53.7, 62.7, 61.7, 62.3, 60.5, 61.3, 61.4, 58.0, 55.8, 60.8, 60.8, 59.1]
tws["Faller"]=[61.3, 62.1, 54.0, 63.2, 62.2, 62.0, 60.7, 61.7, 61.4, 58.6, 55.9, 61.1, 62.7, 58.4]
tws["Forefront"]=[60.4, 62.2, 56.6, 63.1, 62.0, 62.1, 60.9, 61.0, 61.4, 59.0, 57.1, 61.2, 60.6, 61.0]
tws["Freyr"]=[60.0, 60.5, None, 62.3, 61.0, None, None, None, None, None, None, None, 60.0, 60.5]
tws["Glenn"]=[62.8, 58.8, 52.8, 64.2, 63.7, 64.0, None, None, None, None, 55.2, 62.4, 61.2, 62.3]
tws["Howard"]=[61.6, None, None, 63.3, 62.8, None, None, None, None, None, 55.4, 61.5, 61.8, 59.4]
tws["HRS 3361"]=[60.9, None, None, None, None, 61.3, 60.0, 60.6, 60.6, 58.1, 55.9, 60.1, 60.7, 59.2]
tws["HRS 3378"]=[60.7, None, None, None, None, 62.7, 60.9, 61.8, 62.2, 58.1, 56.9, 60.9, 62.8, 61.0]
tws["HRS 3419"]=[60.4, None, None, None, None, 60.0, 59.3, 59.6, 59.9, 57.7, 54.9, 60.2, 60.5, 57.3]
tws["Jenna"]=[59.7, 59.9, 53.3, 62.5, 60.3, 61.4, 60.1, 60.3, 60.8, 57.2, 56.2, 60.0, 61.9, 59.1]
tws["Kelby"]=[60.2, 60.6, 54.4, 62.5, 61.5, None, None, None, None, None, 56.8, None, 60.4, 61.4]
tws["Albany"]=[61.1, 61.8, 52.9, 63.3, 60.8, 61.9, 59.8, 61.5, 61.0, 57.7, 55.9, 59.1, 62.6, 58.8]
tws["Breakaway"]=[61.2, 61.3, 53.8, 63.3, 63.0, 62.9, 62.7, 62.8, 62.9, 60.4, 58.0, 62.2, 63.7, 61.5]
tws["Iguacu"]=[60.8, 61.2, 54.5, 63.2, 61.8, 62.0, 61.1, 61.8, 61.6, 58.7, 54.6, 59.8, 61.2, 60.8]
tws["Nitro"]=[60.6, 61.2, 52.7, None, None, 61.5, 59.8, 60.0, 60.9, 57.0, 55.0, None, None, None]
tws["Powerplay"]=[61.3, 61.4, 54.3, 62.7, 62.9, 62.4, 61.6, 62.3, 62.0, 59.5, 56.5, 60.8, 61.4, 60.5]
tws["Pro"]=[None, None, None, None, None, None, None, None, None, None, 56.6, None, None, None]
tws["Linkert"]=[60.6, 60.2, 53.2, 63.1, 61.7, 62.2, 60.6, 60.9, 61.4, 57.9, 57.0, 60.8, 59.7, 59.6]
tws["Mott"]=[61.0, None, 53.5, 63.0, 61.2, None, None, None, None, None, 57.0, 60.8, 61.1, 60.4]
tws["Chevelle"]=[59.7, 60.5, 52.5, 61.3, 61.0, 62.1, None, None, None, None, None, 60.2, 59.7, None]
tws["Stingray"]=[59.9, 60.6, 51.2, 61.6, 59.7, 60.1, None, None, None, None, 54.4, 58.7, 62.3, None]
tws["ND 901CL Plus"]=[60.4, None, None, 62.5, 61.2, None, None, None, None, None, 55.9, 60.0, 60.4, 60.5]
tws["Norden"]=[61.8, 61.4, None, 64.0, 63.0, 63.2, 63.0, 63.2, 63.0, 60.7, 58.1, 62.3, 63.7, 61.0]
tws["Prevail"]=[60.1, 61.5, 54.5, 62.3, 61.7, 61.9, 60.5, 61.2, 60.8, 58.5, 56.0, 61.0, 61.1, 59.5]
tws["Prosper"]=[61.0, 61.6, 55.0, 62.0, 62.2, 62.4, 60.5, 61.9, 61.5, 58.3, 56.4, 60.7, 63.1, 58.1]
tws["RB07"]=[60.4, None, None, 63.0, 60.7, 62.1, 60.8, 60.7, 61.3, 57.9, 50.6, 60.1, 59.9, 61.1]
tws["Reeder"]=[None, None, None, 63.2, 61.8, None, None, None, None, None, None, None, None, 59.8]
tws["Rollag"]=[61.7, 61.7, 55.1, 63.5, 62.6, 63.0, 61.7, 62.3, 62.3, 59.9, 57.5, 61.6, 61.5, 60.4]
tws["Sabin"]=[None, None, None, None, None, None, None, None, None, None, None, 60.3, None, 59.7]
tws["Samson"]=[56.9, 59.7, 53.4, 61.1, 61.2, 60.9, 60.4, 60.0, 61.1, 57.2, 54.0, 59.2, 59.4, 59.7]
tws["Select"]=[61.3, 61.8, 55.6, 63.2, 62.7, 62.6, None, None, None, None, 58.5, 62.7, 59.9, 60.5]
tws["Shaw"]=[None, None, None, 63.0, 61.1, None, None, None, None, None, None, None, None, None]
tws["Steele-ND"]=[60.7, 60.0, 54.7, 62.4, 62.7, None, None, None, None, None, 58.2, 61.3, 61.4, 59.7]
tws["SY Ingmar"]=[60.8, 60.9, 53.9, 63.0, 61.7, 62.9, 61.5, 62.2, 61.9, 59.1, 56.9, 61.3, 62.4, 60.7]
tws["SY Rowyn"]=[60.2, 61.8, 53.9, 63.0, 62.2, 62.2, 61.3, 61.4, 61.5, 59.2, 57.0, 60.3, 60.6, 59.6]
tws["SY Soren"]=[60.9, 61.1, 54.7, 62.6, 61.6, 63.2, 60.9, 61.3, 61.5, 58.8, 57.0, 61.3, 61.7, 60.0]
tws["SY Tyra"]=[59.6, None, 51.8, 61.2, 61.1, None, None, None, None, None, 56.2, 60.4, 60.6, 61.5]
tws["SY605 CL"]=[60.9, None, 53.9, 63.1, 61.8, None, None, None, None, None, 55.1, 62.0, 59.0, 60.1]
tws["Vantage"]=[62.4, 61.5, 56.1, 64.4, 62.8, 63.5, 62.2, 62.6, 63.2, 59.5, 56.2, 61.1, 63.3, 61.1]
tws["Velva"]=[58.9, 56.2, 51.7, 62.6, 60.2, 61.2, None, None, None, None, 55.2, 59.2, 59.6, 59.5]
tws["Vesper"]=[58.9, 56.2, 51.7, 62.6, 60.2, 61.2, None, None, None, None, 55.2, 59.2, 59.6, 59.5]
tws["Vida"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, 59.6]
tws["WB-Digger"]=[60.5, 59.2, 52.3, 61.6, 60.3, 61.9, 59.6, 60.4, 61.0, 56.3, 56.8, 59.9, 61.8, 59.0]
tws["WB-Gunnison"]=[None, None, None, None, None, None, None, None, None, None, 57.7, 60.0, 62.5, 60.1]
tws["WB-Mayville"]=[58.4, 58.2, 52.0, 61.0, 61.6, 61.4, 61.0, 61.2, 61.4, 58.0, 55.5, 59.6, 61.1, 60.8]
tws["WB9507"]=[59.0, 60.9, 53.7, None, None, 60.4, 60.0, 60.3, 60.6, 58.5, 54.1, 58.7, 59.9, 57.4]
tws["WB9879CLP"]=[None, None, None, None, None, None, None, None, None, None, 52.2, 59.5, 57.2, 60.5]

ps = {}
ps["Advance"]=[14.0, 13.7, 14.3, 13.2, 14.5, 12.6, 13.7, 13.6, 12.6, 14.1, 11.7, 12.7, 12.4, 14.8]
ps["Agawam"]=[None, None, None, 13.1, 14.2, None, None, None, None, None, None, None, None, 13.2]
ps["Alpine"]=[14.9, 14.5, None, 13.5, 14.2, 12.9, None, None, None, None, 12.6, None, 12.8, 13.9]
ps["Alsen"]=[15.0, None, None, 14.4, 15.0, None, None, None, None, None, None, None, None, 15.4]
ps["Barlow"]=[14.6, 15.2, 14.6, 13.5, 14.8, 13.9, 14.7, 14.3, 13.1, 15.1, 12.5, 13.8, 14.4, 15.5]
ps["Breaker"]=[14.4, None, None, 13.3, 14.6, 13.0, None, None, None, None, 11.8, 13.2, 13.5, 14.8]
ps["Brennan"]=[14.4, 15.2, 14.7, 14.3, 14.3, 13.8, None, None, None, None, 12.5, 12.5, 14.7, 15.5]
ps["Brick"]=[14.3, 15.1, 14.9, None, None, 13.4, None, None, None, None, None, None, None, None]
ps["Briggs"]=[15.2, 15.5, 14.9, 13.8, 15.0, None, None, None, None, None, None, None, 14.4, 15.4]
ps["Cardale"]=[None, None, None, None, None, 13.8, None, None, None, None, None, None, None, None]
ps["Choteau"]=[None, None, None, 13.4, 14.0, None, None, None, None, None, None, None, 13.6, 15.9]
ps["Dapps"]=[None, None, None, 14.8, 15.4, None, None, None, None, None, None, None, None, 16.9]
ps["Duclair"]=[14.3, None, None, 13.5, 14.9, None, None, None, None, None, 12.1, None, 14.0, 14.5]
ps["Elgin"]=[14.8, 14.8, 14.7, 13.6, 14.3, 13.7, 14.5, 14.5, 12.2, 14.9, 12.7, 13.4, 13.9, 15.4]
ps["Faller"]=[14.3, 13.9, 14.2, 12.2, 13.8, 12.3, 14.1, 13.8, 11.8, 14.1, 11.9, 11.9, 12.7, 14.5]
ps["Forefront"]=[14.7, 15.4, 14.7, 14.1, 14.4, 13.8, 14.7, 15.1, 13.4, 14.9, 12.7, 13.2, 13.5, 14.4]
ps["Freyr"]=[14.7, 14.7, None, 13.6, 14.7, None, None, None, None, None, None, None, 13.8, 14.5]
ps["Glenn"]=[15.3, 15.6, 15.4, 14.0, 14.5, 14.4, None, None, None, None, 11.7, 14.5, 14.6, 15.3]
ps["Howard"]=[14.6, None, None, 13.3, 14.6, None, None, None, None, None, 12.7, 12.9, 14.4, 14.7]
ps["HRS 3361"]=[14.3, None, None, None, None, 13.5, 13.9, 14.3, 12.2, 13.9, 11.7, 11.7, 13.8, 15.1]
ps["HRS 3378"]=[13.5, None, None, None, None, 12.4, 13.3, 13.4, 12.1, 13.3, 11.6, 12.1, 13.1, 14.3]
ps["HRS 3419"]=[13.5, None, None, None, None, 12.3, 13.4, 12.2, 11.3, 13.7, 11.6, 11.8, 11.5, 14.2]
ps["Jenna"]=[14.6, 14.5, 14.6, 13.5, 14.7, 12.7, 14.4, 14.7, 13.0, 14.9, 12.2, 13.0, 14.3, 14.3]
ps["Kelby"]=[14.4, 15.4, 15.0, 14.4, 14.9, None, None, None, None, None, 13.8, None, 13.7, 15.3]
ps["Albany"]=[13.6, 13.7, 14.2, 12.3, 13.5, 11.7, 13.6, 12.1, 11.0, 14.3, 11.4, 12.2, 12.1, 14.4]
ps["Breakaway"]=[15.0, 15.9, 15.2, 13.9, 14.8, 13.7, 14.8, 15.3, 13.1, 14.9, 12.3, 13.5, 14.5, 15.2]
ps["Iguacu"]=[12.5, 12.6, 13.1, 12.3, 13.3, 11.6, 11.4, 11.9, 10.9, 11.7, 10.6, 11.1, 12.0, 14.1]
ps["Nitro"]=[13.0, 12.2, 13.0, None, None, 11.8, 12.4, 12.2, 10.9, 12.9, 10.9, None, None, None]
ps["Powerplay"]=[14.2, 14.5, 14.5, 12.8, 13.9, 13.4, 14.5, 13.6, 12.0, 14.8, 12.4, 12.4, 13.9, 14.8]
ps["Pro"]=[None, None, None, None, None, None, None, None, None, None, 11.7, None, None, None]
ps["Linkert"]=[14.8, 15.8, 15.3, 14.7, 15.2, 13.6, 15.0, 15.5, 13.9, 15.1, 13.7, 14.2, 14.3, 15.8]
ps["Mott"]=[15.1, None, 15.7, 13.5, 14.8, None, None, None, None, None, 12.5, 12.9, 13.6, 15.3]
ps["Chevelle"]=[13.2, 13.3, 13.6, 13.1, 13.7, 12.5, None, None, None, None, None, 10.7, 12.7, None]
ps["Stingray"]=[12.2, 11.4, 12.2, 11.3, 12.7, 10.7, None, None, None, None, 11.0, 10.5, 10.9, None]
ps["ND 901CL Plus"]=[16.6, None, None, 14.8, 15.5, None, None, None, None, None, 13.0, 14.9, 14.6, 16.9]
ps["Norden"]=[13.9, 13.9, None, 13.2, 14.3, 13.2, 13.8, 13.7, 12.7, 14.3, 12.1, 12.5, 13.4, 14.5]
ps["Prevail"]=[14.1, 14.5, 14.4, 13.0, 14.4, 13.3, 14.5, 13.8, 13.2, 14.0, 12.9, 12.2, 13.8, 14.5]
ps["Prosper"]=[14.2, 13.8, 14.3, 12.1, 13.8, 12.4, 13.9, 13.7, 12.1, 14.3, 11.5, 11.7, 13.1, 15.3]
ps["RB07"]=[14.8, None, None, 13.5, 14.5, 13.8, 14.7, 14.7, 12.9, 14.6, 13.1, 13.3, 13.4, 15.0]
ps["Reeder"]=[None, None, None, 13.1, 15.1, None, None, None, None, None, None, None, None, 14.6]
ps["Rollag"]=[15.2, 15.4, 16.0, 13.9, 15.2, 14.1, 14.8, 14.9, 13.4, 15.4, 13.2, 13.7, 14.0, 15.4]
ps["Sabin"]=[None, None, None, None, None, None, None, None, None, None, None, 13.8, None, 14.3]
ps["Samson"]=[13.6, 13.9, 14.2, 13.4, 14.2, 12.5, 14.0, 13.8, 12.0, 14.0, 11.9, 11.8, 13.0, 14.5]
ps["Select"]=[14.7, 15.0, 15.3, 13.2, 14.0, 13.7, None, None, None, None, 12.3, 12.7, 13.3, 14.7]
ps["Shaw"]=[None, None, None, 13.8, 15.4, None, None, None, None, None, None, None, None, None]
ps["Steele-ND"]=[14.6, 15.7, 15.0, 13.5, 14.2, None, None, None, None, None, 12.7, 13.6, 14.2, 14.8]
ps["SY Ingmar"]=[14.8, 15.9, 15.2, 13.9, 15.2, 13.7, 14.9, 15.2, 13.2, 15.0, 12.7, 13.2, 14.1, 15.1]
ps["SY Rowyn"]=[13.9, 14.4, 14.7, 13.1, 13.7, 12.9, 13.8, 14.4, 12.0, 14.3, 12.7, 12.0, 12.9, 14.0]
ps["SY Soren"]=[14.7, 15.4, 14.9, 13.9, 14.9, 13.4, 14.3, 15.0, 13.6, 14.5, 12.4, 13.4, 13.6, 15.5]
ps["SY Tyra"]=[13.7, None, 13.8, 12.5, 14.1, None, None, None, None, None, 11.9, 11.8, 13.2, 14.3]
ps["SY605 CL"]=[15.8, None, 15.6, 13.7, 14.9, None, None, None, None, None, 13.2, 14.1, 13.3, 15.6]
ps["Vantage"]=[16.6, 15.8, 16.3, 15.1, 15.5, 14.4, 16.6, 15.3, 14.4, 17.2, 13.1, 14.9, 14.4, 16.1]
ps["Velva"]=[14.8, 14.5, 14.7, 12.9, 15.1, 12.5, None, None, None, None, 12.3, 13.0, 13.8, 14.9]
ps["Vesper"]=[None, None, None, 14.4, 14.8, None, None, None, None, None, None, None, None, None]
ps["Vida"]=[None, None, None, None, None, None, None, None, None, None, None, None, None, 14.3]
ps["WB-Digger"]=[15.1, 14.5, 14.6, 13.3, 14.2, 12.8, 14.2, 14.0, 12.2, 14.6, 10.9, 12.7, 13.5, 14.5]
ps["WB-Gunnison"]=[None, None, None, None, None, None, None, None, None, None, 11.4, 12.6, 13.0, 14.3]
ps["WB-Mayville"]=[14.8, 15.2, 15.1, 14.1, 14.3, 13.6, 14.4, 14.2, 13.3, 14.8, 12.0, 13.2, 14.1, 14.8]
ps["WB9507"]=[14.8, 14.8, 14.9, None, None, 13.1, 14.6, 15.0, 11.7, 14.6, 11.8, 12.2, 13.2, 15.4]
ps["WB9879CLP"]=[None, None, None, None, None, None, None, None, None, None, 12.8, 12.3, 12.4, 15.1]

plant, harvest =  models.Date.objects.filter(date__year=2014)

for v in ys:
 for i in range(len(ls)):
  y = ys[v][i]
  if y is None:
   continue
  l, lsd10, lsd5 = ls[i]
  if l == "Carrington":
   tags = "dryland"
  else:
   tags = None
  tw = tws[v][i]
  p = ps[v][i]
  t = models.Trial_Entry(bushels_acre=y, plant_date=plant, harvest_date=harvest, location=models.Location.objects.filter(name=l)[0], variety=models.Variety.objects.filter(name=v)[0], hidden=False)
  if tw is not None:
   t.test_weight = tw
  if p is not None:
   t.protein_percent = p
  if tags is not None:
   t.planting_method_tags = tags
  if lsd10 is not None:
   t.lsd_10 = lsd10
  if lsd5 is not None: 
   t.lsd_05 = lsd5
  t.save()
 
