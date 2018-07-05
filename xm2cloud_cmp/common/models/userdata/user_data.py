#! -*- coding: utf-8 -*-


import json


from .. import BaseModel


class UserData(BaseModel):
    def __init__(self, host_id=None, cluster_id=None, hostgroup_id=None, rabbitmq_ssl=None, rabbitmq_port=None,
                 rabbitmq_vhost=None, rabbitmq_host=None, rabbitmq_auth_user=None, rabbitmq_auth_pass=None,
                 rabbitmq_up_exchange_type=None, rabbitmq_down_exchange_type=None, rabbitmq_up_exchange=None,
                 rabbitmq_down_exchange=None, rabbitmq_up_routing_key=None, rabbitmq_down_routing_key=None,
                 rabbitmq_up_queue=None, rabbitmq_down_queue=None):

        self.host_id = host_id
        self.cluster_id = cluster_id
        self.hostgroup_id = hostgroup_id
        self.rabbitmq_ssl = rabbitmq_ssl
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_vhost = rabbitmq_vhost
        self.rabbitmq_up_queue = rabbitmq_up_queue
        self.rabbitmq_auth_user = rabbitmq_auth_user
        self.rabbitmq_auth_pass = rabbitmq_auth_pass
        self.rabbitmq_down_queue = rabbitmq_down_queue
        self.rabbitmq_up_exchange = rabbitmq_up_exchange
        self.rabbitmq_down_exchange = rabbitmq_down_exchange
        self.rabbitmq_up_routing_key = rabbitmq_up_routing_key
        self.rabbitmq_down_routing_key = rabbitmq_down_routing_key
        self.rabbitmq_up_exchange_type = rabbitmq_up_exchange_type
        self.rabbitmq_down_exchange_type = rabbitmq_down_exchange_type

    def get_host_id(self):
        return self.host_id

    def set_host_id(self, host_id):
        self.host_id = host_id

    def get_cluster_id(self):
        return self.cluster_id

    def set_cluster_id(self, cluster_id):
        self.cluster_id = cluster_id

    def get_hostgroup_id(self):
        return self.hostgroup_id

    def set_hostgroup_id(self, hostgroup_id):
        self.hostgroup_id = hostgroup_id

    def get_rabbitmq_ssl(self):
        return self.rabbitmq_ssl

    def set_rabbitmq_ssl(self, rabbitmq_ssl):
        self.rabbitmq_ssl = rabbitmq_ssl

    def get_rabbitmq_host(self):
        return self.rabbitmq_host

    def set_rabbitmq_host(self, rabbitmq_host):
        self.rabbitmq_host = rabbitmq_host

    def get_rabbitmq_port(self):
        return self.rabbitmq_port

    def set_rabbitmq_port(self, rabbitmq_port):
        self.rabbitmq_port = rabbitmq_port

    def get_rabbitmq_vhost(self):
        return self.rabbitmq_vhost

    def set_rabbitmq_vhost(self, rabbitmq_vhost):
        self.rabbitmq_vhost = rabbitmq_vhost

    def get_rabbitmq_up_queue(self):
        return self.rabbitmq_up_queue

    def set_rabbitmq_up_queue(self, rabbitmq_up_queue):
        self.rabbitmq_up_queue = rabbitmq_up_queue

    def get_rabbitmq_auth_user(self):
        return self.rabbitmq_auth_user

    def set_rabbitmq_auth_user(self, rabbitmq_auth_user):
        self.rabbitmq_auth_user = rabbitmq_auth_user

    def get_rabbitmq_auth_pass(self):
        return self.rabbitmq_auth_pass

    def set_rabbitmq_auth_pass(self, rabbitmq_auth_pass):
        self.rabbitmq_auth_pass = rabbitmq_auth_pass

    def get_rabbitmq_down_queue(self):
        return self.rabbitmq_down_queue

    def set_rabbitmq_down_queue(self, rabbitmq_down_queue):
        self.rabbitmq_down_queue = rabbitmq_down_queue

    def get_rabbitmq_up_exchange(self):
        return self.rabbitmq_up_exchange

    def set_rabbitmq_up_exchange(self, rabbitmq_up_exchange):
        self.rabbitmq_up_exchange = rabbitmq_up_exchange

    def get_rabbitmq_down_exchange(self):
        return self.rabbitmq_down_exchange

    def set_rabbitmq_down_exchange(self, rabbitmq_down_exchange):
        self.rabbitmq_down_exchange = rabbitmq_down_exchange

    def get_rabbitmq_up_routing_key(self):
        return self.rabbitmq_up_routing_key

    def set_rabbitmq_up_routing_key(self, rabbitmq_up_routing_key):
        self.rabbitmq_up_routing_key = rabbitmq_up_routing_key

    def get_rabbitmq_down_routing_key(self):
        return self.rabbitmq_down_routing_key

    def set_rabbitmq_down_routing_key(self, rabbitmq_down_routing_key):
        self.rabbitmq_down_routing_key = rabbitmq_down_routing_key

    def get_rabbitmq_up_exchange_type(self):
        return self.rabbitmq_up_exchange_type

    def set_rabbitmq_up_exchange_type(self, rabbitmq_up_exchange_type):
        self.rabbitmq_up_exchange_type = rabbitmq_up_exchange_type

    def get_rabbitmq_down_exchange_type(self):
        return self.rabbitmq_down_exchange_type

    def set_rabbitmq_down_exchange_type(self, rabbitmq_down_exchange_type):
        self.rabbitmq_down_exchange_type = rabbitmq_down_exchange_type

    def to_dict(self):
        data = {
            'host_id': self.get_host_id(),
            'cluster_id': self.get_cluster_id(),
            'hostgroup_id': self.get_hostgroup_id(),
            'rabbitmq_ssl': self.get_rabbitmq_ssl(),
            'rabbitmq_host': self.get_rabbitmq_host(),
            'rabbitmq_port': self.get_rabbitmq_port(),
            'rabbitmq_vhost': self.get_rabbitmq_vhost(),
            'rabbitmq_up_queue': self.get_rabbitmq_up_queue(),
            'rabbitmq_auth_user': self.get_rabbitmq_auth_user(),
            'rabbitmq_auth_pass': self.get_rabbitmq_auth_pass(),
            'rabbitmq_down_queue': self.get_rabbitmq_down_queue(),
            'rabbitmq_up_exchange': self.get_rabbitmq_up_exchange(),
            'rabbitmq_down_exchange': self.get_rabbitmq_down_exchange(),
            'rabbitmq_up_routing_key': self.get_rabbitmq_up_routing_key(),
            'rabbitmq_down_routing_key': self.get_rabbitmq_down_routing_key(),
            'rabbitmq_up_exchange_type': self.get_rabbitmq_up_exchange_type(),
            'rabbitmq_down_exchange_type': self.get_rabbitmq_down_exchange_type()
        }

        return data

    def is_valid(self):
        return True

    @staticmethod
    def from_dict(data):
        event = UserData()
        map(lambda r: setattr(event, r[0], r[1]), data.iteritems())

        return event

    @staticmethod
    def from_json(data):
        dict_data = json.loads(data)
        event = UserData.from_dict(dict_data)

        return event
