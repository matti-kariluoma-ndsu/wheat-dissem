#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django.conf.urls import include, url, handler404
from django.conf import settings
from django.contrib import admin
from variety_trials_data.models import *
from variety_trials_data import views
from variety_trials_data import json_views
from nopasswordauth import views as authviews

handler404 = authviews.page_not_found

urlpatterns = [
		url(r'^admin/login/', authviews.login),
		url(r'^admin/', include(admin.site.urls)),
		url(r'^accounts/login/', authviews.login),
		url(r'^accounts/', include('nopassword.urls')),
		url(r'^upload/', include('upload_spreadsheet.urls')),
		
		url(r'^$', views.index), # the home page
		
		url(r'^about/', views.about),
		
		url(r'^view/$', views.advanced_search),
		url(r'^view/last_(?P<year_range>[0-9]+)_years/(?P<fieldname>[a-z0-9_]+)/', views.zipcode_view), # defaults to location-based view
		url(r'^view/(?P<startyear>[0-9]+)/(?P<fieldname>[a-z0-9_]+)/', views.historical_zipcode_view), # defaults to location-based view
		url(r'^view/variety/(?P<variety_name>[a-zA-Z_]+)/', views.variety_info),
		url(r'^view/available/', views.inspect),
		
		url(r'^data/$', views.howto_api),
		url(r'^data/trial_entry/id_(?P<id>[0-9]+)/json/', json_views.trial_entry_json),
		url(r'^data/trial_entry/near_zipcode_(?P<zipcode>[0-9]+)/last_3_years/json/', json_views.trial_entry_near_json),
		url(r'^data/trial_entry/near_zipcode_(?P<zipcode>[0-9]+)/last_3_years/ids/json/', json_views.trial_entry_near_ids_json),
		url(r'^data/zipcode/id_(?P<id>[0-9]+)/json/', json_views.zipcode_json),
		url(r'^data/zipcode/partial_zipcode_(?P<partial_zipcode>[0-9]+)/json/', json_views.autocomplete_zipcode_json),
		url(r'^data/location/id_(?P<id>[0-9]+)/json/', json_views.location_json),
		url(r'^data/location/all/json/', json_views.location_json_all),
		url(r'^data/location/near_zipcode_(?P<zipcode>[0-9]+)/json/', json_views.zipcode_near_json),
		url(r'^data/variety/all/json/', json_views.variety_json_all),
		url(r'^data/variety/id_(?P<id>[0-9]+)/json/', json_views.variety_json),
		url(r'^data/disease/id_(?P<id>[0-9]+)/json/', json_views.disease_json),
]

