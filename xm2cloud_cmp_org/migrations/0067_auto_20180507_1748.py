# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-07 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0066_auto_20180507_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='metric_uuid',
            field=models.UUIDField(default=b'aa09b87a-ca5a-424f-8d50-7a80d088f44f'),
        ),
    ]