# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import sys
import uuid
import calendar


from django.db import models
from django.utils import timezone
from django.core.cache import cache
from djcelery.models import PeriodicTask


reload(sys)
sys.setdefaultencoding('utf-8')


class Manufacturer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    short_name = models.CharField(max_length=32, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    website = models.CharField(max_length=255, default='#', blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


class Continent(models.Model):
    name = models.CharField(max_length=128, unique=True)
    short_name = models.CharField(max_length=32, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    continent = models.ForeignKey(Continent)

    def __str__(self):
        return self.name


class OemInfo(models.Model):
    name = models.CharField(max_length=255, default='')
    oemid = models.CharField(max_length=128, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return '{0}::{1}'.format(self.name, self.oemid)


class OperatingSystem(models.Model):
    name = models.CharField(max_length=128, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    kernel = models.CharField(max_length=32, choices=[('UNIX', 'UNIX'), (u'WINS', u'WINS')], default='UNIX')

    def __str__(self):
        return self.name


class Cluster(models.Model):
    name = models.CharField(max_length=128, unique=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


class ClusterContext(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()

    cluster = models.ForeignKey(Cluster)

    def __str__(self):
        return '{0}::{1}'.format(self.cluster.name, self.name)


class AlertContactGroup(models.Model):
    name = models.CharField(max_length=128)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name


class AlertContact(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)
    email = models.EmailField(unique=True, blank=False)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    alertcontactgroups = models.ManyToManyField(AlertContactGroup)

    def __str__(self):
        return self.name


class HostGroup(models.Model):
    name = models.CharField(max_length=128)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    cluster = models.ForeignKey(Cluster)
    alertcontactgroup = models.ForeignKey(AlertContactGroup, null=True, blank=True)

    def __str__(self):
        return self.name


class HostGroupContext(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()

    hostgroup = models.ForeignKey(HostGroup)

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
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    area = models.ForeignKey(Region)
    firm = models.ForeignKey(Manufacturer)
    oems = models.ManyToManyField(OemInfo)
    vmos = models.ForeignKey(OperatingSystem)
    hostgroups = models.ManyToManyField(HostGroup)

    def __str__(self):
        return self.name

    def agentstate(self):
        key = 'xm2cloud_agent::heartbeat::{0}'.format(self.pk)

        return cache.get(key)

    def checkstate(self):
        key = 'xm2cloud_sched::checking::{0}'.format(self.pk)

        return cache.get(key)

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
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    line = models.CharField(max_length=128, choices=[(u'移动', u'移动'), (u'联通', u'联通'),
                                                     (u'电信', u'电信'), (u'其它', u'其它')], default=u'移动')

    def __str__(self):
        return '{0}::{1}'.format(self.line, self.name)


class IpLine(models.Model):
    band = models.IntegerField(default=30, blank=True)
    is_preferred = models.BooleanField(default=False)
    ip = models.GenericIPAddressField(blank=True, null=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    line = models.CharField(max_length=128, choices=[('BGP', 'BGP'), (u'移动', u'移动'), (u'联通', u'联通'),
                                                     (u'电信', u'电信'), (u'其它', u'其它')], default='BGP')

    host = models.ForeignKey(Host, null=True, blank=True)
    package = models.ForeignKey(IpLinePackage, null=True, blank=True)

    def __str__(self):
        return '{0}::{1}'.format(self.line, self.ip)


class DashBoardScreen(models.Model):
    name = models.CharField(max_length=255)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)

    def __str__(self):
        return self.name


class DashBoardScreenTarget(models.Model):
    target = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='', blank=True)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    charttype = models.CharField(max_length=32, choices=[('line', 'line'), ('pie', 'pie'), ('area', 'area'),
                                                         ('table', 'table'), ('hotmap', 'hotmap')], default='line')

    screen = models.ForeignKey(DashBoardScreen, related_name='targets')

    def __str__(self):
        return '{0}::{1}'.format(self.name, self.target)
