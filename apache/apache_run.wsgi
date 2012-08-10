import os
import sys

path = '/home/kariluom/repo/wheat-dissem/'
if path not in sys.path:
    sys.path.append(path)

os.chdir("/home/kariluom/repo/wheat-dissem/")

os.environ['DJANGO_SETTINGS_MODULE'] = 'variety_trials_website.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
