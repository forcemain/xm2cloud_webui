# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-27 18:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0036_alarmstrategy_alarmstrategygroups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alarmstrategygroup',
            name='hosts',
        ),
    ]