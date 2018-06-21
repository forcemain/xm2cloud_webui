# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import sys
import json
import uuid
import calendar


from django.db import models
from celery import current_app
from django.utils import timezone
from djcelery.models import PeriodicTask
from celery.exceptions import SoftTimeLimitExceeded


reload(sys)
sys.setdefaultencoding('utf-8')


from django.core.cache import cache
from .tasks import check as check_tasks
from .tasks import alert as alert_tasks
from .tasks import clean as clean_tasks
from .tasks import report as report_tasks
from .tasks import collect as collect_tasks
from .signal import check as check_signals
from .signal import report as report_signals


class ConstantsForCelery(object):
    class Date(object):
        REPORT_DURINGS = [
            ('last_day', 'last_day'),
            ('last_week', 'last_week'),
            ('last_quarter', 'last_quarter'),
            ('last_year', 'last_year')
        ]

    class Task(object):
        def get_tasks(self, category=None):
            all_tasks = [t for t in current_app.tasks if not t.startswith('celery.')]
            if category is not None:
                tasks = [t for t in all_tasks if category in t]
            else:
                tasks = all_tasks

            return tasks

        CHECKING_TASKS = zip(
            get_tasks(None, category='.check.'),
            get_tasks(None, category='.check.')
        )
        REPORTING_TASKS = zip(
            get_tasks(None, category='.report.'),
            get_tasks(None, category='.report.')
        )
        REPORTING_TYPES = [
            ('monitoring_overview', 'monitoring_overview'),
            ('monitoring_detailed', 'monitoring_detailed'),
            ('codedeploy_overview', 'codedeploy_overview'),
            ('resources_occupy_low', 'resources_occupy_low'),
            ('resources_occupy_high', 'resources_occupy_high')
        ]


class ConstantsForDashBoard(object):
    class Chart(object):
        PIE_CHART_TYPE = 'pie'
        LINE_CHART_TYPE = 'line'
        AREA_CHART_TYPE = 'area'
        TABLE_CHART_TYPE = 'table'
        HOTMAP_CHART_TYPE = 'hotmap'

        CHART_TYPES = [
            (PIE_CHART_TYPE, PIE_CHART_TYPE),
            (LINE_CHART_TYPE, LINE_CHART_TYPE),
            (AREA_CHART_TYPE, AREA_CHART_TYPE),
            (TABLE_CHART_TYPE, TABLE_CHART_TYPE),
            (HOTMAP_CHART_TYPE, HOTMAP_CHART_TYPE)
        ]


