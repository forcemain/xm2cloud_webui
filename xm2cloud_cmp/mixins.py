# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import time


from django.contrib.auth.models import User


from .common.rabbitmq import RabbitMQChannelSender
from .common.models.event.pub_event import PubEvent
from .common.models.event.event_type import EventType
from .common.models.event.user_script import UserScript
from .models import Cluster, HostGroup, Host, Script, ScriptLog, TimedTask


class ExecuteScriptMixin(object):
    _data_source = None
    result_model = ScriptLog
    sender_class = RabbitMQChannelSender

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, data):
        self._data_source = data

    def get_owner(self):
        ownerid = self.data_source.get('owner', 0)

        return User.objects.filter(pk=ownerid).first()

    def get_sender(self):
        return self.sender_class()

    def get_host(self):
        hostid = self.data_source.get('host', '')

        return Host.objects.filter(pk=hostid).first()

    def get_script(self):
        scriptid = self.data_source.get('script', '')

        return Script.objects.filter(pk=scriptid).first()

    def get_cluster(self):
        clusterid = self.data_source.get('cluster', '')

        return Cluster.objects.filter(pk=clusterid).first()

    def get_hostgroup(self):
        hostgroupid = self.data_source.get('hostgroup', '')

        return HostGroup.objects.filter(pk=hostgroupid).first()

    def get_timedtask(self):
        timedtaskid = self.data_source.get('timedtask', '')

        return TimedTask.objects.filter(sevent_uuid=timedtaskid).first()

    def get_encrypt_data(self, data):
        encryption = None

        return encryption, data

    def get_parameter_data(self):
        # maybe you need rewrite
        return {}

    def get_execute_target(self, sevent_uuid, cluster, hostgroup, host):
        instances_list = []
        parameter_dict = self.get_parameter_data()

        if host:
            parameter_dict.update({
                'host': host,
                'cluster': cluster,
                'hostgroup': hostgroup,
                'sevent_uuid': sevent_uuid,
            })
            instances_list.append(self.result_model(**parameter_dict))

            return instances_list

        if hostgroup:
            for host in hostgroup.host_set.all():
                parameter_dict.update({
                    'host': host,
                    'cluster': cluster,
                    'hostgroup': hostgroup,
                    'sevent_uuid': sevent_uuid,
                })
                instances_list.append(self.result_model(**parameter_dict))

            return instances_list

        if cluster:
            for hostgroup in cluster.hostgroup_set.all():
                for host in hostgroup.host_set.all():
                    parameter_dict.update({
                        'host': host,
                        'cluster': cluster,
                        'hostgroup': hostgroup,
                        'sevent_uuid': sevent_uuid,
                    })
                    instances_list.append(self.result_model(**parameter_dict))

        return instances_list

    def get_instances_data(self, sevent_uuid):
        host = self.get_host()
        script = self.get_script()
        cluster = self.get_cluster()
        hostgroup = self.get_hostgroup()

        run_timeout = script and script.timeout or self.data_source.get('run_timeout', 300)
        user_script = script and script.contents or self.data_source.get('user_script', '')
        run_parameters = script and script.parameters or self.data_source.get('run_parameters', '')
        run_interpreter = script and script.interpreter or self.data_source.get('run_interpreter', 'sh')

        script_event = UserScript()
        script_event.set_timeout(run_timeout)
        script_event.set_scripttext(user_script)
        script_event.set_parameters(run_parameters)
        script_event.set_interpreter(run_interpreter)

        event_data = script_event.to_json()
        encryption, event_data = self.get_encrypt_data(event_data)

        public_event = PubEvent()
        public_event.set_event_id(sevent_uuid)
        public_event.set_encryption(encryption)
        public_event.set_event_data(event_data)
        public_event.set_event_timestamp(time.time())
        public_event.set_event_name(EventType.EXECUTESCRIPT)
        public_event.set_target_host_id(host and [host.pk] or [])
        public_event.set_target_cluster_id(cluster and [cluster.pk] or [])
        public_event.set_target_hostgroup_id(hostgroup and [hostgroup.pk] or [])

        target_hosts = self.get_execute_target(sevent_uuid, cluster, hostgroup, host)

        return public_event, target_hosts
