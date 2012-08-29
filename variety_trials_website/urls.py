from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.conf import settings
from variety_trials_data.models import *
from variety_trials_data import views
from variety_trials_data import json_views

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
		
		(r'^about/', views.index),
		
		(r'^view/$', views.index),
		(r'^view/last_(?P<year_range>[0-9]+)_years/(?P<fieldname>[a-z0-9_]+)/', views.zipcode_view), # defaults to location-based view
		(r'^view/(?P<startyear>[0-9]+)/(?P<fieldname>[a-z0-9_]+)/', views.historical_zipcode_view), # defaults to location-based view
		(r'^view/variety/(?P<variety_name>[a-zA-Z_]+)/', views.variety_info),
		(r'^view/available/', views.inspect),
		
		(r'^add/$', views.index),
		(r'^add/trial_entry/', views.add_trial_entry_csv_file), # page to upload a spreadsheet to
		(r'^add/variety/', views.add_variety), # page to variety
		
		(r'^add_new_variety/', views.add_new_variety), # page to variety
		(r'^edit_variety/', views.edit_variety), # page to variety
		(r'^edited_variety/', views.edited_variety), # page to variety
		(r'^add_trials_confirm/', views.add_form_confirmation), # Page to confirmations
		(r'^add_info/', views.add_information), # Page to confirmations
		(r'^add_data_variety_or_location/', views.adding_to_database_confirm), # Page to adding to database
		(r'^sucess/', views.redirect_sucess), # Page to sucess
		
		(r'^add/history/', views.history), # defaults to location-based view
		(r'^add/history/delete/(?P<delete>[0-9]+)/', views.history_delete), # defaults to location-based view
		
		(r'^data/$', views.index),
		(r'^data/trial_entry/id_(?P<id>[0-9]+)/json/', json_views.trial_entry_json),
		(r'^data/trial_entry/near_zipcode_(?P<zipcode>[0-9]+)/last_3_years/json/', json_views.trial_entry_json),
		(r'^data/trial_entry/near_zipcode_(?P<zipcode>[0-9]+)/last_3_years/ids/json/', json_views.trial_entry_id_json),
		(r'^data/zipcode/id_(?P<id>[0-9]+)/json/', json_views.zipcode_json),
		(r'^data/zipcode/partial_zipcode_(?P<partial_zipcode>[1234567890]+)/json/', json_views.autocomplete_zipcode_json),
		(r'^data/location/id_(?P<id>[0-9]+)/json/', json_views.location_json),
		(r'^data/location/all/json/', json_views.location_json_all),
		(r'^data/location/near_zipcode_(?P<zipcode>[0-9]+)/json/', json_views.zipcode_near_json),
		(r'^data/variety/all/json/', json_views.variety_json_all),
		(r'^data/variety/id_(?P<id>[0-9]+)/json/', json_views.variety_json),
		(r'^data/disease/id_(?P<id>[0-9]+)/json/', json_views.disease_json),
		
		
)

