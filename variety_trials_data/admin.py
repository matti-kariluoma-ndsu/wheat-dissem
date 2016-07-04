#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from django.contrib import admin
from django import forms
from . import models
# separate admin site from default (default being used for user creation)
class UserAdminSite(admin.sites.AdminSite):
	def has_permission(self, request):
		# any logged-in user can access this admin
		return request.user.is_active

hrsw_admin_site = UserAdminSite(name='hrsw-admin')

# customized (sorted) view of TrialEntry (for when we edit a SignificanceEntry)
class SignificanceEntryForm(forms.ModelForm):
	trials = forms.ModelMultipleChoiceField(
			queryset = models.TrialEntry.objects.order_by(
					'harvest_date__date',
					'location',
					'planting_method_tags',
					'variety',
				),
			widget = forms.SelectMultiple(
					attrs = {'style': 'height: 200px'}
				),
		)
	class Meta:
		model = models.SignificanceEntry
		fields = '__all__'

class SignificanceEntryAdmin(admin.ModelAdmin):
	form = SignificanceEntryForm

# sortable view of trial entries when browsing them all
class TrialEntryAdmin(admin.ModelAdmin):
	list_display = (
			'harvest_date',
			'location',
			'planting_method_tags',
			'variety',
		)

# instead of admin.site (the default instance) use hrsw_admin_site
hrsw_admin_site.register(models.Date)
hrsw_admin_site.register(models.Location)
hrsw_admin_site.register(models.PlantingMethod)
hrsw_admin_site.register(models.SignificanceEntry, SignificanceEntryAdmin)
hrsw_admin_site.register(models.TrialEntry, TrialEntryAdmin)
hrsw_admin_site.register(models.Variety)
