#! -*- coding: utf-8 -*-
from __future__ import division


from django.template import Library


register = Library()


@register.filter(name='values_list')
def values_list(v, k):
    return v.values_list(k, flat=True)
