#! -*- coding: utf-8 -*-


import json


from .. import BaseModel


class PubEvent(BaseModel):
    def __init__(self, event_uuid=None, event_id=None, event_name=None, event_source='xm2cloud_webui',
                 source_version='0.0.1', source_cluster_id=None, source_hostgroup_id=None, source_host_id=None,
                 target_cluster_id=None, target_hostgroup_id=None, target_host_id=None, handled_event_id=None,
                 handled_event_cluster_id=None, handled_event_hostgroup_id=None, handled_event_host_id=None,
                 event_timestamp=None, event_data=None, encryption=None, response_code=None):

        self.event_id = event_id
        self.event_data = event_data
        self.event_name = event_name
        self.event_uuid = event_uuid
        self.encryption = encryption
        self.event_source = event_source
        self.response_code = response_code
        self.target_host_id = target_host_id
        self.source_version = source_version
        self.source_host_id = source_host_id
        self.event_timestamp = event_timestamp
        self.handled_event_id = handled_event_id
        self.target_cluster_id = target_cluster_id
        self.source_cluster_id = source_cluster_id
        self.target_hostgroup_id = target_hostgroup_id
        self.source_hostgroup_id = source_hostgroup_id
        self.handled_event_host_id = handled_event_host_id
        self.handled_event_cluster_id = handled_event_cluster_id
        self.handled_event_hostgroup_id = handled_event_hostgroup_id

    def get_event_id(self):
        return self.event_id

    def set_event_id(self, event_id):
        self.event_id = event_id

    def get_encryption(self):
        return self.encryption

    def set_encryption(self, encryption):
        self.encryption = encryption

    def get_event_data(self):
        return self.event_data

    def set_event_data(self, event_data):
        self.event_data = event_data

    def get_event_name(self):
        return self.event_name

    def set_event_name(self, event_name):
        self.event_name = event_name

    def get_event_uuid(self):
        return self.event_uuid

    def set_event_uuid(self, event_uuid):
        self.event_uuid = event_uuid

    def get_event_source(self):
        return self.event_source

    def set_event_source(self, event_source):
        self.event_source = event_source

    def get_response_code(self):
        return self.response_code

    def set_response_code(self, response_code):
        self.response_code = response_code

    def get_target_host_id(self):
        return self.target_host_id

    def set_target_host_id(self, target_host_id):
        self.target_host_id = target_host_id

    def get_source_version(self):
        return self.source_version

    def set_source_version(self, source_version):
        self.source_version = source_version

    def get_source_host_id(self):
        return self.source_host_id

    def set_source_host_id(self, source_host_id):
        self.source_host_id = source_host_id

    def get_event_timestamp(self):
        return self.event_timestamp

    def set_event_timestamp(self, event_timestamp):
        self.event_timestamp = event_timestamp

    def get_handled_event_id(self):
        return self.handled_event_id

    def set_handled_event_id(self, handled_event_id):
        self.handled_event_id = handled_event_id

    def get_target_cluster_id(self):
        return self.target_cluster_id

    def set_target_cluster_id(self, target_cluster_id):
        self.target_cluster_id = target_cluster_id

    def get_source_cluster_id(self):
        return self.source_cluster_id

    def set_source_cluster_id(self, source_cluster_id):
        self.source_cluster_id = source_cluster_id

    def get_target_hostgroup_id(self):
        return self.target_hostgroup_id

    def set_target_hostgroup_id(self, target_hostgroup_id):
        self.target_hostgroup_id = target_hostgroup_id

    def get_source_hostgroup_id(self):
        return self.source_hostgroup_id

    def set_source_hostgroup_id(self, source_hostgroup_id):
        self.source_hostgroup_id = source_hostgroup_id

    def get_handled_event_host_id(self):
        return self.handled_event_host_id

    def set_handled_event_host_id(self, handled_event_host_id):
        self.handled_event_host_id = handled_event_host_id

    def get_handled_event_cluster_id(self):
        return self.handled_event_cluster_id

    def set_handled_event_cluster_id(self, handled_event_cluster_id):
        self.handled_event_cluster_id = handled_event_cluster_id

    def get_handled_event_hostgroup_id(self):
        return self.handled_event_hostgroup_id

    def set_handled_event_hostgroup_id(self, handled_event_hostgroup_id):
        self.handled_event_hostgroup_id = handled_event_hostgroup_id

    def to_dict(self):
        data = {
            'event_id': self.get_event_id(),
            'event_data': self.get_event_data(),
            'event_name': self.get_event_name(),
            'encryption': self.get_encryption(),
            'event_uuid': self.get_event_uuid(),
            'event_source': self.get_event_source(),
            'response_code': self.get_response_code(),
            'target_host_id': self.get_target_host_id(),
            'source_version': self.get_source_version(),
            'source_host_id': self.get_source_host_id(),
            'event_timestamp': self.get_event_timestamp(),
            'handled_event_id': self.get_handled_event_id(),
            'target_cluster_id': self.get_target_cluster_id(),
            'source_cluster_id': self.get_source_cluster_id(),
            'target_hostgroup_id': self.get_target_hostgroup_id(),
            'source_hostgroup_id': self.get_source_hostgroup_id(),
            'handled_event_host_id': self.get_handled_event_host_id(),
            'handled_event_cluster_id': self.get_handled_event_cluster_id(),
            'handled_event_hostgroup_id': self.get_handled_event_hostgroup_id()
        }

        return data

    def is_valid(self):
        return True

    @staticmethod
    def from_dict(data):
        event = PubEvent()
        map(lambda r: setattr(event, r[0], r[1]), data.iteritems())

        return event

    @staticmethod
    def from_json(data):
        dict_data = json.loads(data)
        event = PubEvent.from_dict(dict_data)

        return event
