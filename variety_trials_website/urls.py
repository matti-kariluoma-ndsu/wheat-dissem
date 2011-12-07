from django.conf.urls.defaults import *
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import list_detail
from django.conf import settings
from variety_trials_data.models import *
from variety_trials_data import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
"""
variety_dictionary = {
      # queries for all Variety Rows in the DB
    "queryset" : Variety.objects.all(),
      # sets which template we'd like to use
    "template_name" : "variety_list.html",
      # changes the variable passed to the template from 'object_list' to 'variety_list'
    "template_object_name" : "variety",
      # sends along additional information, notice the lack of '()'
    "extra_context" : {"entry_list" : Trial_Entry.objects.all}
}
"""

urlpatterns = patterns('',
    # Example:
    # (r'^variety_trials_website/', include('variety_trials_website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', views.index), # the default view
    (r'^(?P<abtest>[1234567890]+)/', views.index),
    #(r'^location/', views.select_location),
    (r'^variety/', views.select_variety),
    #(r'^variety_all/', list_detail.object_list, variety_dictionary),
    #(r'^location/'),
    (r'^view/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[1234567890]+)', views.zipcode_view),
    (r'^view/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)', views.zipcode_view),
    (r'^view/location/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[1234567890]+)', views.locations_view),
    (r'^view/location/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)', views.locations_view),
    (r'^view/variety/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/', views.varieties_view),
    (r'^view/variety/(?P<yearname>[1234567890]+)/(?P<fieldname>[a-z_]+)/(?P<abtest>[1234567890]+)', views.varieties_view),
    (r'^add_variety/', views.add_variety),
    (r'^add_trial/', views.add_trial_entry),
    (r'^add_trials/', views.add_trial_entry_csv_file),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_URL})
)


#urlpatterns += staticfiles_urlpatterns()
