#! -*- coding: utf-8 -*-


import time
import datetime


from django.conf import settings
from django_redis import get_redis_connection


from .argsparser import ArgsParser
from .decorator import not_implemented
from .exception import UnSupportFunctionError, MetricKeyNotExistError, MetricDataNoEnoughError


FUNCTION_MAP = {
    'abschange': 'abschange',
    'avg': 'avg',
    'change': 'change',
    'count': 'count',
    'date': 'date',
    'dayofmonth': 'dayofmonth',
    'dayofweek': 'dayofweek',
    'delta': 'delta',
    'diff': 'diff',
    'iregexp': 'iregexp',
    'last': 'last',
    'max': 'max',
    'min': 'min',
    'nodata': 'nodata',
    'now': 'now',
    'regexp': 'regexp',
    'strlen': 'strlen',
    'sum': 'sum',
    'time': 'time'
}


class FunctionFactory(object):
    parser = ArgsParser()
    data_source = get_redis_connection('default')

    def __init__(self, engine):
        self.engine = engine

    def combinetags(self, tags):
        combine_list = []
        for k, v in tags.iteritems():
            combine_list.append('{0}={1}'.format(k, v))
        combine_tags = '/{0}'.format(','.join(combine_list)) if combine_list else ''

        return combine_tags

    def generatekey(self, rule):
        path = rule.get_path()
        uuid = rule.get_uuid()
        path_args = rule.get_path_args()

        path_adds = self.combinetags(path_args)

        metric_key = '{0}::{1}.{2}{3}'.format(settings.MONITORING_TASK_KEY_PREFIX, uuid, path, path_adds)

        return metric_key

    def zrange_keys(self, rule, onerror=False, minkeys=1):
        keys = []
        args = rule.get_func_args()
        arg_type, arg_value = self.parser.nt_parse(args[0] if len(args) >= 1 else '5m')
        metric_key = self.generatekey(rule)
        if arg_type == 'nu':
            keys = self.data_source.zrange(metric_key, -arg_value, -1)
        if arg_type == 'ts':
            _start_ts, _stop_ts = time.time() - arg_value, time.time()
            keys = self.data_source.zrangebyscore(metric_key, _start_ts, _stop_ts)
        if not onerror:
            return keys
        if not keys or len(keys) < minkeys:
            err = 'metric key {0} with noenough data'.format(metric_key)
            raise MetricDataNoEnoughError(err)

        return keys

    def zrange_vals(self, rule, onerror=False, minkeys=1):
        keys = self.zrange_keys(rule, onerror, minkeys)
        _all = []
        for k in keys:
            v = self.data_source.hget(k, 'value') or 0
            _all.append(float(v))
        return _all

    def abschange(self, rule):
        return abs(self.change(rule))

    def avg(self, rule):
        vals = self.zrange_vals(rule, True)

        return sum(vals)/len(vals)

    def change(self, rule):
        keys = self.zrange_keys(rule, True, 2)
        _start_key, _stop_key = keys[0], keys[-1]
        _start_val, _stop_val = map(lambda k: self.data_source.hget(k, 'value'), (_start_key, _stop_key))
        if _start_val is None:
            err = 'metric key {0} not exist'.format(_start_key)
            raise MetricKeyNotExistError(err)
        if _stop_val is None:
            err = 'metric key {0} not exist'.format(_stop_key)
            raise MetricKeyNotExistError(err)
        if _start_val.isdigit() and _stop_val.isdigit():
            return float(_stop_val) - float(_start_val)
        return 0 if _start_val == _stop_val else 1

    def count(self, rule):
        keys = self.zrange_keys(rule, True)
        _num = 0
        args = rule.get_func_args()
        pattern = args[1] if len(args) >= 2 else '.*'
        operator = args[2] if len(args) >= 3 else 'regexp'
        f = self.engine.operator_factory.get_func(operator)
        for k in keys:
            v = self.data_source.hget(k, 'value')
            if f(pattern, v):
                _num += 1
        return _num

    def date(self, rule):
        d = datetime.date.today()

        return d.strftime('%Y%m%d')

    def dayofmonth(self, rule):
        d = datetime.date.today()

        return d.day

    def dayofweek(self, rule):
        d = datetime.date.today()

        return d.isoweekday()

    def delta(self, rule):
        vals = self.zrange_vals(rule, True)

        return max(vals) - min(vals)

    def diff(self, rule):
        return 1 if self.change(rule) else 0

    def iregexp(self, rule):
        keys = self.zrange_keys(rule, True)
        _iok = 0
        args = rule.get_func_args()
        pattern = args[1] if len(args) >= 2 else '.*'
        operator = args[2] if len(args) >= 3 else 'iregexp'
        f = self.engine.operator_factory.get_func(operator)
        for k in keys:
            v = self.data_source.hget(k, 'value')
            if f(pattern, v):
                _iok = 1
                break
        return _iok

    def last(self, rule):
        _start_key = self.zrange_keys(rule, True)[0]
        _start_val = self.data_source.hget(_start_key, 'value')
        if _start_val is None:
            err = 'metric key {0} not exist'.format(_start_key)
            raise MetricKeyNotExistError(err)
        return _start_val

    def max(self, rule):
        vals = self.zrange_vals(rule, True)

        return max(vals)

    def min(self, rule):
        vals = self.zrange_vals(rule, True)

        return min(vals)

    def nodata(self, rule):
        keys = self.zrange_keys(rule, False)

        return 1 if not keys else 0

    def now(self, rule):
        return time.time()

    def regexp(self, rule):
        keys = self.zrange_keys(rule, True)
        _iok = 0
        args = rule.get_func_args()
        pattern = args[1] if len(args) >= 2 else '.*'
        operator = args[2] if len(args) >= 3 else 'regexp'
        f = self.engine.operator_factory.get_func(operator)
        for k in keys:
            v = self.data_source.hget(k, 'value')
            if f(pattern, v):
                _iok = 1
                break
        return _iok

    def strlen(self, rule):
        return len(self.last(rule))

    def sum(self, rule):
        vals = self.zrange_vals(rule, True)

        return sum(vals)

    def time(self, rule):
        t = time.localtime()

        return time.strftime('%H%M%S', t)

    def get_func(self, funcname):
        if funcname in FUNCTION_MAP:
            func_name = FUNCTION_MAP[funcname]
            return getattr(self, func_name)
        err = 'trigger function {0} no supported'.format(funcname)
        raise UnSupportFunctionError(err)

