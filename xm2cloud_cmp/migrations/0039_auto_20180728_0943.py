# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-28 09:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0038_auto_20180727_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alarmstrategy',
            old_name='level',
            new_name='grade',
        )
    ]
