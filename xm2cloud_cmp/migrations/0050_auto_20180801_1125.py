# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-01 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0049_alarmhistory_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarmhistory',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]