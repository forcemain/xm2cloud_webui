#! -*- coding: utf-8 -*-


from django.dispatch import Signal

host_post_save = Signal(providing_args=["instance"], use_caching=True)
hostgroup_post_save = Signal(providing_args=["instance", 'before_host_set', 'after_host_set'], use_caching=True)
cluster_post_save = Signal(providing_args=["instance", "before_hostgroup_set", "after_hostgroup_set"], use_caching=True)