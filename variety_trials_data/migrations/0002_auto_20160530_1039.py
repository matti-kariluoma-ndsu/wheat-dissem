# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variety_trials_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location_year_plantingmethods_survey_answer',
            name='location',
        ),
        migrations.RemoveField(
            model_name='trial_entry_history',
            name='trial_entry',
        ),
        migrations.DeleteModel(
            name='Location_Year_PlantingMethods_Survey_Answer',
        ),
        migrations.DeleteModel(
            name='Trial_Entry_History',
        ),
    ]
