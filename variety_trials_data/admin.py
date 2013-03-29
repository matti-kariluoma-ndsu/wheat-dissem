#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2012 Matti Kariluoma <matti.m.kariluoma@ndsu.edu>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

import models
from django.contrib import admin

admin.site.register(models.Disease)
admin.site.register(models.Variety)
admin.site.register(models.Location)
admin.site.register(models.Date)
admin.site.register(models.Trial_Entry)
admin.site.register(models.Disease_Entry)
