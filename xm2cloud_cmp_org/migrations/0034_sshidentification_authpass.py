# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-08 01:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0033_auto_20180305_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='sshidentification',
            name='authpass',
            field=models.CharField(default='', max_length=32),
        ),
    ]