class ConstantsForChecking(object):
    class Status(object):
        ERROR_STATUS = 'error'
        PASSING_STATUS = 'passing'
        WARNING_STATUS = 'warning'
        CRITICAL_STATUS = 'critical'

        IGNORED_STATUS = 'ignored'
        ALERTING_STATUS = 'alerting'
        RELIEVED_STATUS = 'relieved'

        CHECKING_STATUSES = [
            (PASSING_STATUS, PASSING_STATUS),
            (WARNING_STATUS, WARNING_STATUS),
            (ERROR_STATUS, ERROR_STATUS),
            (CRITICAL_STATUS, CRITICAL_STATUS),
        ]

        ALERTING_STATUSES = [
            (ALERTING_STATUS, ALERTING_STATUS),
            (IGNORED_STATUS, IGNORED_STATUS),
            (RELIEVED_STATUS, RELIEVED_STATUS),
        ]

        CALCULATED_PASSING_STATUS = 'passing'
        CALCULATED_FAILING_STATUS = 'failing'
        CALCULATED_EXCEPTION_STATUS = 'exception'
        CALCULATED_INTERMITTENT_STATUS = 'intermittent'

        CALCULATED_STATUSES = [
            (CALCULATED_PASSING_STATUS, CALCULATED_PASSING_STATUS),
            (CALCULATED_FAILING_STATUS, CALCULATED_FAILING_STATUS),
            (CALCULATED_EXCEPTION_STATUS, CALCULATED_EXCEPTION_STATUS),
            (CALCULATED_INTERMITTENT_STATUS, CALCULATED_INTERMITTENT_STATUS)
        ]

    class Comparision(object):
        COMPARE_LT_TERMS = 'lt'
        COMPARE_LE_TERMS = 'le'
        COMPARE_EQ_TERMS = 'eq'
        COMPARE_GT_TERMS = 'gt'
        COMPARE_GE_TERMS = 'ge'

        COMPARE_AVG_METHOD = 'avg'
        COMPARE_MIN_METHOD = 'min'
        COMPARE_MAX_METHOD = 'max'

        COMPARE_TERMS = [
            (COMPARE_LT_TERMS, COMPARE_LT_TERMS),
            (COMPARE_LE_TERMS, COMPARE_LE_TERMS),
            (COMPARE_EQ_TERMS, COMPARE_EQ_TERMS),
            (COMPARE_GT_TERMS, COMPARE_GT_TERMS),
            (COMPARE_GE_TERMS, COMPARE_GE_TERMS)
        ]

        COMPARE_METHODS = [
            (COMPARE_AVG_METHOD, COMPARE_AVG_METHOD),
            (COMPARE_MIN_METHOD, COMPARE_MIN_METHOD),
            (COMPARE_MAX_METHOD, COMPARE_MAX_METHOD),
        ]

    class Unit(object):
        FROM_DAY_UNIT = 'd'
        FROM_HOUR_UNIT = 'h'
        FROM_WEEK_UNIT = 'w'
        FROM_YEAR_UNIT = 'y'
        FROM_SECOND_UNIT = 's'
        FROM_MONTH_UNIT = 'mon'
        FROM_MINUTE_UNIT = 'min'

        FROM_UNITS = [
            (FROM_SECOND_UNIT, 'seconds'),
            (FROM_MINUTE_UNIT, 'minutes'),
            (FROM_HOUR_UNIT, 'hours'),
            (FROM_DAY_UNIT, 'days'),
            (FROM_WEEK_UNIT, 'weeks'),
            (FROM_MONTH_UNIT, 'monthes'),
            (FROM_YEAR_UNIT, 'years')
        ]


class ConstantsForIdentification(object):
    class AuthType(object):
        PASSWORD_AUTH_TYPE = 'password'
        AUTHFILE_AUTH_TYPE = 'authfile'
        AUTH_TYPES = [
            (PASSWORD_AUTH_TYPE, PASSWORD_AUTH_TYPE),
            (AUTHFILE_AUTH_TYPE, AUTHFILE_AUTH_TYPE),
        ]


class IpLine(models.Model):
    ip = models.GenericIPAddressField(blank=True, null=True)
    band = models.IntegerField(default=30, blank=True)
    name = models.CharField(max_length=128)
    is_preferred = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return '{0}_{1}'.format(self.name, self.ip)


