# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-04 04:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0047_auto_20180404_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporting',
            name='template_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
