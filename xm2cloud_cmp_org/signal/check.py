#! -*- coding: utf-8 -*-


from django.dispatch import Signal
from ..utils.enhance import Switch
from django.core import serializers


check_state_migration_post_save = Signal(providing_args=['sender', 'check_type'])


def check_state_migration_hook(sender, check_type, **kwargs):
    from ..tasks import alert as alert_tasks
    for case in Switch(check_type):
        if case('graphite_check'):
            instance_set = kwargs.pop('instance_set')
            if not instance_set.count():
                break
            data = serializers.serialize('json', instance_set)
            alert_tasks.graphite_alert_dispatcher.delay(instance_set=data, check_type=check_type)
            break
        if case('http_check'):
            # preprocessing
            alert_tasks.http_alert_dispatcher.delay(**{})
            break
        if case('port_check'):
            # preprocessing
            alert_tasks.port_alert_dispatcher.delay(**{})
            break
        if case('service_check'):
            # preprocessing
            alert_tasks.service_alert_dispatcher.delay(**{})
            break
        if case():
            print 'Error with typeof status check, ignore'
            break


check_state_migration_post_save.connect(check_state_migration_hook)

