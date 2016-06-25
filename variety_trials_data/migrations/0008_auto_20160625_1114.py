# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variety_trials_data', '0007_populate_sig_entry_planting_methods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trialentry',
            name='hsd_10',
        ),
        migrations.RemoveField(
            model_name='trialentry',
            name='lsd_05',
        ),
        migrations.RemoveField(
            model_name='trialentry',
            name='lsd_10',
        ),
        migrations.RemoveField(
            model_name='trialentry',
            name='planting_method_tags',
        ),
    ]
