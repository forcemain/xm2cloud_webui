#! -*- coding: utf-8 -*-


import re


from .exception import UnSupportOperatorError


OPERATOR_MAP = {
    '=': 'eq',
    '!=': 'neq',
    '>': 'gt',
    '>=': 'ge',
    '<': 'lt',
    '<=': 'le',
    '&': 'and_',
    '|': 'or_',
    '~': 'like',
    '=~': 'regexp',
    '~=': 'iregexp',
}


class OperatorFactory(object):
    def eq(self, *args):
        return str(args[0]) == str(args[1])

    def neq(self, *args):
        return str(args[0]) != str(args[1])

    def gt(self, *args):
        return float(args[0]) > float(args[1])

    def ge(self, *args):
        return float(args[0]) >= float(args[1])

    def lt(self, *args):
        return float(args[0]) < float(args[1])

    def le(self, *args):
        return float(args[0]) <= float(args[1])

    def or_(self, *args):
        return any(args)

    def and_(self, *args):
        return all(args)

    def like(self, *args):
        return str(args[0]) in str(args[1])

    def regexp(self, *args):
        return bool(re.search(str(args[0]), str(args[1])))

    def iregexp(self, *args):
        pattern = str(args[0]).lower()
        strings = str(args[1]).lower()
        return bool(re.search(pattern, strings))

    def get_func(self, operator):
        if operator in OPERATOR_MAP:
            func_name = OPERATOR_MAP[operator]
            return getattr(self, func_name)
        err = 'trigger operator {0} no supported'.format(operator)
        raise UnSupportOperatorError(err)
