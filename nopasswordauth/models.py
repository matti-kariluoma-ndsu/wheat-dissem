#!/usr/bin/env python
# coding: ascii

"""
thanks https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#specifying-a-custom-user-model
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""


from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import re

class NoPasswordUserManager(BaseUserManager):
	def create_user(self, email):
		if email is None:
			raise ValueError('Users must have an email address')
		email = self.normalize_email(email) # lowercases domain
		if not self.model.email_re.match(email):
			raise ValueError('Email address must only contain alphanumeric and the _@\.- characters.')
		user = self.model(email=email)
		user.set_unusable_password()
		user.save(using=self._db)
		return user
	def create_superuser(self, email, password):
		del password # we don't use passwords, but the api forces one
		user = self.create_user(email)
		user.is_superuser = True
		user.save(using=self._db)
		return user

class NoPasswordUser(AbstractBaseUser):
	# this requirement is enforced by the nopassword app when the user 
	# tries to login... I guess its to only allow email addresses that
	# can be printed as urls? In any case, its out of our control.
	email_re = re.compile('^[a-zA-Z0-9_@\\.-]+$')
	email = models.EmailField(
			verbose_name='email address',
			max_length=256,
			unique=True,
		)
	is_superuser = models.BooleanField(default=False)
	objects = NoPasswordUserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	class Meta:
		verbose_name = 'System user'
		verbose_name_plural = 'System users'

	def get_full_name(self):
		return self.email
	def get_short_name(self):
		return self.email
	def __str__(self):
		return self.email
	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True
	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True
	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_superuser

