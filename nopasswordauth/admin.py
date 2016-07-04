#!/usr/bin/env python
# coding: ascii

"""
thanks https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#specifying-a-custom-user-model
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import NoPasswordUser

class UserCreationForm(forms.ModelForm):
	class Meta:
		model = NoPasswordUser
		fields = ('email',)
	def clean_email(self):
		email = self.cleaned_data['email']
		if not NoPasswordUser.email_re.match(email):
			raise forms.ValidationError('Email must contain alphanumeric and _@\.- characters!')
		return email
	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	class Meta:
		model = NoPasswordUser
		fields = ('email', 'is_superuser')
	def clean_email(self):
		email = self.cleaned_data['email']
		if not NoPasswordUser.email_re.match(email):
			raise forms.ValidationError('Email must contain alphanumeric and _@\.- characters!')
		return email

class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserCreationForm
	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('email', 'is_superuser')
	list_filter = ('is_superuser',)
	fieldsets = (
		(None, {'fields': ('email',)}),
		('Permissions', {'fields': ('is_superuser',)}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email',)}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(NoPasswordUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

