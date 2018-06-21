#! -*- coding: utf-8 -*-


import json


from .. import BaseModel


class UserScript(BaseModel):
    def __init__(self, interpreter='sh', scripttext='', parameters='', timeout=300):
        self.timeout = timeout
        self.interpreter = interpreter
        self.scripttext = scripttext
        self.parameters = parameters

    def get_timeout(self):
        return self.timeout

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_interpreter(self):
        return self.interpreter

    def set_interpreter(self, interpreter):
        self.interpreter = interpreter

    def get_scripttext(self):
        return self.scripttext

    def set_scripttext(self, scripttext):
        self.scripttext = scripttext

    def get_parameters(self):
        return self.parameters

    def set_parameters(self, parameters):
        self.parameters = parameters

    def to_dict(self):
        data = {
            'timeout': self.get_timeout(),
            'scripttext': self.get_scripttext(),
            'parameters': self.get_parameters(),
            'interpreter': self.get_interpreter()
        }

        return data

    def is_valid(self):
        return True

    @staticmethod
    def from_dict(data):
        event = UserScript()
        map(lambda r: setattr(event, r[0], r[1]), data.iteritems())

        return event

    @staticmethod
    def from_json(data):
        dict_data = json.loads(data)
        event = UserScript.from_dict(dict_data)

        return event
