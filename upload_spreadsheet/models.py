#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django.db import models
from django.utils import timezone
from django.conf import settings
from nopasswordauth.models import NoPasswordUser as User

class UploadProgress(models.Model):
	'''
	Keeps track of the state of a users uploaded spreadsheet
	'''
	user = models.ForeignKey(
			User,
			on_delete=models.CASCADE,
			help_text='foreign key to the user this token is for'
		)
	path = models.CharField(
			max_length=4096,
			help_text='path the users uploaded spreadsheet has been stored'
		)
	submitted = models.BooleanField(
			default=False, 
			help_text='have we finished processing this spreadsheet?'
		)
	created = models.DateTimeField(
			default=timezone.now, 
			help_text='datetime this request was created'
		)
	
