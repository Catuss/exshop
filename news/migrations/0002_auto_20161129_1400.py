# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 14:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2016, 11, 29, 14, 0, 26, 592197, tzinfo=utc), verbose_name='Опубликована'),
        ),
    ]
