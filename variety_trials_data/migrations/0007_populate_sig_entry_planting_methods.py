# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def populate_sig_pm(apps, schema_editor):
	# We can't import a model directly as it may be a newer
	# version than this migration expects. We use the historical version.
	TrialEntry = apps.get_model('variety_trials_data', 'TrialEntry')
	SignificanceEntry = apps.get_model('variety_trials_data', 'SignificanceEntry')
	PlantingMethod = apps.get_model('variety_trials_data', 'PlantingMethod')
	sigs_lsd_5 = {}
	sigs_lsd_10 = {}
	sigs_10_hsd = {}
	planting_methods = {}
	normal = PlantingMethod(planting_methods='')
	normal.save()
	planting_methods[''] = normal
	for entry in TrialEntry.objects.all():
		# write new planting tags, update planting method tags on trials
		pmt = entry.planting_method_tags
		if not pmt:
			pmt = ''
		if pmt not in planting_methods:
			pm = PlantingMethod(planting_methods=pmt)
			pm.save()
			planting_methods[pmt] = pm
		entry.planting_method_tags_new = planting_methods[pmt]
		entry.save()
		# collect significance values from all TrialEntry
		if entry.lsd_05:
			lpyv = (entry.location.pk, pmt, entry.harvest_date.date.year, entry.lsd_05)
			try:
				sigs_lsd_5[lpyv].append(entry.pk)
			except KeyError:
				sigs_lsd_5[lpyv] = [entry.pk]
		if entry.lsd_10:
			lpyv = (entry.location.pk, pmt, entry.harvest_date.date.year, entry.lsd_10)
			try:
				sigs_lsd_10[lpyv].append(entry.pk)
			except KeyError:
				sigs_lsd_10[lpyv] = [entry.pk]
		if entry.hsd_10:
			lpyv = (entry.location.pk, pmt, entry.harvest_date.date.year, entry.hsd_10)
			try:
				sigs_10_hsd[lpyv].append(entry.pk)
			except KeyError:
				sigs_10_hsd[lpyv] = [entry.pk]
	# write significance entries
	for lpyv, trial_pks in sigs_lsd_5.items():
		(loc_pk, planting_method_tags, year, value) = lpyv
		sigentry = SignificanceEntry(
				trials=TrialEntry.objects.filter(pk__in=trial_pks),
				comparing='bushels_acre',
				method='LSD',
				alpha=0.05,
				value=value,
			)
		sigentry.save()
	for lpyv, trial_pks in sigs_lsd_10.items():
		(loc_pk, planting_method_tags, year, value) = lpyv
		sigentry = SignificanceEntry(
				trials=TrialEntry.objects.filter(pk__in=trial_pks),
				comparing='bushels_acre',
				method='LSD',
				alpha=0.10,
				value=value,
			)
		sigentry.save()
	for lpyv, trial_pks in sigs_10_hsd.items():
		(loc_pk, planting_method_tags, year, value) = lpyv
		sigentry = SignificanceEntry(
				trials=TrialEntry.objects.filter(pk__in=trial_pks),
				comparing='bushels_acre',
				method='HSD',
				alpha=0.10,
				value=value,
			)
		sigentry.save()

class Migration(migrations.Migration):

    dependencies = [
        ('variety_trials_data', '0006_trialentry_planting_method_tags_new'),
    ]

    operations = [
        migrations.RunPython(populate_sig_pm),
    ]