class Manufacturer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    website = models.URLField(default='')
    short_name = models.CharField(max_length=32, unique=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.name


class Continent(models.Model):
    name = models.CharField(max_length=128, unique=True)
    short_name = models.CharField(max_length=32, unique=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    continent = models.ForeignKey(Continent)

    def __str__(self):
        return self.name


class Envirment(models.Model):
    name = models.CharField(max_length=128, unique=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.name


class OemInformation(models.Model):
    oemid = models.CharField(max_length=128, unique=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)


class Project(models.Model):
    name = models.CharField(max_length=128, unique=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.name


class OperatingSystem(models.Model):
    type = models.CharField(max_length=64, default='linux')
    name = models.CharField(max_length=128, unique=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.name


class Cluster(models.Model):
    name = models.CharField(max_length=128, unique=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    env = models.ForeignKey(Envirment)
    project = models.ForeignKey(Project)

    def __str__(self):
        return self.name


class AlertContactGroup(models.Model):
    name = models.CharField(max_length=128)
    notes = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.name


class AlertContact(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=11)

    alertcontactgroups = models.ManyToManyField(AlertContactGroup)

    def __str__(self):
        return self.name


class HostGroup(models.Model):
    name = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    cluster = models.ForeignKey(Cluster)
    alertcontactgroup = models.ForeignKey(AlertContactGroup)

    def __str__(self):
        return self.name


class SSHIdentification(models.Model):
    name = models.CharField(max_length=255)
    authtype = models.CharField(max_length=16, default=ConstantsForIdentification.AuthType.PASSWORD_AUTH_TYPE,
                                choices=ConstantsForIdentification.AuthType.AUTH_TYPES)
    username = models.CharField(max_length=32, default='root')
    password = models.CharField(max_length=32, blank=True)
    authfile = models.FileField(upload_to='ssh_keys', blank=True)
    authpass = models.CharField(max_length=32, default='', blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    def __str__(self):
        return self.name


class Host(models.Model):
    name = models.CharField(max_length=128)
    vmcpu = models.IntegerField(default=4, blank=True)
    vmmem = models.IntegerField(default=4, blank=True)
    ssh_port = models.IntegerField(default=65022)
    update_time = models.DateTimeField(auto_now=True, blank=True)
    metric_uuid = models.UUIDField(default=uuid.uuid4().__str__())
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    expiry_time = models.DateTimeField(default=timezone.now, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)

    area = models.ForeignKey(Region)
    firm = models.ForeignKey(Manufacturer)
    vmos = models.ForeignKey(OperatingSystem)
    auth = models.ForeignKey(SSHIdentification)
    iplines = models.ManyToManyField(IpLine)
    hostgroups = models.ManyToManyField(HostGroup)

    def __str__(self):
        return self.name

    def is_running(self):
        return True

    def is_outdate(self):
        time_delta = self.expiry_time - timezone.now()

        _now = timezone.now()
        _year, _month = _now.year, _now.month
        monthrange = calendar.monthrange(_year, _month)

        return time_delta.days < monthrange[1]

    def is_overdue(self):
        return timezone.now() > self.expiry_time
    
    def is_unusual(self):
        return self.checkhostresult_set.exists()

    @property
    def remoteip(self):
        return self.iplines.filter(is_preferred=True).first().ip


class StatusCheck(PeriodicTask):
    class Meta:
        ordering = ['name']

    triggers = models.TextField(default='')
    reg_task = models.CharField(max_length=255, blank=True, null=True,
                                choices=ConstantsForCelery.Task.CHECKING_TASKS)

    def __str__(self):
        return self.name

    def save_signal(self):
        self.no_changes = False
        models.signals.pre_save.send(sender=PeriodicTask, instance=self)

    def delete_signal(self):
        self.no_changes = False
        models.signals.pre_delete.send(sender=PeriodicTask, instance=self)

    def save(self, *args, **kwargs):
        self.save_signal()

        if self.args == '[]':
            super(StatusCheck, self).save(*args, **kwargs)
            self.args = json.dumps([self.periodictask_ptr_id])
            super(StatusCheck, self).save(*args, **kwargs)
        else:
            super(StatusCheck, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_signal()

        super(StatusCheck, self).delete(*args, **kwargs)

    def running_check(self):
        try:
            self._run()
        except (SoftTimeLimitExceeded, Exception) as _:
            # do you want keep the exception _ ?
            pass

    def _run(self):
        raise NotImplementedError


class GraphiteStatusCheck(StatusCheck):
    CHECK_TYPE = 'graphite_check'

    def _run(self):
        pass


class HttpStatusCheck(StatusCheck):
    CHECK_TYPE = 'http_check'

    endpoint = models.TextField(null=True, blank=True)
    username = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    regexp_text = models.TextField(blank=True, null=True)
    status_code = models.TextField(default=200, null=True)
    req_timeout = models.IntegerField(default=30, null=True)
    ssl_enabled = models.BooleanField(default=False)

    def _run(self):
        pass


class PortStatusCheck(StatusCheck):
    CHECK_TYPE = 'port_check'

    def _run(self):
        pass


class StatusCheckResult(models.Model):
    sta_time = models.DateTimeField(null=True, db_index=True)
    end_time = models.DateTimeField(null=True, db_index=True)
    raw_data = models.TextField(null=True)
    err_nums = models.IntegerField(default=0)
    err_info = models.TextField(null=True)

    status_check = models.ForeignKey(StatusCheck)

    class Meta:
        ordering = ['-end_time']


class CheckHostResult(models.Model):
    sub_metric = models.TextField(null=True)
    messages = models.TextField(null=True)
    sta_time = models.DateTimeField(auto_created=True, default=timezone.now, db_index=True)
    end_time = models.DateTimeField(null=True, db_index=True)
    end_values = models.TextField(null=True)
    sta_status = models.CharField(max_length=64, choices=ConstantsForChecking.Status.CHECKING_STATUSES,
                                  default=ConstantsForChecking.Status.PASSING_STATUS)
    end_status = models.CharField(max_length=64, choices=ConstantsForChecking.Status.CHECKING_STATUSES,
                                  null=True)
    alert_status = models.CharField(max_length=64, choices=ConstantsForChecking.Status.ALERTING_STATUSES,
                                    default=ConstantsForChecking.Status.ALERTING_STATUS)
    host = models.ForeignKey(Host, null=True)
    check_result = models.ForeignKey(StatusCheckResult, null=True)

    class Meta:
        ordering = ['-end_time']


class Notification(models.Model):
    notice_way = models.CharField(max_length=32, default='email')
    alarms_way = models.CharField(max_length=32, default='')
    is_success = models.BooleanField(default=False)
    notifytime = models.DateTimeField(auto_created=True, default=timezone.now, db_index=True)
    retrytimes = models.IntegerField(default=0)

    checkhostresult = models.OneToOneField(CheckHostResult)

    class Meta:
        ordering = ['-notifytime']


class DashBoardScreen(models.Model):
    name = models.CharField(max_length=255)

    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)

    def __str__(self):
        return self.name


class DashBoardScreenTarget(models.Model):
    name = models.CharField(max_length=255, default='', blank=True)
    charttype = models.CharField(max_length=32, choices=ConstantsForDashBoard.Chart.CHART_TYPES,
                                 default='line')
    gh_target = models.TextField()

    screen = models.ForeignKey(DashBoardScreen, related_name='targets')

    def __str__(self):
        return self.gh_target


class ReportTask(PeriodicTask):
    period = models.CharField(max_length=32, choices=ConstantsForCelery.Date.REPORT_DURINGS, null=True)
    reg_task = models.CharField(max_length=255, choices=ConstantsForCelery.Task.REPORTING_TASKS, null=True)
    task_id = models.CharField(max_length=255, blank=True, null=True)
    task_type = models.CharField(max_length=64, choices=ConstantsForCelery.Task.REPORTING_TYPES, null=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)

    clusters = models.ManyToManyField(Cluster)
    hostgroups = models.ManyToManyField(HostGroup)
    contactgroups = models.ManyToManyField(AlertContactGroup)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        models.signals.pre_save.send(sender=PeriodicTask, instance=self)

        if self.args == '[]':
            super(ReportTask, self).save(*args, **kwargs)
            self.args = json.dumps([self.periodictask_ptr_id])
            super(ReportTask, self).save(*args, **kwargs)
            return
        super(ReportTask, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        models.signals.pre_delete.send(sender=PeriodicTask, instance=self)

        super(ReportTask, self).delete(*args, **kwargs)

    def running_report(self):
        instance_ids = [self.pk]
        report_signals.report_task_dispatch_post_save.send(
            sender=ReportTask, report_type=self.task_type, instance_ids=instance_ids
        )

    class Meta:
        ordering = ['-create_time']


class Reporting(models.Model):
    task_id = models.CharField(max_length=255, blank=True, null=True)
    context = models.TextField(default='')
    template_name = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)

    reporttask = models.ForeignKey(ReportTask)

    class Meta:
        ordering = ['-create_time']

