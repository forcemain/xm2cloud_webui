# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-14 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0002_auto_20180514_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostgroup',
            name='ports',
            field=models.CommaSeparatedIntegerField(blank=True, max_length=255, null=True),
        ),
    ]