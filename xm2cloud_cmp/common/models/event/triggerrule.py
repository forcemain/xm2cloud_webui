#! -*- coding: utf-8 -*-


import json


from .. import BaseModel


class TriggerRule(BaseModel):
    def __init__(self, path=None, func_args=None, path_args=None, func=None, uuid=None):
        self.path = path
        self.func = func
        self.uuid = uuid
        self.func_args = func_args
        self.path_args = path_args

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def get_func(self):
        return self.func

    def set_func(self, func):
        self.func = func

    def get_uuid(self):
        return self.uuid

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_func_args(self):
        return self.func_args

    def set_func_args(self, func_args):
        self.func_args = func_args

    def get_path_args(self):
        return self.path_args

    def set_path_args(self, path_args):
        self.path_args = path_args

    def to_dict(self):
        data = {
            'path': self.get_path(),
            'func': self.get_func(),
            'uuid': self.get_uuid(),
            'func_args': self.get_func_args(),
            'path_args': self.get_path_args(),
        }

        return data

    def is_valid(self):
        return True

    @staticmethod
    def from_dict(data):
        event = TriggerRule()
        map(lambda r: setattr(event, r[0], r[1]), data.iteritems())

        return event

    @staticmethod
    def from_json(data):
        dict_data = json.loads(data)
        event = TriggerRule.from_dict(dict_data)

        return event
