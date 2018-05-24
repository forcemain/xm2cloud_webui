#! -*- coding: utf-8 -*-
from __future__ import division


from django.template import Library


register = Library()


@register.filter(name='hide_phone')
def hide_phone(v):
    if not v:
        return ''
    return ''.join([v[:3], '*' * 4, v[8:]])


@register.filter(name='hide_email')
def hide_email(v):
    if not v:
        return ''
    at_pre, at_nxt = v.split('@')
    end_ps = len(at_pre) // 2
    return ''.join([at_pre[:end_ps], '*' * (len(at_pre)-end_ps), '@', at_nxt])

