# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import time


from django.conf import settings
from django.contrib.auth.models import User


from .common.enhance import ExtDict
from .common.rabbitmq import RabbitMQChannelSender
from .common.models.event.pub_event import PubEvent
from .common.models.event.event_type import EventType
from .common.models.userdata.user_data import UserData
from .common.models.event.user_script import UserScript
from .models import Cluster, HostGroup, Host, Script, ScriptLog, TimedTask, UpdateLog


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


class UpdateUserDataMixin(object):
    _data_source = None
    result_model = UpdateLog
    sender_class = RabbitMQChannelSender

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, data):
        self._data_source = data

    def get_sender(self):
        return self.sender_class()

    def get_owner(self):
        ownerid = self.data_source.get('owner', 0)

        return User.objects.filter(pk=ownerid).first()

    def get_host(self):
        hostid = self.data_source.get('host', '')

        return Host.objects.filter(pk=hostid).first()

    def get_cluster(self):
        clusterid = self.data_source.get('cluster', '')

        return Cluster.objects.filter(pk=clusterid).first()

    def get_hostgroup(self):
        hostgroupid = self.data_source.get('hostgroup', '')

        return HostGroup.objects.filter(pk=hostgroupid).first()

    def get_encrypt_data(self, data):
        encryption = None

        return encryption, data

    def get_parameter_data(self):
        # maybe you need rewrite
        return {}

    def dispatch_configure(self, owner, host):
        # Reserved load balancing interface, example below
        configure = ExtDict({
            'host_id': host.pk,
            'rabbitmq_ssl': settings.CHANNEL_RABBITMQ_SSL,
            'rabbitmq_host': settings.CHANNEL_RABBITMQ_HOST,
            'rabbitmq_port': settings.CHANNEL_RABBITMQ_PORT,
            'rabbitmq_vhost': settings.CHANNEL_RABBITMQ_VHOST,
            'rabbitmq_up_queue': settings.CHANNEL_RABBITMQ_UP_QUEUE,
            'rabbitmq_auth_user': settings.CHANNEL_RABBITMQ_AUTH_USER,
            'rabbitmq_auth_pass': settings.CHANNEL_RABBITMQ_AUTH_PASS,
            'rabbitmq_down_queue': settings.CHANNEL_RABBITMQ_DOWN_QUEUE,
            'rabbitmq_up_exchange': settings.CHANNEL_RABBITMQ_UP_EXCHANGE,
            'rabbitmq_down_exchange': settings.CHANNEL_RABBITMQ_DOWN_EXCHANGE,
            'hostgroup_id': list(host.hostgroups.values_list('pk', flat=True)),
            'rabbitmq_up_routing_key': settings.CHANNEL_RABBITMQ_UP_ROUTING_KEY,
            'rabbitmq_down_routing_key': settings.CHANNEL_RABBITMQ_DOWN_ROUTING_KEY,
            'rabbitmq_up_exchange_type': settings.CHANNEL_RABBITMQ_UP_EXCHANGE_TYPE,
            'cluster_id': list(host.hostgroups.values_list('cluster__pk', flat=True)),
            'rabbitmq_down_exchange_type': settings.CHANNEL_RABBITMQ_DOWN_EXCHANGE_TYPE
        })

        return configure

    def create_public_event(self, sevent_uuid, owner, host):
        configure = self.dispatch_configure(owner, host)
        userdata_event = UserData()
        userdata_event.set_host_id(configure.host_id)
        userdata_event.set_cluster_id(configure.cluster_id)
        userdata_event.set_hostgroup_id(configure.hostgroup_id)
        userdata_event.set_rabbitmq_ssl(configure.rabbitmq_ssl)
        userdata_event.set_rabbitmq_host(configure.rabbitmq_host)
        userdata_event.set_rabbitmq_port(configure.rabbitmq_port)
        userdata_event.set_rabbitmq_vhost(configure.rabbitmq_vhost)
        userdata_event.set_rabbitmq_up_queue(configure.rabbitmq_up_queue)
        userdata_event.set_rabbitmq_auth_user(configure.rabbitmq_auth_user)
        userdata_event.set_rabbitmq_auth_pass(configure.rabbitmq_auth_pass)
        userdata_event.set_rabbitmq_down_queue(configure.rabbitmq_down_queue)
        userdata_event.set_rabbitmq_up_exchange(configure.rabbitmq_up_exchange)
        userdata_event.set_rabbitmq_down_exchange(configure.rabbitmq_down_exchange)
        userdata_event.set_rabbitmq_up_routing_key(configure.rabbitmq_up_routing_key)
        userdata_event.set_rabbitmq_down_routing_key(configure.rabbitmq_down_routing_key)
        userdata_event.set_rabbitmq_up_exchange_type(configure.rabbitmq_up_exchange_type)
        userdata_event.set_rabbitmq_down_exchange_type(configure.rabbitmq_down_exchange_type)

        event_data = userdata_event.to_json()
        encryption, event_data = self.get_encrypt_data(event_data)

        public_event = PubEvent()
        public_event.set_event_id(sevent_uuid)
        public_event.set_encryption(encryption)
        public_event.set_event_data(event_data)
        public_event.set_event_timestamp(time.time())
        public_event.set_event_name(EventType.UPDATEUSERDATA)
        public_event.set_target_host_id(host and [host.pk] or [])

        return public_event

    def get_execute_target(self, sevent_uuid, owner, cluster, hostgroup, host):
        instances_list = []
        pubevents_list = []
        parameter_dict = self.get_parameter_data()

        if host:
            parameter_dict.update({'host': host, 'sevent_uuid': sevent_uuid})
            instances_list.append(self.result_model(**parameter_dict))
            pubevents_list.append(self.create_public_event(sevent_uuid, owner, host))

            return pubevents_list, instances_list

        if hostgroup:
            for host in hostgroup.host_set.all():
                parameter_dict.update({'host': host, 'sevent_uuid': sevent_uuid})
                instances_list.append(self.result_model(**parameter_dict))
                pubevents_list.append(self.create_public_event(sevent_uuid, owner, host))

            return pubevents_list, instances_list

        if cluster:
            for hostgroup in cluster.hostgroup_set.all():
                for host in hostgroup.host_set.all():
                    parameter_dict.update({'host': host, 'sevent_uuid': sevent_uuid})
                    instances_list.append(self.result_model(**parameter_dict))
                    pubevents_list.append(self.create_public_event(sevent_uuid, owner, host))

            return pubevents_list, instances_list

    def get_instances_data(self, sevent_uuid):
        host = self.get_host()
        owner = self.get_owner()
        cluster = self.get_cluster()
        hostgroup = self.get_hostgroup()

        target_events, target_hosts = self.get_execute_target(sevent_uuid, owner, cluster, hostgroup, host)

        return target_events, target_hosts
