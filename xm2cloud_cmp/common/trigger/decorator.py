#! -*- coding: utf-8 -*-

from .exception import UnSupportFunctionError


def not_implemented(func):
    def _decorator(*args, **kwargs):
        err = 'trigger function {0} no supported'.format(func.__name__)
        raise UnSupportFunctionError(err)
    return _decorator
