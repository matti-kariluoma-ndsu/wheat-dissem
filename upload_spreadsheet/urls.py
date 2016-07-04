#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'^$', views.index),
		url(r'^verify-(?P<pk>[0-9]+)/locations/clean/$', views.clean_locations),
		url(r'^verify-(?P<pk>[0-9]+)/locations/add/planting-methods/$', views.add_planting_methods),
		url(r'^verify-(?P<pk>[0-9]+)/locations/add/$', views.add_locations),
		url(r'^verify-(?P<pk>[0-9]+)/locations/$', views.verify_locations),
		url(r'^verify-(?P<pk>[0-9]+)/varieties/clean/$', views.clean_varieties),
		url(r'^verify-(?P<pk>[0-9]+)/varieties/add/$', views.add_varieties),
		url(r'^verify-(?P<pk>[0-9]+)/varieties/$', views.verify_varieties),
		url(r'^verify-(?P<pk>[0-9]+)/measures/clean/$', views.clean_measures),
		url(r'^verify-(?P<pk>[0-9]+)/measures/$', views.verify_measures),
		url(r'^verify-(?P<pk>[0-9]+)/statistics/clean/$', views.clean_stats),
		url(r'^verify-(?P<pk>[0-9]+)/statistics/add/$', views.add_stats),
		url(r'^verify-(?P<pk>[0-9]+)/statistics/$', views.verify_stats),
		url(r'^verify-(?P<pk>[0-9]+)/preview/$', views.verify_preview),
		url(r'^verify-(?P<pk>[0-9]+)/$', views.verify),
		url(r'^update-(?P<pk>[0-9]+)/$', views.update),
	]
