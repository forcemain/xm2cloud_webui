# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-07 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0005_scriptlog_script_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='timeout',
            field=models.IntegerField(default=300),
        ),
    ]
