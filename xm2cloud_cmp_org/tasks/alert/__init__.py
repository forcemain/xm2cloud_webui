#! -*- coding: utf-8 -*-


import json


from celery.task import task
from ...utils.enhance import Switch


@task(ignore_result=True)
def graphite_alert_dispatcher(**kwargs):
    from ... import models
    check_type, instance_set_json = map(kwargs.get, ['check_type', 'instance_set'])

    for ins_dict in json.loads(instance_set_json):
        queryset = models.CheckHostResult.objects.filter(pk=ins_dict['pk'])
        if not queryset.exists():
            continue
        ins = queryset.first()
        for sta_case in Switch(ins.sta_status):
            if sta_case(models.ConstantsForChecking.Status.PASSING_STATUS):
                for end_case in Switch(ins.end_status):
                    if end_case(models.ConstantsForChecking.Status.PASSING_STATUS):
                        # passing to passing
                        break
                    if end_case(models.ConstantsForChecking.Status.WARNING_STATUS):
                        # passing to warning
                        ins.alert_status = models.ConstantsForChecking.Status.ALERTING_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.ERROR_STATUS):
                        # passing to error
                        ins.alert_status = models.ConstantsForChecking.Status.ALERTING_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.CRITICAL_STATUS):
                        # passing to critical
                        ins.alert_status = models.ConstantsForChecking.Status.ALERTING_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case():
                        break
                break
            if sta_case(models.ConstantsForChecking.Status.WARNING_STATUS):
                for end_case in Switch(ins.end_status):
                    if end_case(models.ConstantsForChecking.Status.PASSING_STATUS):
                        # warning to passing
                        ins.alert_status = models.ConstantsForChecking.Status.RELIEVED_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.WARNING_STATUS):
                        # warning to warning
                        ins.alert_status = models.ConstantsForChecking.Status.ALERTING_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.ERROR_STATUS):
                        # warning to error
                        ins.alert_status=models.ConstantsForChecking.Status.ALERTING_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.CRITICAL_STATUS):
                        # warning to critical
                        ins.alert_status = models.ConstantsForChecking.Status.ALERTING_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case():
                        break
                break
            if sta_case(models.ConstantsForChecking.Status.ERROR_STATUS):
                for end_case in Switch(ins.end_status):
                    if end_case(models.ConstantsForChecking.Status.PASSING_STATUS):
                        # error to passing
                        ins.alert_status = models.ConstantsForChecking.Status.RELIEVED_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.WARNING_STATUS):
                        # error to warning
                        ins.alert_status = models.ConstantsForChecking.Status.RELIEVED_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.ERROR_STATUS):
                        # error to error
                        ins.alert_status = models.ConstantsForChecking.Status.ALERTING_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.CRITICAL_STATUS):
                        # error to critical
                        ins.alert_status = models.ConstantsForChecking.Status.ALERTING_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case():
                        break
                break
            if sta_case(models.ConstantsForChecking.Status.CRITICAL_STATUS):
                for end_case in Switch(ins.end_status):
                    if end_case(models.ConstantsForChecking.Status.PASSING_STATUS):
                        # critical to passing
                        ins.alert_status = models.ConstantsForChecking.Status.RELIEVED_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.WARNING_STATUS):
                        # critical to warning
                        ins.alert_status=models.ConstantsForChecking.Status.RELIEVED_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.ERROR_STATUS):
                        # critical to error
                        ins.alert_status = models.ConstantsForChecking.Status.RELIEVED_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case(models.ConstantsForChecking.Status.CRITICAL_STATUS):
                        # critical to critical
                        ins.alert_status = models.ConstantsForChecking.Status.ALERTING_STATUS
                        models.Notification.objects.get_or_create(
                            notice_way='email', alarms_way=check_type, checkhostresult=ins
                        )
                        break
                    if end_case():
                        break
                break
        ins.save()


@task(ignore_result=True)
def http_alert_dispatcher(**kwargs):
    print 'http_alert_dispatcher: ', kwargs


@task(ignore_result=True)
def port_alert_dispatcher(**kwargs):
    print 'port_alert_dispatcher: ', kwargs


@task(ignore_result=True)
def service_alert_dispatcher(**kwargs):
    print 'service_alert_dispatcher: ', kwargs
