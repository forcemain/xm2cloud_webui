#! -*- coding: utf-8 -*-


class TriggerError(Exception):
    pass


class MetricDataNoEnoughError(TriggerError):
    pass


class MetricKeyNotExistError(TriggerError):
    pass


class UnSupportOperatorError(TriggerError):
    pass


class UnSupportFunctionError(TriggerError):
    pass


class InvalidTriggerRuleError(TriggerError):
    pass


class UnparsedParametersError(TriggerError):
    pass


class ParametersNoEnoughError(TriggerError):
    pass
