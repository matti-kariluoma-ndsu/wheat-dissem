# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadProgress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(help_text=b'path the users uploaded spreadsheet has been stored', max_length=4096)),
                ('submitted', models.BooleanField(default=False, help_text=b'have we finished processing this spreadsheet?')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, help_text=b'datetime this request was created')),
                ('user', models.ForeignKey(help_text=b'foreign key to the user this token is for', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
