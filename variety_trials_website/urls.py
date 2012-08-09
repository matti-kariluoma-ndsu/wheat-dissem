from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.conf import settings
from variety_trials_data.models import *
from variety_trials_data import views

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
		# Example:
		# (r'^variety_trials_website/', include('variety_trials_website.foo.urls'))
		
		# Uncomment the next line to enable the admin:
		#(r'^admin/', include(admin.site.urls)),
		
		(r'^$', views.index), # the home page
		## TODO: There are 3 views of our data, reduce to 2 if not 1.
		(r'^view/last_(?P<year_range>[0-9]+)_years/(?P<fieldname>[a-z0-9_]+)/', views.zipcode_view), # defaults to location-based view
		(r'^view/(?P<startyear>[0-9]+)/(?P<fieldname>[a-z0-9_]+)/', views.historical_zipcode_view), # defaults to location-based view
		#(r'^view/location/(?P<startyear>[0-9]+)/(?P<fieldname>[a-z0-9_]+)/', views.locations_view), # view based on variety head-to-head comparison
		#(r'^view/variety/(?P<startyear>[0-9]+)/(?P<fieldname>[a-z0-9_]+)/', views.varieties_view), # view based on proximity
		#(r'^(?P<abtest>[0-9]+)/', views.index),
		#(r'^view/(?P<startyear>[0-9]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[0-9]+)/', views.zipcode_view),
		#(r'^view/location/(?P<startyear>[0-9]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[0-9]+)/', views.locations_view),
		#(r'^view/variety/(?P<startyear>[0-9]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[0-9]+)/', views.varieties_view),
		(r'^add_trials/', views.add_trial_entry_csv_file), # page to upload a spreadsheet to
		(r'^add_trials_confirm/', views.add_form_confirmation), # Page to confirmations
		(r'^sucess/', views.redirect_sucess), # Page to sucess
		(r'^add_info/', views.add_information), # Page to confirmations
		(r'^add_data_variety_or_location/', views.adding_to_database_confirm), # Page to adding to database
		(r'^view/info/(?P<variety_name>[a-zA-Z_]+)/', views.variety_info), # defaults to location-based view
		(r'^view/history/', views.history), # defaults to location-based view
		(r'^view/delete/(?P<delete>[0-9]+)/', views.history_delete), # defaults to location-based view
		#(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}), # serves static/img static/css static/js etc.
		(r'^view/info/(?P<variety_name>[a-zA-Z_]+)', views.variety_info), # defaults to location-based view
		(r'^inspect/', views.inspect),
		(r'^trial_entry/(?P<id>[0-9]+)/json', views.trial_entry_json),
		(r'^zipcode/(?P<id>[0-9]+)/json', views.zipcode_json),
		(r'^zipcode/near/(?P<zipcode>[0-9]+)/json', views.zipcode_near_json),
		(r'^location/(?P<id>[0-9]+)/json', views.location_json),
		(r'^variety/(?P<id>[0-9]+)/json', views.variety_json),
		(r'^(?P<zipcode>[0-9]+)/last_three_years/json', views.trial_entry_id_json),
		(r'^location/all/json', views.location_json_all),
		(r'^variety/all/json', views.variety_json_all),
		(r'^disease/(?P<id>[0-9]+)/json', views.disease_json),
		(r'^debug', views.debug),
)

