# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('variety_trials_data', '0003_auto_20160530_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiseaseEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('susceptibility', models.DecimalField(help_text=b'Format: 5.00, Percentage of susceptibility of this variety to this disease.', max_digits=8, decimal_places=5)),
                ('disease', models.ForeignKey(help_text=b'Name of disease', to='variety_trials_data.Disease')),
            ],
        ),
        migrations.CreateModel(
            name='PlantingMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('planting_methods', models.CharField(help_text=b'comma separated keywords', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='SignificanceEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comparing', models.CharField(help_text=b'Field in TrialEntry this LSD compares (one of bushels_acre, protein_percent, test_weight)', max_length=200)),
                ('method', models.CharField(help_text=b'Method of comparison, one of LSD, HSD, Mean, CV', max_length=16)),
                ('alpha', models.DecimalField(help_text=b'Significance level of reported value', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('value', models.DecimalField(help_text=b'Value to compare other TrialEntries against', max_digits=10, decimal_places=5)),
            ],
        ),
        migrations.RemoveField(
            model_name='disease_entry',
            name='disease',
        ),
        migrations.RemoveField(
            model_name='disease_entry',
            name='variety',
        ),
        migrations.AlterField(
            model_name='trialentry',
            name='bushels_acre',
            field=models.DecimalField(help_text=b'Format: 37.4, Bushels per Acre', null=True, max_digits=10, decimal_places=5, blank=True),
        ),
        migrations.AlterField(
            model_name='trialentry',
            name='harvest_date',
            field=models.ForeignKey(related_name='harvest_date', on_delete=django.db.models.deletion.DO_NOTHING, to='variety_trials_data.Date', help_text=b'Date this trial was harvested'),
        ),
        migrations.AlterField(
            model_name='trialentry',
            name='hidden',
            field=models.BooleanField(default=False, help_text=b'Should we hide this trial from the public-facing website?'),
        ),
        migrations.AlterField(
            model_name='trialentry',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='variety_trials_data.Location', help_text=b'Name of location'),
        ),
        migrations.AlterField(
            model_name='trialentry',
            name='plant_date',
            field=models.ForeignKey(related_name='plant_date', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='variety_trials_data.Date', help_text=b'Date this trial was planted', null=True),
        ),
        migrations.AlterField(
            model_name='trialentry',
            name='planting_method_tags',
            field=models.ForeignKey(related_name='planting_method_tags', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='variety_trials_data.PlantingMethod', help_text=b'Comma-separated list of planting methods', null=True),
        ),
        migrations.AlterField(
            model_name='trialentry',
            name='shatter',
            field=models.DecimalField(help_text=b'Format: 4, Ranking: 1 (Least Shatter) to 9 (Most Shatter)', null=True, max_digits=8, decimal_places=5, blank=True),
        ),
        migrations.AlterField(
            model_name='trialentry',
            name='variety',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='variety_trials_data.Variety', help_text=b'Name of variety'),
        ),
        migrations.AlterField(
            model_name='variety',
            name='beard',
            field=models.CharField(help_text=b'Color(?) of beard.', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='variety',
            name='diseases',
            field=models.ManyToManyField(to='variety_trials_data.Disease', through='variety_trials_data.DiseaseEntry'),
        ),
        migrations.DeleteModel(
            name='Disease_Entry',
        ),
        migrations.AddField(
            model_name='significanceentry',
            name='trials',
            field=models.ManyToManyField(to='variety_trials_data.TrialEntry'),
        ),
        migrations.AddField(
            model_name='diseaseentry',
            name='variety',
            field=models.ForeignKey(help_text=b'Name of variety', to='variety_trials_data.Variety'),
        ),
    ]
