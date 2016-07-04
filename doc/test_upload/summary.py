#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""

from __future__ import print_function
import os, sys, json
import django

sys.path.append('../../')
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whip.settings')
django.setup()

from hrsw import models

def main():
	try:
		with open('summary.json', 'r') as f:
			last = json.load(f)
	except IOError:
		last = {}
	now = {}
	trials = models.TrialEntry.objects.order_by('-pk')
	sigs = models.SignificanceEntry.objects.order_by('-pk')
	now['trials'] = trials.count()
	now['sigs'] = sigs.count()
	now['tlast'] = trials[0].pk
	now['slast'] = sigs[0].pk
	with open('summary.json', 'w') as f:
		json.dump(now, f)
	if last:
		dt = now['trials'] - last['trials']
		ds = now['sigs'] - last['sigs']
	else:
		print('No data from last run, assume first run on new database', file=sys.stderr)
		dt = now['trials']
		ds = now['sigs']
	print('change in TrialEntry        ', dt)
	print('change in SignificanceEntry ', ds)

if __name__ == '__main__':
	main()

