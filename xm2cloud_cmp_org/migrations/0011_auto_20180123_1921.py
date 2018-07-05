# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-23 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xm2cloud_cmp', '0010_auto_20180123_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statuscheck',
            name='cached_health',
        ),
        migrations.AlterField(
            model_name='statuscheck',
            name='check_value',
            field=models.TextField(default=0),
        ),
        migrations.AlterField(
            model_name='statuscheck',
            name='compare_method',
            field=models.CharField(choices=[('avges', '\u5e73\u5747\u503c'), ('mines', '\u6700\u5c0f\u503c'), ('maxes', '\u6700\u5927\u503c')], default='avg', max_length=32),
        ),
        migrations.AlterField(
            model_name='statuscheck',
            name='max_failed_nums',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='statuscheck',
            name='min_series_nums',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='statuscheck',
            name='successive',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
