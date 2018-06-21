#! -*- coding: utf-8 -*-


import json


from .. import BaseModel


class HandleLog(BaseModel):
    def __init__(self, name=None, thread=None, module=None, lineno=None, message=None, process=None, asctime=None,
                 created=None, levelno=None, pathname=None, filename=None, funcname=None, levelname=None,
                 threadname=None, relativecreated=None):
        self.name = name
        self.thread = thread
        self.module = module
        self.lineno = lineno
        self.message = message
        self.process = process
        self.asctime = asctime
        self.created = created
        self.levelno = levelno
        self.pathname = pathname
        self.filename = filename
        self.funcname = funcname
        self.levelname = levelname
        self.threadname = threadname
        self.relativecreated = relativecreated

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_thread(self):
        return self.thread

    def set_thread(self, thread):
        self.thread = thread

    def get_module(self):
        return self.module

    def set_module(self, module):
        self.module = module

    def get_lineno(self):
        return self.lineno

    def set_lineno(self, lineno):
        self.lineno = lineno

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message

    def get_process(self):
        return self.process

    def set_process(self, process):
        self.process = process

    def get_asctime(self):
        return self.asctime

    def set_asctime(self, asctime):
        self.asctime = asctime

    def get_created(self):
        return self.created

    def set_created(self, created):
        self.created = created

    def get_levelno(self):
        return self.levelno

    def set_levelno(self, levelno):
        self.levelno = levelno

    def get_pathname(self):
        return self.pathname

    def set_pathname(self, pathname):
        self.pathname = pathname

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_funcname(self):
        return self.funcname

    def set_funcname(self, funcname):
        self.funcname = funcname

    def get_levelname(self):
        return self.levelname

    def set_levelname(self, levelname):
        self.levelname = levelname

    def get_threadname(self):
        return self.threadname

    def set_threadname(self, threadname):
        self.threadname = threadname

    def get_relativecreated(self):
        return self.relativecreated

    def set_relativecreated(self, relativecreated):
        self.relativecreated = relativecreated

    def to_dict(self):
        data = {
            'name': self.get_name(),
            'thread': self.get_thread(),
            'module': self.get_module(),
            'lineno': self.get_lineno(),
            'message': self.get_message(),
            'process': self.get_process(),
            'asctime': self.get_asctime(),
            'created': self.get_created(),
            'levelno': self.get_levelno(),
            'pathname': self.get_pathname(),
            'filename': self.get_filename(),
            'funcname': self.get_funcname(),
            'levelname': self.get_levelname(),
            'threadname': self.get_threadname(),
            'relativecreated': self.get_relativecreated()
        }

        return data

    def is_valid(self):
        return True

    @staticmethod
    def from_dict(data):
        event = HandleLog()
        map(lambda r: setattr(event, r[0], r[1]), data.iteritems())

        return event

    @staticmethod
    def from_json(data):
        dict_data = json.loads(data)
        event = HandleLog.from_dict(dict_data)

        return event
