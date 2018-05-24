# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-31 01:33
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0042_auto_20180331_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporting',
            name='task_id',
            field=models.CharField(blank=True, default=uuid.UUID('76417e3d-ec1e-4f5e-8bfb-aa3547741268'), max_length=36),
        ),
        migrations.AlterField(
            model_name='reporttask',
            name='fromdate',
            field=models.CharField(blank=True, choices=[(b'01:33_20180330', 'last_day'), (b'01:33_20180324', 'last_week'), (b'01:33_20180106', 'last_quarter'), (b'01:33_20170429', 'last_year')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='reporttask',
            name='task_id',
            field=models.CharField(blank=True, default=uuid.UUID('c4cd7477-02c4-43a8-9e6e-de068485f0e6'), max_length=36),
        ),
    ]
