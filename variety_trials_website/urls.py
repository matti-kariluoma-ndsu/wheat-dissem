#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.conf import settings
from variety_trials_data.models import *
from variety_trials_data import views
from variety_trials_data import json_views
from variety_trials_data import adding_data_views

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
		# Example:
		# (r'^variety_trials_website/', include('variety_trials_website.foo.urls'))
		
		# Uncomment the next line to enable the admin:
		#(r'^admin/', include(admin.site.urls)),
		#(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}), # serves static/img static/css static/js etc.
		
		#(r'^debug', views.debug),
		
		(r'^$', views.index), # the home page
		
		(r'^about/', views.about),
		
		(r'^view/$', views.advanced_search),
		(r'^view/last_(?P<year_range>[0-9]+)_years/(?P<fieldname>[a-z0-9_]+)/', views.zipcode_view), # defaults to location-based view
		(r'^view/(?P<startyear>[0-9]+)/(?P<fieldname>[a-z0-9_]+)/', views.historical_zipcode_view), # defaults to location-based view
		(r'^view/variety/(?P<variety_name>[a-zA-Z_]+)/', views.variety_info),
		(r'^view/available/', views.inspect),
		
		(r'^data/$', views.howto_api),
		(r'^data/trial_entry/id_(?P<id>[0-9]+)/json/', json_views.trial_entry_json),
		(r'^data/trial_entry/near_zipcode_(?P<zipcode>[0-9]+)/last_3_years/json/', json_views.trial_entry_near_json),
		(r'^data/trial_entry/near_zipcode_(?P<zipcode>[0-9]+)/last_3_years/ids/json/', json_views.trial_entry_near_ids_json),
		(r'^data/zipcode/id_(?P<id>[0-9]+)/json/', json_views.zipcode_json),
		(r'^data/zipcode/partial_zipcode_(?P<partial_zipcode>[0-9]+)/json/', json_views.autocomplete_zipcode_json),
		(r'^data/location/id_(?P<id>[0-9]+)/json/', json_views.location_json),
		(r'^data/location/all/json/', json_views.location_json_all),
		(r'^data/location/near_zipcode_(?P<zipcode>[0-9]+)/json/', json_views.zipcode_near_json),
		(r'^data/variety/all/json/', json_views.variety_json_all),
		(r'^data/variety/id_(?P<id>[0-9]+)/json/', json_views.variety_json),
		(r'^data/disease/id_(?P<id>[0-9]+)/json/', json_views.disease_json),
		
		(r'^add/$', views.howto_add_data),
		(r'^add/trial_entries/$', adding_data_views.add_trial_entry_csv_file), # page to upload a spreadsheet to
		(r'^add/trial_entries/confirm/', adding_data_views.add_trial_entry_csv_file_confirm), # page to upload a spreadsheet to
		(r'^add/trial_entry/', adding_data_views.add_trial_entry),
		(r'^add/date/', adding_data_views.add_date),
		(r'^add/location/', adding_data_views.add_location),
		(r'^add/variety/', adding_data_views.add_variety), 
		(r'^add/history/', adding_data_views.history), # defaults to location-based view
		(r'^add/history/delete/(?P<delete>[0-9]+)/', adding_data_views.history_delete), # defaults to location-based view
		
		(r'^survey/$', views.planting_method_survey), 
		(r'^survey/results/', views.planting_method_view_survey), 
)

