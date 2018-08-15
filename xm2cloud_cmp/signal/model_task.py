#! -*- coding: utf-8 -*-


from django.conf import settings
from celery.registry import tasks
from django.dispatch import receiver
from djcelery.models import PeriodicTask
from django_redis import get_redis_connection
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete


from ..tasks import ExecutorUpdateUserData
from . import host_post_save, hostgroup_post_save, cluster_post_save
from ..models import TimedTask, Host, HostGroup, Cluster, ScriptLog, UpdateLog


@receiver(pre_delete, sender=ScriptLog)
def script_log_delete(sender, instance, **kwargs):
    event_id, host_id = instance.sevent_uuid, instance.host.pk

    rds = get_redis_connection('default')
    map(lambda k: rds.delete(k), [
        '{0}::{1}::{2}'.format(settings.LOGGING_TASK_KEY_PREFIX, event_id, host_id),
        '{0}::{1}::{2}'.format(settings.LOGGING_TASK_VAL_PREFIX, event_id, host_id)
    ])


@receiver(pre_delete, sender=UpdateLog)
def update_log_delete(sender, instance, **kwargs):
    event_id, host_id = instance.sevent_uuid, instance.host.pk

    rds = get_redis_connection('default')
    map(lambda k: rds.delete(k), [
        '{0}::{1}::{2}'.format(settings.LOGGING_TASK_KEY_PREFIX, event_id, host_id),
        '{0}::{1}::{2}'.format(settings.LOGGING_TASK_VAL_PREFIX, event_id, host_id)
    ])


@receiver(post_save, sender=TimedTask)
def timedtask_save_change(instance, **kwargs):
    instance.no_changes = False
    pre_save.send(sender=PeriodicTask, instance=instance)


@receiver(pre_delete, sender=TimedTask)
def timedtask_delete_change(instance, **kwargs):
    instance.no_changes = False
    pre_delete.send(sender=PeriodicTask, instance=instance)


@receiver(host_post_save, sender=Host)
def host_save_change(instance, **kwargs):
    func = tasks[ExecutorUpdateUserData.name]
    func.delay(owner=instance.owner.pk, host=instance.pk)


@receiver(pre_delete, sender=Host)
def host_delete_change(instance, **kwargs):
    pass


@receiver(cluster_post_save, sender=Cluster)
def cluster_save_change(instance, before_hostgroup_set, after_hostgroup_set, **kwargs):
    pass


@receiver(pre_delete, sender=Cluster)
def cluster_delete_change(instance, **kwargs):
    pass


@receiver(hostgroup_post_save, sender=HostGroup)
def hostgroup_save_change(instance, before_host_set, after_host_set, **kwargs):
    func = tasks[ExecutorUpdateUserData.name]
    hosts = before_host_set | after_host_set
    map(lambda h: func.delay(owner=instance.owner.pk, host=h), hosts)


@receiver(pre_delete, sender=HostGroup)
def hostgroup_delete_change(instance, **kwargs):
    pass
