# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-18 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0027_dashboardscreentarget_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardscreentarget',
            name='weight',
            field=models.SmallIntegerField(blank=True, default=0),
        ),
    ]
