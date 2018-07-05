#! -*- coding: utf-8 -*-

from celery.task import task
from datetime import timedelta
from django.utils import timezone


@task(ignore_result=True)
def database_cleanup(**kwargs):
    from .. import models

    models.StatusCheckResult.objects.filter(end_time__isnull=False).order_by('end_time').filter(
        end_time__lte=timezone.now()-timedelta(**kwargs)
    ).delete()
