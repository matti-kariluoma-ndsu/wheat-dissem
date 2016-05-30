# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(help_text=b'Format: MM/DD/YYYY')),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Disease_Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('susceptibility', models.DecimalField(help_text=b'Format: 5.00, Percentage of susceptibility of this variety to this disease.', max_digits=8, decimal_places=5)),
                ('disease', models.ForeignKey(help_text=b'Name of disease', to='variety_trials_data.Disease')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'', max_length=200)),
                ('latitude', models.DecimalField(help_text=b'Format: 46.8772, Overrides the latitude value derived from the zipcode. The Equator is 0, south is negative.', null=True, max_digits=13, decimal_places=10, blank=True)),
                ('longitude', models.DecimalField(help_text=b'Format: -96.7894, Overrides the longitude value derived from the zipcode. The Grand Meridian is 0, west is negative.', null=True, max_digits=13, decimal_places=10, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location_Year_PlantingMethods_Survey_Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField()),
                ('irrigated', models.CharField(max_length=32)),
                ('fungicide', models.CharField(max_length=32)),
                ('notes', models.CharField(max_length=2000)),
                ('location', models.ForeignKey(to='variety_trials_data.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Trial_Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bushels_acre', models.DecimalField(help_text=b'Format: 37.4, Bushels per Acre', max_digits=10, decimal_places=5)),
                ('protein_percent', models.DecimalField(help_text=b'Format: 12.1, Percentage of protein per pound', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('test_weight', models.DecimalField(help_text=b'Format: 50.1, Pounds per bushel', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('kernel_weight', models.DecimalField(help_text=b'Format: 30.5, Grams per 1000 kernels', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('plant_height', models.DecimalField(help_text=b'Format: 24.5, Height of plant in inches', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('days_to_head', models.DecimalField(help_text=b'Format: 57, Days from planting to head', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('lodging_factor', models.DecimalField(help_text=b'Format: 4, Ranking: 1 (No Lodging) to 9 (Heavy Lodging)', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('jday_of_head', models.DecimalField(help_text=b'Format: 265, Julian day of head', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('winter_survival_rate', models.DecimalField(help_text=b'Format: 20.5, Percentage that survive winter', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('shatter', models.DecimalField(help_text=b'Format 4, Ranking: 1 (Least Shatter) to 9 (Most Shatter)', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('seeds_per_round', models.DecimalField(help_text=b'Format: 1.2, Number of seeds (in 1000s) per round', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('canopy_density', models.DecimalField(help_text=b'Format 4, Ranking: 1 (Least Dense) to 9 (Most Dense)', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('canopy_height', models.DecimalField(help_text=b'Format: 26.2, Height of canopy in inches', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('days_to_flower', models.DecimalField(help_text=b'Format: 28, Days from planting to flower', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('seed_oil_percent', models.DecimalField(help_text=b'Format: 5.6, Percentage of mass', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('planting_method_tags', models.CharField(help_text=b'Comma-separated list of planting methods', max_length=200, null=True, blank=True)),
                ('seeding_rate', models.DecimalField(help_text=b'Format: 2.1, Number of seeds (in 1000s) per foot', null=True, max_digits=8, decimal_places=5, blank=True)),
                ('previous_crop', models.CharField(help_text=b'Name of the previous crop at this location', max_length=200, null=True, blank=True)),
                ('moisture_basis', models.DecimalField(help_text=b'Format: 3, Ranking: 1 (Dry) to 9 (Flooded)', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('lsd_05', models.DecimalField(help_text=b'Bushels per Acre LSD at a=0.05 (for the entire location in this year)', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('lsd_10', models.DecimalField(help_text=b'Bushels per Acre LSD at a=0.10 (for the entire location in this year)', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('hsd_10', models.DecimalField(help_text=b'Bushels per Acre HSD at a=0.05 (for the entire location in this year)', null=True, max_digits=10, decimal_places=5, blank=True)),
                ('hidden', models.BooleanField(default=True, help_text=b'')),
                ('harvest_date', models.ForeignKey(related_name='harvest_date', to='variety_trials_data.Date', help_text=b'Date this trial was harvested')),
                ('location', models.ForeignKey(help_text=b'Name of location', to='variety_trials_data.Location')),
                ('plant_date', models.ForeignKey(related_name='plant_date', blank=True, to='variety_trials_data.Date', help_text=b'Date this trial was planted', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trial_Entry_History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=200)),
                ('created_date', models.DateField()),
                ('trial_entry', models.ForeignKey(to='variety_trials_data.Trial_Entry', on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
        ),
        migrations.CreateModel(
            name='Variety',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'', max_length=200)),
                ('description_url', models.CharField(help_text=b'A link to a resource that describes this variety.', max_length=200, null=True, blank=True)),
                ('picture_url', models.CharField(help_text=b'A link to a small picture of this variety.', max_length=200, null=True, blank=True)),
                ('agent_origin', models.CharField(help_text=b'The name of the cultivar.', max_length=200, null=True, blank=True)),
                ('year_released', models.CharField(help_text=b'Format: YYYY, The year this variety was released.', max_length=200, null=True, blank=True)),
                ('straw_length', models.CharField(help_text=b'The length of the stems.', max_length=200, null=True, blank=True)),
                ('maturity', models.CharField(help_text=b'Type of maturity(?)', max_length=200, null=True, blank=True)),
                ('grain_color', models.CharField(help_text=b'Color of mature grain.', max_length=200, null=True, blank=True)),
                ('seed_color', models.CharField(help_text=b'Color of seed.', max_length=200, null=True, blank=True)),
                ('beard', models.CharField(help_text=b'Color (?) of beard.', max_length=200, null=True, blank=True)),
                ('wilt', models.CharField(help_text=b'Degree of wilt(?)', max_length=200, null=True, blank=True)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zipcode', models.PositiveIntegerField()),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=2)),
                ('latitude', models.DecimalField(max_digits=13, decimal_places=10)),
                ('longitude', models.DecimalField(max_digits=13, decimal_places=10)),
                ('timezone', models.SmallIntegerField()),
                ('daylight_savings', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VarietyManager',
            fields=[
                ('variety_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='variety_trials_data.Variety')),
            ],
            bases=('variety_trials_data.variety',),
        ),
        migrations.AddField(
            model_name='variety',
            name='diseases',
            field=models.ManyToManyField(to='variety_trials_data.Disease', null=True, through='variety_trials_data.Disease_Entry', blank=True),
        ),
        migrations.AddField(
            model_name='trial_entry',
            name='variety',
            field=models.ForeignKey(help_text=b'Name of variety', to='variety_trials_data.Variety'),
        ),
        migrations.AddField(
            model_name='location',
            name='zipcode',
            field=models.ForeignKey(help_text=b'Format: 12345, The five-digit zipcode of this locaton.', to='variety_trials_data.Zipcode'),
        ),
        migrations.AddField(
            model_name='disease_entry',
            name='variety',
            field=models.ForeignKey(help_text=b'Name of variety', to='variety_trials_data.Variety'),
        ),
    ]
