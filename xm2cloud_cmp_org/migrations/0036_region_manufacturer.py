# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-27 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0035_auto_20180310_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='manufacturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='xm2cloud_cmp.Manufacturer'),
        ),
    ]
