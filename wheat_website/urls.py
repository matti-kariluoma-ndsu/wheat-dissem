from django.conf.urls.defaults import *
from django.views.generic import list_detail
from wheat_data.models import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

variety_info = {
      # queries for all Variety Rows in the DB
    "queryset" : Variety.objects.all(),
      # sets which template we'd like to use
    "template_name" : "variety_list.html",
      # changes the variable passed to the template from 'object_list' to 'variety_list'
    "template_object_name" : "variety",
      # sends along additional information, notice the lack of '()'
    "extra_context" : {"entry_list" : Entry.objects.all}
}


urlpatterns = patterns('',
    # Example:
    # (r'^wheat_website/', include('wheat_website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^variety/', list_detail.object_list, variety_info)

)
