# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-28 10:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0045_auto_20180728_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alarmstrategy',
            name='periodictask_ptr',
        ),
        migrations.DeleteModel(
            name='AlarmStrategy',
        ),
    ]
