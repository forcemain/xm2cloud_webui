#! -*- coding: utf-8 -*-


from celery.task import task


@task(ignore_result=True)
def running_check(instance_or_id):
    from .. import models
    if isinstance(instance_or_id, models.GraphiteStatusCheck):
        ins = instance_or_id
    else:
        ins = models.GraphiteStatusCheck.objects.get(id=instance_or_id)
    ins.running_check()
