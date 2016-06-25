# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variety_trials_data', '0008_auto_20160625_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trialentry',
            old_name='planting_method_tags_new',
            new_name='planting_method_tags',
        ),
    ]
