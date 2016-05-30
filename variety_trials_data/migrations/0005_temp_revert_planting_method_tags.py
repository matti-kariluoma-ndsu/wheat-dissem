# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variety_trials_data', '0004_refactor_trial_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trialentry',
            name='planting_method_tags',
            field=models.CharField(help_text=b'Comma-separated list of planting methods', max_length=200, null=True, blank=True),
        ),
    ]
