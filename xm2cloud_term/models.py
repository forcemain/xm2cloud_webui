# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.utils import timezone


from .common.enhance import Random


class Identification(models.Model):
    port = models.IntegerField(default=65022)
    password = models.CharField(max_length=32, blank=True)
    username = models.CharField(max_length=32, default='root')
    authfile = models.FileField(upload_to='sshkeys', blank=True)
    notes = models.CharField(max_length=255, default='', blank=True)
    authpass = models.CharField(max_length=32, default='', blank=True)
    create_time = models.DateTimeField(auto_created=True, default=timezone.now, blank=True)
    id = models.CharField(max_length=36, primary_key=True, auto_created=True, default=Random.get_uuid, editable=False)
    authtype = models.CharField(max_length=16, choices=[('password', 'password'), ('authfile', 'authfile')],
                                default='password')
    protocol = models.CharField(max_length=32, default='ssh',
                                choices=[
                                    ('ssh', 'ssh'), ('vnc', 'vnc'), ('rdp', 'rdp'), ('sftp', 'sftp'),
                                    ('telnet', 'telnet')
                                ])

    host = models.ForeignKey('xm2cloud_cmp.Host')

    class Meta:
        unique_together = ('host', 'port', 'username')

    def get_host_ip(self):
        return self.host.ipline_set.filter(is_preferred=True).first()

    def __str__(self):
        host_ip = self.get_host_ip()
        return '{0}:{1} {2}'.format(host_ip, self.port, self.username)
