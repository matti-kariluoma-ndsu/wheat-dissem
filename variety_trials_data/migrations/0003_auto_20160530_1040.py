# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variety_trials_data', '0002_auto_20160530_1039'),
    ]

    operations = [
        migrations.RenameModel(
            'Trial_Entry', 'TrialEntry'
        ),
    ]
