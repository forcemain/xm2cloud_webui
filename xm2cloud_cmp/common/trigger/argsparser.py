#! -*- coding: utf-8 -*-


from datetime import timedelta


from .exception import UnparsedParametersError


class ArgsParser(object):
    def nt_parse(self, value):
        if not isinstance(value, (str, unicode)):
            err = 'trigger rule args {0} unable to parse'.format(value)
            raise UnparsedParametersError(err)
        if value.startswith('#'):
            return 'nu', self.num_parse(value)
        if value.endswith('d') or \
           value.endswith('h') or \
           value.endswith('m') or \
           value.endswith('s'):
            return 'ts', self.time_shift_parse(value)
        err = 'trigger rule args {0} unable to parse'.format(value)
        raise UnparsedParametersError(err)

    def num_parse(self, value):
        if not isinstance(value, (str, unicode)) and not value.startswith('#'):
            err = 'trigger rule args {0} unable to parse'.format(value)
            raise UnparsedParametersError(err)
        u, t = value[0], value[1:]
        if not t.isdigit():
            err = 'trigger rule args {0} unable to parse'.format(value)
            raise UnparsedParametersError(err)
        v = int(t)

        return v

    def time_shift_parse(self, value):
        if not isinstance(value, (str, unicode)) and \
           not value.endswith('d') and \
           not value.endswith('h') and \
           not value.endswith('m') and \
           not value.endswith('s'):
            err = 'trigger rule args {0} unable to parse'.format(value)
            raise UnparsedParametersError(err)
        time_shift = 0
        t, u = value[:-1], value[-1]
        if not t.isdigit():
            err = 'trigger rule args time_shift {0} unable to parse'.format(value)
            raise UnparsedParametersError(err)

        v = int(t)
        if u == 'd':
            time_shift = timedelta(days=v).seconds
        if u == 'h':
            time_shift = timedelta(hours=v).seconds
        if u == 'm':
            time_shift = timedelta(minutes=v).seconds
        if u == 's':
            time_shift = timedelta(seconds=v).seconds

        return time_shift
