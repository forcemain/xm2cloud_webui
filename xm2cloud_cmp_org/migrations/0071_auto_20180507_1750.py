# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-07 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0070_auto_20180507_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='metric_uuid',
            field=models.UUIDField(default=b'6256d36e-7bb4-44bb-822a-3d9b0b1b4596'),
        ),
    ]
