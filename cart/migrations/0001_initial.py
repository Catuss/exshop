# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-23 22:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(max_length=50)),
                ('cart_date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(default=1)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Good')),
            ],
            options={
                'ordering': ['cart_date'],
            },
        ),
    ]