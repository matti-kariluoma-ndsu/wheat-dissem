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
    # (r'^variety_trials_website/', include('variety_trials_website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    
    (r'^$', views.index), # the home page
    ## TODO: There are 3 views of our data, reduce to 2 if not 1.
    (r'^view/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)', views.zipcode_view), # defaults to location-based view
    (r'^view/location/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)', views.locations_view), # view based on variety head-to-head comparison
    (r'^view/variety/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/', views.varieties_view), # view based on proximity
    #(r'^(?P<abtest>[1234567890]+)/', views.index),
    #(r'^view/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[1234567890]+)', views.zipcode_view),
    #(r'^view/location/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[1234567890]+)', views.locations_view),
    #(r'^view/variety/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[1234567890]+)', views.varieties_view),
    (r'^add_trials/', views.add_trial_entry_csv_file), # page to upload a spreadsheet to
    (r'^view/info/(?P<variety_name>[a-zA-Z_]+)', views.variety_info), # defaults to location-based view
	(r'^view/history/', views.history), # defaults to location-based view
	(r'^view/delete/(?P<delete>[1234567890]+)', views.history_delete), # defaults to location-based view
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}) # serves static/img static/css static/js etc.
                       
)

