#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

def restricted(f):
	return user_passes_test(
			lambda u: u.is_authenticated() and not u.is_superuser,
			login_url=settings.LOGIN_URL,
			redirect_field_name='next'
		)(f)
