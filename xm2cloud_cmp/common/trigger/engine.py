#! -*- coding: utf-8 -*-


import json


from .function import FunctionFactory
from .operator import OperatorFactory
from .exception import InvalidTriggerRuleError
from ..models.event.triggerrule import TriggerRule


class TriggerEngine(object):
    def __init__(self, rules=None, operator_factory=None, function_factory=None):
        self._rules = rules
        self._operator_factory = operator_factory
        self._function_factory = function_factory

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, rules):
        err = None
        if not isinstance(rules, (str, unicode)):
            err = 'trigger rule must be json data'
        try:
            self._rules = json.loads(rules)
        except InvalidTriggerRuleError as e:
            err = 'trigger rule is valid, {0}'.format(e)
        if len(self._rules) < 2:
            err = 'trigger rule few operands, at least 3'
        if err:
            raise InvalidTriggerRuleError(err)

    @property
    def operator_factory(self):
        if isinstance(self._operator_factory, OperatorFactory):
            return self._operator_factory
        self._operator_factory = OperatorFactory()

        return self._operator_factory

    @property
    def function_factory(self):
        if isinstance(self._function_factory, FunctionFactory):
            return self._function_factory
        self._function_factory = FunctionFactory(self)

        return self._function_factory

    def _partical(self, **kwargs):
        rule = TriggerRule.from_dict(kwargs)
        if not rule.is_valid():
            err = 'trigger rule is valid, path,func_args,path_args,func,uuid needed'
            raise InvalidTriggerRuleError(err)
        f_name = rule.get_func()
        f = self.function_factory.get_func(f_name)

        return f(rule)

    def _evaluate(self, rules):
        def _recurse_evaluate(arg):
            if isinstance(arg, list):
                return self._evaluate(arg)
            if isinstance(arg, dict):
                return self._partical(**arg)
            return arg

        r = map(_recurse_evaluate, rules)
        f = self.operator_factory.get_func(r[0])

        return f(*r[1:])

    def evaluate(self):
        result = self._evaluate(self.rules)

        return result
