from django.conf.urls.defaults import *
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import list_detail
from django.conf import settings
from wheat_data.models import *
from wheat_data import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

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


urlpatterns = patterns('',
    # Example:
    # (r'^wheat_website/', include('wheat_website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', views.select_location), # the default view
    (r'^variety/', list_detail.object_list, variety_dictionary),
    #(r'^location/'),
    (r'^add_variety/', views.add_variety),
    (r'^add_trial/', views.add_trial_entry),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_URL})
)


#urlpatterns += staticfiles_urlpatterns()
