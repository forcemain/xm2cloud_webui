#! -*- coding: utf-8 -*-

from django.dispatch import Signal
from ..utils.enhance import Switch


report_task_dispatch_post_save = Signal(providing_args=['sender', 'report_type'])


def report_task_dispatch_hook(sender, report_type,  **kwargs):
    from ..tasks import collect as report_tasks
    for case in Switch(report_type):
        if case('monitoring_overview'):
            report_tasks.monitoring_overview_dispatcher.delay(report_type=report_type, **kwargs)
            break
        if case('monitoring_detailed'):
            report_tasks.monitoring_detailed_dispatcher.delay(report_type=report_type, **kwargs)
            break
        if case('codedeploy_overview'):
            report_tasks.codedeploy_overview_dispatcher.delay(report_type=report_type, **kwargs)
            break
        if case('resources_occupy_low'):
            report_tasks.resources_occupy_low_dispatcher.delay(report_type=report_type, **kwargs)
            break
        if case('resources_occupy_high'):
            report_tasks.resources_occupy_high_dispatcher.delay(report_type=report_type, **kwargs)
            break
        if case():
            print 'Error with typeof report task, ignore'
            break

report_task_dispatch_post_save.connect(report_task_dispatch_hook)
