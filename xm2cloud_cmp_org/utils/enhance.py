#! -*- coding: utf-8 -*-


class Switch(object):
    def __init__(self, v):
        self._v = v

    def __iter__(self):
        yield self.case

    def case(self, *args):
        if len(args) == 0:
            return True
        return self._v in args

