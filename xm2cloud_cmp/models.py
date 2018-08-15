# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import sys
import calendar


from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django_redis import get_redis_connection
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule


from .common.enhance import Random


reload(sys)
sys.setdefaultencoding('utf-8')


class Manufacturer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    short_name = models.CharField(max_length=32, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    website = models.CharField(max_length=255, default='#', blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name


class Continent(models.Model):
    name = models.CharField(max_length=128, unique=True)
    short_name = models.CharField(max_length=32, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    continent = models.ForeignKey(Continent)
    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name


class OemInfo(models.Model):
    name = models.CharField(max_length=255, default='')
    oemid = models.CharField(max_length=128, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return '{0}::{1}'.format(self.name, self.oemid)


class OperatingSystem(models.Model):
    name = models.CharField(max_length=128, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)
    kernel = models.CharField(max_length=32, choices=[('UNIX', 'UNIX'), (u'WINS', u'WINS')], default='UNIX')

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name


class Cluster(models.Model):
    name = models.CharField(max_length=128, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name


class ClusterContext(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()

    cluster = models.ForeignKey(Cluster)
    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return '{0}::{1}'.format(self.cluster.name, self.name)


class AlertContactGroup(models.Model):
    name = models.CharField(max_length=128)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name


class AlertContact(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)
    email = models.EmailField(unique=True, blank=False)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)
    alertcontactgroups = models.ManyToManyField(AlertContactGroup)

    def __str__(self):
        return self.name


class HostGroup(models.Model):
    name = models.CharField(max_length=128)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)
    cluster = models.ForeignKey(Cluster, null=True, blank=True)
    alertcontactgroup = models.ForeignKey(AlertContactGroup, null=True, blank=True)

    def __str__(self):
        return self.name


class HostGroupContext(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()

    hostgroup = models.ForeignKey(HostGroup)
    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return '{0}::{1}'.format(self.hostgroup.name, self.name)


class Host(models.Model):
    name = models.CharField(max_length=128)
    vmcpu = models.IntegerField(default=4, blank=True)
    vmmem = models.IntegerField(default=4, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    expiry_time = models.DateTimeField(default=timezone.now, blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)
    bill_method = models.SmallIntegerField(choices=[(0, u'包年/包月'), (1, u'流量/计算')], default=0)

    area = models.ForeignKey(Region)
    firm = models.ForeignKey(Manufacturer)
    oems = models.ManyToManyField(OemInfo)
    vmos = models.ForeignKey(OperatingSystem)
    owner = models.ForeignKey(User, null=True, blank=True)
    hostgroups = models.ManyToManyField(HostGroup)

    def __str__(self):
        return self.name

    def agentstate(self):
        rds = get_redis_connection('default')
        key = '{0}::{1}'.format(settings.AGENT_HEARTBEAT_TASK_KEY_PREFIX, self.pk)

        return rds.hgetall(key)

    def is_running(self):
        rds = get_redis_connection('default')
        key = '{0}::{1}'.format(settings.AGENT_HEARTBEAT_TASK_KEY_PREFIX, self.pk)

        return rds.exists(key)

    def is_outdate(self):
        time_delta = self.expiry_time - timezone.now()

        _now = timezone.now()
        _year, _month = _now.year, _now.month
        monthrange = calendar.monthrange(_year, _month)

        return time_delta.days < monthrange[1]

    def is_overdue(self):
        return timezone.now() > self.expiry_time

    def is_unusual(self):
        return False

    @property
    def remoteip(self):
        return self.ipline_set.filter(is_preferred=True).first().ip


class IpLinePackage(models.Model):
    band = models.IntegerField(default=200, blank=True)
    name = models.CharField(max_length=255, default='', blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)
    line = models.CharField(max_length=128, choices=[(u'移动', u'移动'), (u'联通', u'联通'),
                                                     (u'电信', u'电信'), (u'其它', u'其它')], default=u'移动')

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return '{0}::{1}'.format(self.line, self.name)


class IpLine(models.Model):
    band = models.IntegerField(default=30, blank=True)
    is_preferred = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(blank=True, null=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)
    line = models.CharField(max_length=128, choices=[('BGP', 'BGP'), (u'移动', u'移动'), (u'联通', u'联通'),
                                                     (u'电信', u'电信'), (u'其它', u'其它')], default='BGP')

    owner = models.ForeignKey(User, null=True, blank=True)
    host = models.ForeignKey(Host, null=True, blank=True)
    package = models.ForeignKey(IpLinePackage, null=True, blank=True)

    def __str__(self):
        return '{0}::{1}'.format(self.line, self.ip)


class ScriptGroup(models.Model):
    name = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name


class Script(models.Model):
    contents = models.TextField()
    name = models.CharField(max_length=255)
    parameters = models.TextField(default='', blank=True)
    timeout = models.IntegerField(default=300, blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)
    interpreter = models.CharField(max_length=32, choices=[('sh', 'sh'), ('python', 'python'),
                                                           ('ruby', 'ruby'), ('perl', 'perl')], default='sh')
    platform = models.CharField(max_length=32, choices=[('linux', 'linux'), ('windows', 'windows')], default='linux')
    owner = models.ForeignKey(User, null=True, blank=True)
    scriptgroup = models.ForeignKey(ScriptGroup, null=True, blank=True)

    def __str__(self):
        return self.name


class TimedTask(PeriodicTask):
    notes = models.CharField(max_length=255, default='', blank=True)
    sevent_uuid = models.CharField(max_length=36, unique=True, auto_created=True, default=Random.get_uuid, editable=False)

    host = models.ForeignKey(Host, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    script = models.ForeignKey(Script, null=True, blank=True)
    cluster = models.ForeignKey(Cluster, null=True, blank=True)
    hostgroup = models.ForeignKey(HostGroup, null=True, blank=True)


class TaskWorkFlow(models.Model):
    name = models.CharField(max_length=128, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False,
                          validators=[])

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name


class WorkFlowTask(models.Model):
    name = models.CharField(max_length=128, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    with_timeout = models.SmallIntegerField(choices=[(0, u'挂起编排任务'), (1, u'忽略继续执行')], default=0)
    with_failure = models.SmallIntegerField(choices=[(0, u'挂起编排任务'), (1, u'忽略继续执行')], default=0)
    with_unknown = models.SmallIntegerField(choices=[(0, u'挂起编排任务'), (1, u'忽略继续执行')], default=0)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False,
                          validators=[])

    host = models.ForeignKey(Host, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    script = models.ForeignKey(Script, null=True, blank=True)
    cluster = models.ForeignKey(Cluster, null=True, blank=True)
    next_task = models.ForeignKey('self', null=True, blank=True)
    hostgroup = models.ForeignKey(HostGroup, null=True, blank=True)
    taskworkflow = models.ForeignKey(TaskWorkFlow, null=True, blank=True)

    def __str__(self):
        return self.name


class ScriptLog(models.Model):
    user_script = models.TextField(default='', blank=True)
    run_parameters = models.TextField(default='', blank=True)
    run_timeout = models.IntegerField(default=300, blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    script_name = models.CharField(max_length=255, default='', blank=True)
    sevent_uuid = models.CharField(max_length=36, default=Random.get_uuid, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    run_interpreter = models.CharField(max_length=32, choices=[('sh', 'sh'), ('python', 'python'),
                                                               ('ruby', 'ruby'), ('perl', 'perl')], default='sh')
    run_platform = models.CharField(max_length=32, choices=[('linux', 'linux'),
                                                            ('windows', 'windows')], default='linux')
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False,
                          validators=[])
    triggermode = models.SmallIntegerField(choices=[(0, u'手动执行'), (1, u'定时任务'), (2, u'发生告警'), (3, u'告警解除')],
                                           default=0)

    owner = models.ForeignKey(User, null=True, blank=True)
    host = models.ForeignKey(Host, null=True, blank=True)
    script = models.ForeignKey(Script, null=True, blank=True)
    cluster = models.ForeignKey(Cluster, null=True, blank=True)
    timedtask = models.ForeignKey(TimedTask, null=True, blank=True)
    hostgroup = models.ForeignKey(HostGroup, null=True, blank=True)

    def __str__(self):
        return '{0}::{1}'.format(self.get_triggermode_display(), self.script and self.script.name or u'自定义脚本')

    def task_state(self):
        """
        1310 等待
        1311 执行
        1312 超时
        1313 失败
        1314 成功
        1315 未知

        xm2cloud_agent::logging::key::77b00ac1-d891-432c-b1b4-8127759d1133::d0bc3866-5126-49a7-a206-27686e1889a1
        [
            1528813713.75694: 1311,
            1528813738.650874: 1312,
            1528813753.20042: 1313,
            1528813772.090729: 1314,
            1528813786.416516: 1315
        ]
        """
        rds = get_redis_connection('default')
        key = '{0}::{1}::{2}'.format(settings.LOGGING_TASK_KEY_PREFIX, self.sevent_uuid, self.host.pk)
        val = rds.zrange(key, -1, -1)

        return int(val and val[0] or 1310)


class UpdateLog(models.Model):
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    sevent_uuid = models.CharField(max_length=36, default=Random.get_uuid, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False,
                          validators=[])

    host = models.ForeignKey(Host, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return '{0}::{1}'.format(self.sevent_uuid, self.host.pk)


class DashBoardScreen(models.Model):
    name = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)

    @property
    def iscompared(self):
        return self.dashboardscreentarget_set.filter(is_compared=True)

    @property
    def uncompared(self):
        return self.dashboardscreentarget_set.filter(is_compared=False)

    def __str__(self):
        return self.name


class DashBoardScreenTarget(models.Model):
    metrics = models.TextField(default='')
    is_compared = models.BooleanField(default=False)
    weight = models.SmallIntegerField(default=0, blank=True)
    name = models.CharField(max_length=255, default='', blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    aggregators = models.CharField(max_length=255, default='', blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)
    charttype = models.CharField(max_length=32, choices=[('line', 'line'), ('pie', 'pie'), ('area', 'area'),
                                                         ('table', 'table'), ('hotmap', 'hotmap')], default='line')

    owner = models.ForeignKey(User, null=True, blank=True)
    hosts = models.ManyToManyField(Host, null=True, blank=True)
    screen = models.ForeignKey(DashBoardScreen, null=True, blank=True)

    class Meta:
        ordering = ['-weight']

    @property
    def metric_list(self):
        return self.metrics.split(',')

    @property
    def aggregator_list(self):
        return self.aggregators.split(',')

    def __str__(self):
        return '{0}::{1}::{2}'.format(self.name, self.metrics, self.aggregators)


class AlarmStrategyGroup(models.Model):
    name = models.CharField(max_length=255, default='', blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return '{0}:{1}'.format(self.name, self.notes)


class MessageTopic(models.Model):
    name = models.CharField(max_length=255, default='', blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return '{0}:{1}'.format(self.name, self.notes)


class MessageSubscriber(models.Model):
    terminal = models.TextField()
    name = models.CharField(max_length=255, default='', blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    protocol = models.CharField(max_length=32, choices=[('sms', u'短信'), ('email', u'邮件'),
                                                        ('http', u'HTTP'), ('https', u'HTTPS')])
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)
    topic = models.ForeignKey(MessageTopic, null=True, blank=True)

    def __str__(self):
        return '{0}:{1}'.format(self.protocol, self.name)


class AlarmStrategy(PeriodicTask):
    rules = models.TextField(default='')
    notes = models.CharField(max_length=255, default='', blank=True)
    sevent_uuid = models.CharField(max_length=36, unique=True, auto_created=True, default=Random.get_uuid,
                                   editable=False)
    grade = models.SmallIntegerField(choices=[(1, u'提示'), (2, u'次要'), (3, u'重要'), (4, u'紧急')], default=3, blank=True)

    owner = models.ForeignKey(User, null=True, blank=True)
    hosts = models.ManyToManyField(Host, null=True, blank=True)
    topic = models.ForeignKey(MessageTopic, null=True, blank=True)
    alarmstrategygroup = models.ForeignKey(AlarmStrategyGroup, null=True, blank=True)

    def __str__(self):
        return '{0}:{1}'.format(self.name, self.notes)


class AlarmHistory(models.Model):
    error = models.TextField(default='')
    notes = models.TextField(default='')
    name = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    host = models.ForeignKey(Host, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    alarmstrategy = models.ForeignKey(AlarmStrategy, null=True, blank=True)

    def __str__(self):
        return self.name


class Acknowledge(models.Model):
    message = models.TextField()
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    ack_choices = models.SmallIntegerField(choices=[(0, u'单个确认'), (1, u'确认所有')], default=0)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)

    owner = models.ForeignKey(User, null=True, blank=True)
    alarmhistory = models.ForeignKey(AlarmHistory, null=True, blank=True)

    def __str__(self):
        return self.message
