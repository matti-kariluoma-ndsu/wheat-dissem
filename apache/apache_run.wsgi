import os
import sys

path = '/home/www/varieties/wheat-dissem/'
if path not in sys.path:
    sys.path.append(path)

path='/home/www/varieties/wheat-dissem/variety_trials_website'
if path not in sys.path:
    sys.path.append(path)

os.chdir("/home/www/varieties/wheat-dissem/variety_trials_website")

os.environ['DJANGO_SETTINGS_MODULE'] = 'variety_trials_website.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
