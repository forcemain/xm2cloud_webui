#! -*- coding: utf-8 -*-


from django.conf import settings
from django.dispatch import receiver
from django_redis import get_redis_connection
from django.db.models.signals import post_delete


from ..models import ScriptLog


@receiver(post_delete, sender=ScriptLog)
def script_log(sender, instance, **kwargs):
    event_id, host_id = instance.sevent_uuid, instance.host.pk

    rds = get_redis_connection('default')
    map(lambda k: rds.delete(k), [
        '{0}::{1}::{2}'.format(settings.LOGGING_TASK_KEY_PREFIX, event_id, host_id),
        '{0}::{1}::{2}'.format(settings.LOGGING_TASK_VAL_PREFIX, event_id, host_id)
    ])
