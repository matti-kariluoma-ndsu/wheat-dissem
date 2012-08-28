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
		(r'^view/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/', views.zipcode_view), # defaults to location-based view
		(r'^view/location/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/', views.locations_view), # view based on variety head-to-head comparison
		(r'^view/variety/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/', views.varieties_view), # view based on proximity
		#(r'^(?P<abtest>[1234567890]+)/', views.index),
		#(r'^view/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[1234567890]+)/', views.zipcode_view),
		#(r'^view/location/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[1234567890]+)/', views.locations_view),
		#(r'^view/variety/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[1234567890]+)/', views.varieties_view),
		(r'^add_trials/', views.add_trial_entry_csv_file), # page to upload a spreadsheet to
		(r'^add_variety/', views.add_variety), # page to variety
		(r'^add_new_variety/', views.add_new_variety), # page to variety
		(r'^edit_variety/', views.edit_variety), # page to variety
		(r'^edited_variety/', views.edited_variety), # page to variety


		(r'^add_trials_confirm/', views.add_form_confirmation), # Page to confirmations
		(r'^sucess/', views.redirect_sucess), # Page to sucess
		(r'^add_info/', views.add_information), # Page to confirmations
		(r'^add_data_variety_or_location/', views.adding_to_database_confirm), # Page to adding to database
		(r'^view/info/(?P<variety_name>[a-zA-Z_]+)/', views.variety_info), # defaults to location-based view
		(r'^view/history/', views.history), # defaults to location-based view
		(r'^view/delete/(?P<delete>[1234567890]+)/', views.history_delete), # defaults to location-based view
		#(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}), # serves static/img static/css static/js etc.
		(r'^view/info/(?P<variety_name>[a-zA-Z_]+)', views.variety_info), # defaults to location-based view
		(r'^inspect/', views.inspect),
		(r'^trial_entry/(?P<id>[1234567890]+)/json', views.trial_entry_json),
		(r'^zipcode/(?P<id>[1234567890]+)/json', views.zipcode_json),
		(r'^autocomplete/zipcode/(?P<partial_zipcode>[1234567890]+)/json', views.autocomplete_zipcode_json),
		(r'^location/(?P<id>[1234567890]+)/json', views.location_json),
		(r'^location/all/json', views.location_json_all),
		(r'^variety/all/json', views.variety_json_all),
		(r'^disease/(?P<id>[1234567890]+)/json', views.disease_json),
		(r'^debug', views.debug),
)

