# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('variety_trials_data', '0005_temp_revert_planting_method_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='trialentry',
            name='planting_method_tags_new',
            field=models.ForeignKey(related_name='planting_method_tags', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='variety_trials_data.PlantingMethod', help_text=b'Comma-separated list of planting methods', null=True),
        ),
    ]
