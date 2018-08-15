# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import json
import base64


from django.conf import settings
from django.db.models import Q, Count
from django.http.response import JsonResponse
from django_redis import get_redis_connection
from urllib3.exceptions import ReadTimeoutError
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import classonlymethod
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from djcelery.models import IntervalSchedule, CrontabSchedule
from django.views.generic import TemplateView, DetailView, View


from .tasks import ExecutorTimedTask
from .common.models.userdata.user_data import UserData
from .base import JSONListView, JSONCreateView, JSONDeleteView, JSONUpdateView
from .signal import model_task, host_post_save, hostgroup_post_save, cluster_post_save
from .models import (Cluster, Host, IpLine, IpLinePackage, Continent, HostGroup, AlertContactGroup, DashBoardScreen,
                     Manufacturer, Region, OemInfo, OperatingSystem, Script, ScriptGroup, ScriptLog, TimedTask,
                     TaskWorkFlow, WorkFlowTask, DashBoardScreenTarget, AlarmStrategyGroup, AlarmStrategy, AlarmHistory,
                     MessageTopic)


class QuerySetProxy(list):
    def __init__(self, v):
        super(QuerySetProxy, self).__init__([])
        self.extend(v)

    def count(self):
        return len(self)


class LoginRequiredMixin(object):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/home.html'

    def get_context_data(self, **kwargs):
        ocontext = super(HomeView, self).get_context_data(**kwargs)
        info_objects = {}

        continents = Continent.objects.all()
        manufacturers = Manufacturer.objects.all()

        for continent in continents:
            continent_kwargs = {'area__continent': continent}
            continent_result = Host.objects.filter(**continent_kwargs).values_list('area__continent__pk',
                                                                                   'area__continent__name')
            continent_key = continent_result.annotate(Count('area__continent__pk'))
            info_objects.setdefault(continent_key, {})
            for manufacturer in manufacturers:
                region_kwargs = manufacturer_kwargs = {'firm': manufacturer, 'area__continent': continent}
                manufacturer_result = Host.objects.filter(**manufacturer_kwargs).values_list('firm__pk', 'firm__name')
                manufacturer_key = manufacturer_result.annotate(Count('firm__pk'))
                region_result = Host.objects.filter(**region_kwargs).values_list('area__pk', 'area__name')
                info_objects[continent_key].setdefault(manufacturer_key, region_result.annotate(Count('area__pk')))

        ocontext.update({'info_objects': info_objects})

        return ocontext


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
        })

        return context


class AgentInstallView(LoginRequiredMixin, DetailView):
    model = Host
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/agent_install.html'

    def get_user_data(self):
        user_data = UserData(
            host_id=self.object.pk,
            rabbitmq_ssl=settings.CHANNEL_RABBITMQ_SSL,
            rabbitmq_host=settings.CHANNEL_RABBITMQ_HOST,
            rabbitmq_port=settings.CHANNEL_RABBITMQ_PORT,
            rabbitmq_vhost=settings.CHANNEL_RABBITMQ_VHOST,
            rabbitmq_up_queue=settings.CHANNEL_RABBITMQ_UP_QUEUE,
            rabbitmq_auth_user=settings.CHANNEL_RABBITMQ_AUTH_USER,
            rabbitmq_auth_pass=settings.CHANNEL_RABBITMQ_AUTH_PASS,
            rabbitmq_down_queue=settings.CHANNEL_RABBITMQ_DOWN_QUEUE,
            rabbitmq_up_exchange=settings.CHANNEL_RABBITMQ_UP_EXCHANGE,
            rabbitmq_down_exchange=settings.CHANNEL_RABBITMQ_DOWN_EXCHANGE,
            rabbitmq_up_routing_key=settings.CHANNEL_RABBITMQ_UP_ROUTING_KEY,
            rabbitmq_down_routing_key=settings.CHANNEL_RABBITMQ_DOWN_ROUTING_KEY,
            rabbitmq_up_exchange_type=settings.CHANNEL_RABBITMQ_UP_EXCHANGE_TYPE,
            hostgroup_id=list(self.object.hostgroups.values_list('pk', flat=True)),
            rabbitmq_down_exchange_type=settings.CHANNEL_RABBITMQ_DOWN_EXCHANGE_TYPE,
            cluster_id=list(self.object.hostgroups.values_list('cluster__pk', flat=True))
        )

        return user_data

    def get_context_data(self, **kwargs):
        user_data = self.get_user_data()
        context = super(AgentInstallView, self).get_context_data(**kwargs)
        context.update({
            'userdata': user_data.to_json()
        })

        return context


class ClusterListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/clusters.html'

    def get_context_data(self, **kwargs):
        context = super(ClusterListView, self).get_context_data(**kwargs)
        context.update({})

        return context


class ClusterCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/cluster_create.html'

    def get_context_data(self, **kwargs):
        context = super(ClusterCreateView, self).get_context_data(**kwargs)
        context.update({
            'hostgroups': HostGroup.objects.all()
        })

        return context


class ClusterUpdateView(LoginRequiredMixin, DetailView):
    model = Cluster
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/cluster_update.html'

    def get_context_data(self, **kwargs):
        context = super(ClusterUpdateView, self).get_context_data(**kwargs)
        context.update({
            'hostgroups': HostGroup.objects.all()
        })

        return context


class ClusterDeleteView(LoginRequiredMixin, DetailView):
    model = Cluster
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/cluster_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ClusterDeleteView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class ClusterDetailView(LoginRequiredMixin, DetailView):
    model = Cluster
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/cluster_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClusterDetailView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class ClusterManageView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/cluster_manage.html'

    def get_context_data(self, **kwargs):
        context = super(ClusterManageView, self).get_context_data(**kwargs)
        context.update({})

        return context


class ClusterApiListView(LoginRequiredMixin, JSONListView):
    model = Cluster

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        clusterid, clustersearch = map(
            lambda field: self.request.GET.get(field, None),
            ['clusterId', 'clusterSearch']
        )
        queryset = super(ClusterApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if clusterid is not None:
            queryset = queryset.filter(pk=clusterid)
            return queryset.order_by(order_by_field)

        if clustersearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=clustersearch),
                Q(notes__contains=clustersearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page-1)*rows, page*rows

    def get_data(self, **context):
        context = super(ClusterApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'hostgroups': obj.hostgroup_set.count(),
                'update_time': obj.update_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return results


class ClusterApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = Cluster
    fields = ['name', 'notes']

    def get_hostgroup_set(self):
        hostgroup_ids = self.request.POST.getlist('hostgroup_set', [])

        return HostGroup.objects.filter(pk__in=hostgroup_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        hostgroup_set = self.get_hostgroup_set()
        self.object.hostgroup_set.add(*hostgroup_set.all())
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class ClusterApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = Cluster
    pk_url_kwarg = 'id'
    fields = ['name', 'notes']

    def get_hostgroup_set(self):
        hostgroup_ids = self.request.POST.getlist('hostgroup_set', [])

        return HostGroup.objects.filter(pk__in=hostgroup_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.hostgroup_set.update(cluster=None)
        hostgroup_set = self.get_hostgroup_set()
        self.object.hostgroup_set.add(*hostgroup_set.all())
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class ClusterApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Cluster
    pk_url_kwarg = 'id'


class HostgroupListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/hostgroups.html'

    def get_context_data(self, **kwargs):
        context = super(HostgroupListView, self).get_context_data(**kwargs)
        context.update({
            'clusters': Cluster.objects.all(),
            'clusterid': self.request.GET.get('clusterId')
        })
        return context


class HostgroupCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/hostgroup_create.html'

    def get_context_data(self, **kwargs):
        context = super(HostgroupCreateView, self).get_context_data(**kwargs)
        context.update({
            'hosts': Host.objects.all(),
            'clusters': Cluster.objects.all(),
            'alertcontactgroups': AlertContactGroup.objects.all(),
        })

        return context


class HostgroupUpdateView(LoginRequiredMixin, DetailView):
    model = HostGroup
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/hostgroup_update.html'

    def get_context_data(self, **kwargs):
        context = super(HostgroupUpdateView, self).get_context_data(**kwargs)
        context.update({
            'hosts': Host.objects.all(),
            'clusters': Cluster.objects.all(),
            'alertcontactgroups': AlertContactGroup.objects.all(),
        })

        return context


class HostgroupDeleteView(LoginRequiredMixin, DetailView):
    model = HostGroup
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/hostgroup_delete.html'

    def get_context_data(self, **kwargs):
        context = super(HostgroupDeleteView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class HostgroupDetailView(LoginRequiredMixin, DetailView):
    model = HostGroup
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/hostgroup_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HostgroupDetailView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class HostgroupManageView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/hostgroup_manage.html'

    def get_context_data(self, **kwargs):
        context = super(HostgroupManageView, self).get_context_data(**kwargs)
        context.update({})

        return context


class HostgroupApiListView(LoginRequiredMixin, JSONListView):
    model = HostGroup

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        clusterid, hostgroupid, hostid, hostgroupsearch = map(
            lambda field: self.request.GET.get(field, None),
            ['clusterId', 'hostgroupId', 'hostId', 'hostgroupSearch']
        )
        queryset = super(HostgroupApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if hostgroupid is not None:
            queryset = queryset.filter(pk=hostgroupid)
            return queryset.order_by(order_by_field)

        if clusterid is not None:
            queryset = queryset.filter(cluster__pk=clusterid)

        if hostid is not None:
            queryset = queryset.filter(host__pk=hostid)

        if hostgroupsearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=hostgroupsearch),
                Q(notes__contains=hostgroupsearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page-1)*rows, page*rows

    def get_data(self, **context):
        context = super(HostgroupApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'hosts': obj.host_set.count(),
                'update_time': obj.update_time.strftime('%Y-%m-%d %H:%S:%M')
            })

        return results


class HostgroupApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = HostGroup
    before_host_set = set()
    fields = ['name', 'notes', 'cluster', 'alertcontactgroup']

    def get_host_set(self):
        host_ids = self.request.POST.getlist('host_set', [])

        return Host.objects.filter(pk__in=host_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.host_set = self.get_host_set()
        self.object.save()
        after_host_set = set(self.object.host_set.values_list('pk', flat=True))

        hostgroup_post_save.send(sender=self.model, instance=self.object,
                                 after_host_set=after_host_set,
                                 before_host_set=self.before_host_set)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class HostgroupApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = HostGroup
    pk_url_kwarg = 'id'
    before_host_set = []
    fields = ['name', 'notes', 'cluster', 'alertcontactgroup']

    def get_host_set(self):
        host_ids = self.request.POST.getlist('host_set', [])

        return Host.objects.filter(pk__in=host_ids)

    def post(self, request, *args, **kwargs):
        self.before_host_set = set(self.get_object().host_set.values_list('pk', flat=True))
        return super(HostgroupApiUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.host_set = self.get_host_set()
        self.object.save()
        after_host_set = set(self.object.host_set.values_list('pk', flat=True))

        hostgroup_post_save.send(sender=self.model, instance=self.object,
                                 after_host_set=after_host_set,
                                 before_host_set=self.before_host_set)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class HostgroupApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = HostGroup
    pk_url_kwarg = 'id'


class HostListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/hosts.html'

    def get_context_data(self, **kwargs):
        context = super(HostListView, self).get_context_data(**kwargs)
        context.update({
            'clusters': Cluster.objects.all(),
            'hostgroups': HostGroup.objects.all(),
            'continents': Continent.objects.all(),
            'clusterid': self.request.GET.get('clusterId'),
            'hostgroupid': self.request.GET.get('hostgroupId'),
            'continentid': self.request.GET.get('continentId')
        })
        return context


class HostCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/host_create.html'

    def get_context_data(self, **kwargs):
        context = super(HostCreateView, self).get_context_data(**kwargs)
        context.update({
            'oems': OemInfo.objects.all(),
            'areas': Region.objects.all(),
            'iplines': IpLine.objects.all(),
            'firms': Manufacturer.objects.all(),
            'hostgroups': HostGroup.objects.all(),
            'vmoses': OperatingSystem.objects.all()
        })

        return context


class HostDetailView(LoginRequiredMixin, DetailView):
    model = Host
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/host_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HostDetailView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class HostUpdateView(LoginRequiredMixin, DetailView):
    model = Host
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/host_update.html'

    def get_context_data(self, **kwargs):
        context = super(HostUpdateView, self).get_context_data(**kwargs)
        context.update({
            'oems': OemInfo.objects.all(),
            'areas': Region.objects.all(),
            'iplines': IpLine.objects.all(),
            'firms': Manufacturer.objects.all(),
            'hostgroups': HostGroup.objects.all(),
            'vmoses': OperatingSystem.objects.all()
        })

        return context


class HostDeleteView(LoginRequiredMixin, DetailView):
    model = Host
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/host_delete.html'

    def get_context_data(self, **kwargs):
        context = super(HostDeleteView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class HostManageView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/host_manage.html'

    def get_context_data(self, **kwargs):
        context = super(HostManageView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class HostApiListView(LoginRequiredMixin, JSONListView):
    model = Host

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        hostid, iplineid, regionid, hostgroupid, continentid, manufacturerid, hostsearch = map(
            lambda field: self.request.GET.get(field, None),
            ['hostId', 'iplineId', 'regionId', 'hostgroupId', 'continentId', 'manufacturerId', 'hostSearch']
        )
        queryset = super(HostApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if hostid is not None:
            queryset = queryset.filter(pk=hostid)
            return queryset.order_by(order_by_field)

        if regionid is not None:
            queryset = queryset.filter(area__pk=regionid)

        if iplineid is not None:
            queryset = queryset.filter(ipline__pk=iplineid)

        if manufacturerid is not None:
            queryset = queryset.filter(firm__pk=manufacturerid)

        if continentid is not None:
            queryset = queryset.filter(area__continent__pk=continentid)

        if hostgroupid is not None:
            queryset = queryset.filter(hostgroups__pk=hostgroupid).distinct()

        if hostsearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=hostsearch),
                Q(notes__contains=hostsearch),
                Q(ipline__ip__contains=hostsearch),
                Q(area__name__contains=hostsearch),
                Q(firm__name__contains=hostsearch),
                Q(area__continent__name__contains=hostsearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_context_data(self, **kwargs):
        is_running, is_outdate, is_overdue, is_unusual = map(
            lambda field: self.request.GET.get(field, None),
            ['isRunning', 'isOutdate', 'isOverdue', 'isUnusual']
        )
        context = super(HostApiListView, self).get_context_data(**kwargs)

        if any([is_running, is_outdate, is_overdue, is_unusual]):
            object_list = QuerySetProxy([])
            for obj in context['object_list']:
                if (is_running is not None and obj.is_running()) or \
                   (is_outdate is not None and obj.is_outdate()) or \
                   (is_overdue is not None and obj.is_overdue()) or \
                   (is_unusual is not None and obj.is_unusual()):
                    object_list.append(obj)
            context['object_list'] = object_list

        return context

    def get_data(self, **context):
        context = self.get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]
        for obj in objects_list:
            ins = {
                'id': obj.pk,
                'name': obj.name,
                'vmcpu': obj.vmcpu,
                'vmmem': obj.vmmem,
                'vmos': obj.vmos.name,
                'is_running': obj.is_running(),
                'is_outdate': obj.is_outdate(),
                'is_overdue': obj.is_overdue(),
                'is_unusual': obj.is_unusual(),
                'agentstate': obj.agentstate(),
                'binds': obj.ipline_set.count(),
                'hostgroups': obj.hostgroups.count(),
                'expiry_time': obj.expiry_time.strftime('%Y-%m-%d %H:%M'),
            }
            results['rows'].append(ins)

        return results


class HostApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = Host
    fields = ['name', 'vmcpu', 'vmmem', 'notes', 'bill_method', 'expiry_time', 'area', 'firm', 'oems', 'vmos', 'hostgroups']

    def get_ipline_set(self):
        ipline_ids = self.request.POST.getlist('ipline_set', [])

        return IpLine.objects.filter(pk__in=ipline_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.ipline_set = self.get_ipline_set()
        self.object.save()
        host_post_save.send(sender=self.model, instance=self.object)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class HostApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = Host
    pk_url_kwarg = 'id'
    fields = ['name', 'vmcpu', 'vmmem', 'notes', 'bill_method', 'expiry_time', 'area', 'firm', 'oems', 'vmos', 'hostgroups']

    def get_ipline_set(self):
        ipline_ids = self.request.POST.getlist('ipline_set', [])

        return IpLine.objects.filter(pk__in=ipline_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.ipline_set = self.get_ipline_set()
        self.object.save()
        host_post_save.send(sender=self.model, instance=self.object)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class HostApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Host
    pk_url_kwarg = 'id'


class MonitorMetricsApiBaseView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(MonitorMetricsApiBaseView, self).dispatch(request, *args, **kwargs)

    def get_dataurl(self, uri):
        return '{0}://{1}:{2}/api/{3}'.format(settings.BACKEND_OPENTSDB_PROTOCOL, settings.BACKEND_OPENTSDB_HOST,
                                              settings.BACKEND_OPENTSDB_PORT, uri)

    def get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if not settings.BACKEND_OPENTSDB_USERNAME or not settings.BACKEND_OPENTSDB_PASSWORD:
            return headers
        _encode_auth = base64.b64encode('{0}:{1}'.format(settings.BACKEND_OPENTSDB_USERNAME,
                                                         settings.BACKEND_OPENTSDB_PASSWORD))
        _authorization = 'Basic {0}'.format(_encode_auth)
        headers.update({'Authorization': _authorization})

        return headers


class MonitorMetricsApiQueryView(MonitorMetricsApiBaseView):
    def post(self, request, *args, **kwargs):
        dataurl = self.get_dataurl('query')
        headers = self.get_headers()

        try:
            r = settings.HTTP_POOL.request('POST', dataurl, body=request.body, headers=headers)
            data = json.loads(r.data)
        except ReadTimeoutError:
            data = []
        return JsonResponse(data, safe=False)


class MonitorMetricsApiSuggestView(MonitorMetricsApiBaseView):
    def get(self, request, *args, **kwargs):
        results = []
        q = request.GET.get('q', '')
        fields = {
            'q': q.split(',')[-1],
            'max': request.GET.get('max', 15),
            'type': request.GET.get('type', 'metrics')
        }

        dataurl = self.get_dataurl('suggest')
        headers = self.get_headers()

        try:
            r = settings.HTTP_POOL.request('GET', dataurl, fields=fields, headers=headers)
            data = json.loads(r.data)
        except ReadTimeoutError:
            data = []
        map(lambda obj: results.append({'id': obj, 'name': obj}), data)
        return JsonResponse(results, safe=False)


class IpLineListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/iplines.html'

    def get_context_data(self, **kwargs):
        context = super(IpLineListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class IpLineCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/ipline_create.html'

    def get_context_data(self, **kwargs):
        context = super(IpLineCreateView, self).get_context_data(**kwargs)
        context.update({
            'hosts': Host.objects.all(),
            'iplinepackages': IpLinePackage.objects.all()
        })

        return context


class IpLineUpdateView(LoginRequiredMixin, DetailView):
    model = IpLine
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/ipline_update.html'

    def get_context_data(self, **kwargs):
        context = super(IpLineUpdateView, self).get_context_data(**kwargs)
        context.update({
            'hosts': Host.objects.all(),
            'iplinepackages': IpLinePackage.objects.all()
        })

        return context


class IpLineDeleteView(LoginRequiredMixin, DetailView):
    model = IpLine
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/ipline_delete.html'

    def get_context_data(self, **kwargs):
        context = super(IpLineDeleteView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class IpLineDetailView(LoginRequiredMixin, DetailView):
    model = IpLine
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/ipline_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IpLineDetailView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class IpLineApiListView(LoginRequiredMixin, JSONListView):
    model = IpLine

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        iplineid, hostid, iplinepackageid, iplinesearch = map(
            lambda field: self.request.GET.get(field, None),
            ['iplineId', 'hostId', 'iplinepackageId', 'iplineSearch']
        )
        queryset = super(IpLineApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if iplineid is not None:
            queryset = queryset.filter(pk=iplineid)
            return queryset.order_by(order_by_field)

        if hostid is not None:
            queryset = queryset.filter(host__pk=hostid)

        if iplinepackageid is not None:
            queryset = queryset.filter(package__pk=iplinepackageid)

        if iplinesearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(ip__contains=iplinesearch),
                Q(line__contains=iplinesearch),
                Q(notes__contains=iplinesearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page-1)*rows, page*rows

    def get_data(self, **context):
        context = super(IpLineApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'ip': obj.ip,
                'line': obj.line,
                'band': obj.band,
                'notes': obj.notes,
                'host_id': obj.host and obj.host.pk or None,
                'host_name': obj.host and obj.host.name or None,
                'package_id': obj.package and obj.package.pk or None,
                'package_band': obj.package and obj.package.band or None,
                'package_name': obj.package and obj.package.name or None,
                'update_time': obj.update_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return results


class IpLineApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = IpLine
    fields = ['band', 'is_preferred', 'ip', 'notes', 'line', 'host', 'package']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class IpLineApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = IpLine
    pk_url_kwarg = 'id'
    fields = ['band', 'is_preferred', 'ip', 'notes', 'line', 'host', 'package']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class IpLineApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = IpLine
    pk_url_kwarg = 'id'


class IpLinePackageListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/iplinepackages.html'

    def get_context_data(self, **kwargs):
        context = super(IpLinePackageListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class IpLinePackageCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/iplinepackage_create.html'

    def get_context_data(self, **kwargs):
        context = super(IpLinePackageCreateView, self).get_context_data(**kwargs)
        context.update({
            'iplines': IpLine.objects.all()
        })
        return context


class IpLinePackageUpdateView(LoginRequiredMixin, DetailView):
    model = IpLinePackage
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/iplinepackage_update.html'

    def get_context_data(self, **kwargs):
        context = super(IpLinePackageUpdateView, self).get_context_data(**kwargs)
        context.update({
            'iplines': IpLine.objects.all()
        })
        return context


class IpLinePackageDeleteView(LoginRequiredMixin, DetailView):
    model = IpLinePackage
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/iplinepackage_delete.html'

    def get_context_data(self, **kwargs):
        context = super(IpLinePackageDeleteView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class IpLinePackageDetailView(LoginRequiredMixin, DetailView):
    model = IpLinePackage
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/iplinepackage_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IpLinePackageDetailView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class IpLinePackageApiListView(LoginRequiredMixin, JSONListView):
    model = IpLinePackage

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        iplinepackageid, iplineid, iplinepackagesearch = map(
            lambda field: self.request.GET.get(field, None),
            ['iplinePackageId', 'iplineId', 'iplinePackageSearch']
        )
        queryset = super(IpLinePackageApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if iplinepackageid is not None:
            queryset = queryset.filter(pk=iplinepackageid)
            return queryset.order_by(order_by_field)

        if iplineid is not None:
            queryset = queryset.filter(ipline__pk=iplineid)

        if iplinepackagesearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=iplinepackagesearch),
                Q(notes__contains=iplinepackagesearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(IpLinePackageApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'band': obj.band,
                'line': obj.line,
                'notes': obj.notes,
                'iplines': obj.ipline_set.count(),
                'update_time': obj.update_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return results


class IpLinePackageApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = IpLinePackage
    fields = ['band', 'name', 'line', 'notes']

    def get_ipline_set(self):
        ipline_ids = self.request.POST.getlist('ipline_set', [])

        return IpLine.objects.filter(pk__in=ipline_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.ipline_set = self.get_ipline_set()
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class IpLinePackageApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = IpLinePackage
    pk_url_kwarg = 'id'
    fields = ['band', 'name', 'line', 'notes']

    def get_ipline_set(self):
        ipline_ids = self.request.POST.getlist('ipline_set', [])

        return IpLine.objects.filter(pk__in=ipline_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.ipline_set = self.get_ipline_set()
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class IpLinePackageApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = IpLinePackage
    pk_url_kwarg = 'id'


class ScriptListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/scripts.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class ScriptCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/script_create.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptCreateView, self).get_context_data(**kwargs)
        context.update({
            'scriptgroups': ScriptGroup.objects.all()
        })
        return context


class ScriptUpdateView(LoginRequiredMixin, DetailView):
    model = Script
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/script_update.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptUpdateView, self).get_context_data(**kwargs)
        context.update({
            'scriptgroups': ScriptGroup.objects.all()
        })
        return context


class ScriptDetailView(LoginRequiredMixin, DetailView):
    model = Script
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/script_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptDetailView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class ScriptDeleteView(LoginRequiredMixin, DetailView):
    model = Script
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/script_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptDeleteView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class ScriptManageView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/script_manage.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptManageView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class ScriptExecuteView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/script_execute.html'

    def get_context_extra(self):
        clusterid, hostgroupid, hostid, scriptid = map(
            lambda k: self.request.GET.get(k, None),
            ['clusterId', 'hostgroupId', 'hostId', 'scriptId']
        )
        context = {
            'host': HostGroup.objects.filter(pk=hostid).first(),
            'script': Script.objects.filter(pk=scriptid).first(),
            'cluster': Cluster.objects.filter(pk=clusterid).first(),
            'hostgroup': HostGroup.objects.filter(pk=hostgroupid).first()
        }
        return context

    def get_context_data(self, **kwargs):
        context = super(ScriptExecuteView, self).get_context_data(**kwargs)
        context_extra = self.get_context_extra()
        context.update(context_extra)

        return context


class ScriptApiListView(LoginRequiredMixin, JSONListView):
    model = Script

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        scriptid, scriptsearch = map(
            lambda field: self.request.GET.get(field, None),
            ['scriptId', 'scriptSearch']
        )
        queryset = super(ScriptApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if scriptid is not None:
            queryset = queryset.filter(pk=scriptid)
            return queryset.order_by(order_by_field)

        if scriptsearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=scriptsearch),
                Q(notes__contains=scriptsearch),
                Q(scriptgroup__name__contains=scriptsearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(ScriptApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'contents': obj.contents,
                'platform': obj.platform,
                'interpreter': obj.interpreter,
                'update_time': obj.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                'scriptgroup': obj.scriptgroup and obj.scriptgroup.name or None,
            })

        return results


class ScriptApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = Script
    fields = ['contents', 'name', 'parameters', 'notes', 'interpreter', 'platform', 'scriptgroup', 'owner', 'timeout']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class ScriptApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = Script
    pk_url_kwarg = 'id'
    fields = ['contents', 'name', 'parameters', 'notes', 'interpreter', 'platform', 'scriptgroup', 'owner', 'timeout']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class ScriptApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Script
    pk_url_kwarg = 'id'


class ScriptLogListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/script_logs.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptLogListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class ScriptLogManageView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/script_log_manage.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptLogManageView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class ScriptLogApiListView(LoginRequiredMixin, JSONListView):
    model = ScriptLog

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        clusterid, hostgroupid, hostid, scriptid, triggermode, timedtaskid = map(
            lambda field: self.request.GET.get(field, None),
            ['clusterId', 'hostgroupId', 'hostId', 'scriptId', 'triggerMode', 'timedtaskId']
        )
        queryset = super(ScriptLogApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()
        condition_and_list = Q()
        if hostid:
            condition_and_list.add(Q(host__pk=hostid), Q.AND)
        if scriptid:
            condition_and_list.add(Q(script__pk=scriptid), Q.AND)
        if clusterid:
            condition_and_list.add(Q(cluster__pk=clusterid), Q.AND)
        if triggermode:
            condition_and_list.add(Q(triggermode=triggermode), Q.AND)
        if hostgroupid:
            condition_and_list.add(Q(hostgroup__pk=hostgroupid), Q.AND)
        if timedtaskid:
            condition_and_list.add(Q(timedtask__sevent_uuid=timedtaskid), Q.AND)

        queryset = queryset.filter(condition_and_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_context_data(self, **kwargs):
        reqtaskstate = int(self.request.GET.get('taskState', 1000))
        context = super(ScriptLogApiListView, self).get_context_data(**kwargs)

        if reqtaskstate == 1000:
            return context
        object_list = QuerySetProxy([])
        for obj in context['object_list']:
            rsptaskstate = obj.task_state()
            if reqtaskstate != rsptaskstate:
                continue
            object_list.append(obj)
            context['object_list'] = object_list

        return context

    def get_data(self, **context):
        context = super(ScriptLogApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            rsptaskstate = obj.task_state()
            results['rows'].append({
                'id': obj.pk,
                'host_id': obj.host.pk,
                'task_state': rsptaskstate,
                'host_name': obj.host.name,
                'cluster_id': obj.cluster.pk,
                'sevent_uuid': obj.sevent_uuid,
                'user_script': obj.user_script,
                'triggermode': obj.triggermode,
                'script_name': obj.script_name,
                'run_timeout': obj.run_timeout,
                'hostgroup_id': obj.hostgroup.pk,
                'cluster_name': obj.cluster.name,
                'run_parameters': obj.run_parameters,
                'hostgroup_name': obj.hostgroup.name,
                'run_interpreter': obj.run_interpreter,
                'script_id': obj.script and obj.script.pk or None,
                'create_time': obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return results


class ScriptLogApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = ScriptLog
    fields = ['triggermode', 'host', 'script', 'cluster', 'hostgroup', 'user_script', 'owner', 'script_name',
              'sevent_uuid', 'run_timeout', 'run_parameters', 'run_interpreter', 'run_platform']

    @staticmethod
    def valid_cluster(request):
        clusterid = request.POST.get('cluster', '')

        return Cluster.objects.filter(pk=clusterid).exists()

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_cluster(request) is False:
            form_errors.append('The field is required.')
            return JsonResponse({'cluster': form_errors}, status=403)
        return super(ScriptLogApiCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('xm2cloud_cmp:script_log_manage')

    def get_owner(self):
        owner = super(ScriptLogApiCreateView, self).get_owner()
        return owner or self.request.user

    def get_parameter_data(self):
        triggermode = 0
        owner = self.get_owner()
        script = self.get_script()
        script_name = script and script.name or u'自定义脚本'
        user_script = script and script.contents or self.data_source.get('user_script', '')

        return {
            'owner': owner, 'script': script, 'script_name': script_name, 'triggermode': triggermode,
            'user_script': user_script
        }

    def form_valid(self, form):
        from celery.registry import tasks
        func = tasks[ExecutorTimedTask.name]

        func.delay(owner=self.request.user.pk, **self.request.POST.dict())

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class ScriptLogApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = ScriptLog
    pk_url_kwarg = 'id'


class ScriptLogApiResultView(LoginRequiredMixin, View):
    def get(self, request):
        event_id, host_id = map(lambda k: request.GET.get(k, None), ['eventId', 'hostId'])
        rds = get_redis_connection('default')
        key = '{0}::{1}::{2}'.format(settings.LOGGING_TASK_VAL_PREFIX, event_id, host_id)
        val = rds.zrange(key, 0, -1)

        return JsonResponse(val, status=200, safe=False)


class TimedTaskListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/timedtasks.html'

    def get_context_data(self, **kwargs):
        context = super(TimedTaskListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TimedTaskCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/timedtask_create.html'

    def get_context_data(self, **kwargs):
        context = super(TimedTaskCreateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TimedTaskUpdateView(LoginRequiredMixin, DetailView):
    model = TimedTask
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'
    template_name = 'xm2cloud_cmp/timedtask_update.html'

    def get_context_data(self, **kwargs):
        context = super(TimedTaskUpdateView, self).get_context_data(**kwargs)
        context.update({
            'hosts': Host.objects.all(),
            'scripts': Script.objects.all(),
            'clusters': Cluster.objects.all(),
            'hostgroups': HostGroup.objects.all(),
            'crontabs': CrontabSchedule.objects.all(),
            'intervals': IntervalSchedule.objects.all()
        })
        return context


class TimedTaskDetailView(LoginRequiredMixin, DetailView):
    model = TimedTask
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'
    template_name = 'xm2cloud_cmp/timedtask_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TimedTaskDetailView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TimedTaskDeleteView(LoginRequiredMixin, DetailView):
    model = TimedTask
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'
    template_name = 'xm2cloud_cmp/timedtask_delete.html'

    def get_context_data(self, **kwargs):
        context = super(TimedTaskDeleteView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TimedTaskManageView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/timedtask_manage.html'

    def get_context_data(self, **kwargs):
        context = super(TimedTaskManageView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TimedTaskApiListView(LoginRequiredMixin, JSONListView):
    model = TimedTask

    def get_user_sort(self):
        return self.request.GET.get('sort', 'date_changed')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        timedtaskid, crontabid, intervalid, timedtasksearch = map(
            lambda field: self.request.GET.get(field, None),
            ['timedtaskId', 'crontabId', 'intervalId', 'timedtaskSearch']
        )
        order_by_field = self.get_ordering()
        queryset = super(TimedTaskApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])

        if timedtaskid is not None:
            queryset = queryset.filter(pk=timedtaskid)
            return queryset.order_by(order_by_field)

        if crontabid is not None:
            queryset = queryset.filter(crontab__pk=crontabid)

        if intervalid is not None:
            queryset = queryset.filter(interval__pk=intervalid)

        if timedtasksearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=timedtasksearch),
                Q(notes__contains=timedtasksearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(TimedTaskApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'enabled': obj.enabled,
                'cluster_id': obj.cluster.pk,
                'sevent_uuid': obj.sevent_uuid,
                'cluster_name': obj.cluster.name,
                'total_run_count': obj.total_run_count,
                'host_id': obj.host and obj.host.pk or None,
                'host_name': obj.host and obj.host.name or None,
                'script_id': obj.script and obj.script.pk or None,
                'crontab_id': obj.crontab and obj.crontab.pk or None,
                'script_name': obj.script and obj.script.name or None,
                'interval_id': obj.interval and obj.interval.pk or None,
                'crontab_hour': obj.crontab and obj.crontab.hour or None,
                'hostgroup_id': obj.hostgroup and obj.hostgroup.pk or None,
                'crontab_minute': obj.crontab and obj.crontab.minute or None,
                'interval_every': obj.interval and obj.interval.every or None,
                'hostgroup_name': obj.hostgroup and obj.hostgroup.name or None,
                'interval_period': obj.interval and obj.interval.period or None,
                'crontab_day_of_week': obj.crontab and obj.crontab.day_of_week or None,
                'crontab_day_of_month': obj.crontab and obj.crontab.day_of_month or None,
                'crontab_month_of_year': obj.crontab and obj.crontab.month_of_year or None,
                'last_run_at': obj.last_run_at and obj.last_run_at.strftime('%Y-%m-%d %H:%M:%S') or None,
                'date_changed': obj.date_changed and obj.date_changed.strftime('%Y-%m-%d %H:%M:%S') or None
            })

        return results


class TimedTaskApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = TimedTask
    fields = ['name', 'interval', 'crontab', 'enabled', 'host', 'script', 'hostgroup', 'cluster', 'notes']

    def get_uuid_pk(self, obj):
        return str(obj and obj.pk or '')

    def get_task_kwargs(self):
        data = {
            'owner': str(self.object.owner.pk),
            'timedtask': str(self.object.sevent_uuid),
            'host': self.get_uuid_pk(self.object.host),
            'script': self.get_uuid_pk(self.object.script),
            'cluster': self.get_uuid_pk(self.object.cluster),
            'hostgroup': self.get_uuid_pk(self.object.hostgroup)
        }

        return json.dumps(data)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.kwargs = self.get_task_kwargs()
        self.object.task = 'executor.timedtask'
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class TimedTaskApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = TimedTask
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'
    fields = ['name', 'interval', 'crontab', 'enabled', 'host', 'script', 'hostgroup', 'cluster', 'notes']

    def get_uuid_pk(self, obj):
        return str(obj and obj.pk or '')

    def get_task_kwargs(self):
        data = {
            'owner': str(self.object.owner.pk),
            'timedtask': str(self.object.sevent_uuid),
            'host': self.get_uuid_pk(self.object.host),
            'script': self.get_uuid_pk(self.object.script),
            'cluster': self.get_uuid_pk(self.object.cluster),
            'hostgroup': self.get_uuid_pk(self.object.hostgroup)
        }

        return json.dumps(data)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.kwargs = self.get_task_kwargs()
        self.object.task = 'executor.timedtask'
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class TimedTaskApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = TimedTask
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'


class RegistedTaskApiListView(LoginRequiredMixin, View):
    def get(self, request):
        from celery.registry import tasks

        results = {'total': len(tasks), 'rows': []}
        map(lambda k: results['rows'].append({'id': k, 'name': tasks[k]}), tasks)

        return JsonResponse(results, status=200)


class CrontabCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/crontab_create.html'

    def get_context_data(self, **kwargs):
        context = super(CrontabCreateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class CrontabUpdateView(LoginRequiredMixin, DetailView):
    model = CrontabSchedule
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/crontab_update.html'

    def get_context_data(self, **kwargs):
        context = super(CrontabUpdateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class CrontabDeleteView(LoginRequiredMixin, DetailView):
    model = CrontabSchedule
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/crontab_delete.html'

    def get_context_data(self, **kwargs):
        context = super(CrontabDeleteView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class CrontabApiListView(LoginRequiredMixin, JSONListView):
    model = CrontabSchedule

    def get_data(self, **context):
        context = super(CrontabApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        objects_list = context['object_list']

        for obj in objects_list:
            hour = obj.hour
            minute = obj.minute
            day_of_week = obj.day_of_week
            day_of_month = obj.day_of_month
            month_of_year = obj.month_of_year
            results['rows'].append({
                'id': obj.pk,
                'hour': hour,
                'minute': minute,
                'day_of_week': day_of_week,
                'day_of_month': day_of_month,
                'month_of_year': month_of_year,
                'name': '{0} {1} {2} {3} {4}'.format(minute, hour, day_of_week, day_of_month, month_of_year)
            })

        return results


class CrontabApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = CrontabSchedule
    fields = ['hour', 'minute', 'day_of_week', 'day_of_month', 'month_of_year']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class CrontabApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = CrontabSchedule
    pk_url_kwarg = 'id'
    fields = ['hour', 'minute', 'day_of_week', 'day_of_month', 'month_of_year']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class CrontabApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = CrontabSchedule
    pk_url_kwarg = 'id'


class IntervalCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/interval_create.html'

    def get_context_data(self, **kwargs):
        context = super(IntervalCreateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class IntervalUpdateView(LoginRequiredMixin, DetailView):
    model = IntervalSchedule
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/interval_update.html'

    def get_context_data(self, **kwargs):
        context = super(IntervalUpdateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class IntervalDeleteView(LoginRequiredMixin, DetailView):
    model = IntervalSchedule
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/interval_delete.html'

    def get_context_data(self, **kwargs):
        context = super(IntervalDeleteView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class IntervalApiListView(LoginRequiredMixin, JSONListView):
    model = IntervalSchedule

    def get_data(self, **context):
        context = super(IntervalApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        objects_list = context['object_list']

        for obj in objects_list:
            every = obj.every
            period = obj.period
            results['rows'].append({
                'id': obj.pk,
                'every': every,
                'period': period,
                'name': '{0} {1}'.format(every, period)
            })

        return results


class IntervalApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = IntervalSchedule
    fields = ['every', 'period']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class IntervalApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = IntervalSchedule
    pk_url_kwarg = 'id'
    fields = ['every', 'period']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class IntervalApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = IntervalSchedule
    pk_url_kwarg = 'id'


class TaskWorkFlowListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/taskworkflows.html'

    def get_context_data(self, **kwargs):
        context = super(TaskWorkFlowListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TaskWorkFlowCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/taskworkflow_create.html'

    def get_context_data(self, **kwargs):
        context = super(TaskWorkFlowCreateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TaskWorkFlowUpdateView(LoginRequiredMixin, DetailView):
    model = TaskWorkFlow
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/taskworkflow_update.html'

    def get_context_data(self, **kwargs):
        context = super(TaskWorkFlowUpdateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TaskWorkFlowDeleteView(LoginRequiredMixin, DetailView):
    model = TaskWorkFlow
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/taskworkflow_delete.html'

    def get_context_data(self, **kwargs):
        context = super(TaskWorkFlowDeleteView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TaskWorkFlowDetailView(LoginRequiredMixin, DetailView):
    model = TaskWorkFlow
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/taskworkflow_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TaskWorkFlowDetailView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class TaskWorkFlowApiListView(LoginRequiredMixin, JSONListView):
    model = TaskWorkFlow

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        taskworkflowid, taskworkflowsearch = map(
            lambda field: self.request.GET.get(field, None),
            ['taskworkflowId', 'taskworkflowSearch']
        )
        queryset = super(TaskWorkFlowApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if taskworkflowid is not None:
            queryset = queryset.filter(pk=taskworkflowid)
            return queryset.order_by(order_by_field)

        if taskworkflowsearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=taskworkflowsearch),
                Q(notes__contains=taskworkflowsearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(TaskWorkFlowApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'workflowtasks': obj.workflowtask_set.count(),
                'update_time': obj.update_time.strftime('%Y-%m-%d %H:%S:%M')
            })

        return results


class TaskWorkFlowManageView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/taskworkflow_manage.html'

    def get_context_data(self, **kwargs):
        context = super(TaskWorkFlowManageView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class DashBoardScreenDefaultView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/dashboardscreen_default.html'

    def get_context_data(self, **kwargs):
        context = super(DashBoardScreenDefaultView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class DashBoardScreenCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/dashboardscreen_create.html'

    def get_context_data(self, **kwargs):
        context = super(DashBoardScreenCreateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class DashBoardScreenUpdateView(LoginRequiredMixin, DetailView):
    model = DashBoardScreen
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/dashboardscreen_update.html'

    def get_context_data(self, **kwargs):
        context = super(DashBoardScreenUpdateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class DashBoardScreenDetailView(LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'id'
    model = DashBoardScreen
    template_name = 'xm2cloud_cmp/dashboardscreen_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DashBoardScreenDetailView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class DashBoardScreenApiListView(LoginRequiredMixin, JSONListView):
    model = DashBoardScreen

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        queryset = super(DashBoardScreenApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by = self.get_ordering()

        return queryset.order_by(order_by)

    def get_data(self, **context):
        context = super(DashBoardScreenApiListView, self).get_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        objects_list = context['object_list']

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes
            })

        return results


class DashBoardScreenApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = DashBoardScreen
    fields = ['name', 'notes']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class DashBoardScreenApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = DashBoardScreen
    pk_url_kwarg = 'id'
    fields = ['name', 'notes']

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class DashBoardScreenApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = DashBoardScreen
    pk_url_kwarg = 'id'


class DashBoardScreenTargetCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/dashboardscreentarget_create.html'

    def get_context_data(self, **kwargs):
        context = super(DashBoardScreenTargetCreateView, self).get_context_data(**kwargs)
        context.update({
        })
        return context


class DashBoardScreenTargetUpdateView(LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'id'
    model = DashBoardScreenTarget
    template_name = 'xm2cloud_cmp/dashboardscreentarget_update.html'

    def get_context_data(self, **kwargs):
        context = super(DashBoardScreenTargetUpdateView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class DashBoardScreenTargetApiListView(LoginRequiredMixin, JSONListView):
    model = DashBoardScreenTarget

    def get_user_sort(self):
        return self.request.GET.get('sort', 'weight')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_queryset(self):
        queryset = super(DashBoardScreenTargetApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        return queryset.order_by(order_by_field)

    def get_data(self, **context):
        context = super(DashBoardScreenTargetApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'weight': obj.weight,
                'metrics': obj.metrics,
                'charttype': obj.charttype,
                'aggregators': obj.aggregators,
                'is_compared': obj.is_compared,
                'screen_id': obj.screen and obj.screen.pk or None
            })

        return results


class DashBoardScreenTargetApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = DashBoardScreenTarget
    fields = ['name', 'notes', 'metrics', 'aggregators', 'is_compared', 'screen']

    def get_hosts(self):
        host_ids = self.request.POST.getlist('hosts', [])

        return Host.objects.filter(pk__in=host_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.hosts = self.get_hosts()
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class DashBoardScreenTargetApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = DashBoardScreenTarget
    pk_url_kwarg = 'id'
    fields = ['name', 'notes', 'metrics', 'aggregators', 'is_compared', 'screen']

    def get_hosts(self):
        host_ids = self.request.POST.getlist('hosts', [])

        return Host.objects.filter(pk__in=host_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.hosts = self.get_hosts()
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class DashBoardScreenTargetApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = DashBoardScreenTarget
    pk_url_kwarg = 'id'

    def get_host(self):
        host_id = self.request.POST.get('host', '')

        return Host.objects.filter(pk=host_id).first()

    def delete(self, request, *args, **kwargs):
        host = self.get_host()
        if not host:
            return super(DashBoardScreenTargetApiDeleteView, self).delete(request, *args, **kwargs)
        self.get_object().hosts.remove(host)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AlarmStrategyManageView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alarmstrategy_manage.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyManageView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class MessageTopicListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/messagetopics.html'

    def get_context_data(self, **kwargs):
        context = super(MessageTopicListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class MessageTopicApiListView(LoginRequiredMixin, JSONListView):
    model = MessageTopic

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        messagetopicid, messagetopicsearch = map(
            lambda field: self.request.GET.get(field, None),
            ['messagetopicId', 'messagetopicSearch']
        )
        queryset = super(MessageTopicApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if messagetopicid is not None:
            queryset = queryset.filter(pk=messagetopicid)
            return queryset.order_by(order_by_field)

        if messagetopicsearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=messagetopicsearch),
                Q(notes__contains=messagetopicsearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(MessageTopicApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'alarmstrategies': obj.alarmstrategy_set.count(),
                'messagesubscribers': obj.messagesubscriber_set.count(),
                'update_time': obj.update_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return results


class AlarmHistoryListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alarmhistories.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmHistoryListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlarmHistoryDetailView(LoginRequiredMixin, DetailView):
    model = AlarmHistory
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(AlarmHistoryDetailView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlarmHistoryApiListView(LoginRequiredMixin, JSONListView):
    model = AlarmHistory

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        alarmhistoryid, alarmhistorysearch = map(
            lambda field: self.request.GET.get(field, None),
            ['alarmhistoryId', 'alarmhistorySearch']
        )
        queryset = super(AlarmHistoryApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if alarmhistoryid is not None:
            queryset = queryset.filter(pk=alarmhistoryid)
            return queryset.order_by(order_by_field)

        if alarmhistorysearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=alarmhistorysearch),
                Q(error__contains=alarmhistorysearch),
                Q(notes__contains=alarmhistorysearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(AlarmHistoryApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'error': obj.error,
                'notes': obj.notes,
                'host_id': obj.host.pk,
                'host_name': obj.host.name,
                'acknowledges': obj.acknowledge_set.count(),
                'alarmstrategy_grade': obj.alarmstrategy.grade,
                'alarmstrategy_id': obj.alarmstrategy.sevent_uuid,
                'update_time': obj.update_time.strftime('%Y-%m-%d %H:%M:%S'),
                'alarmstrategy_topic_id': obj.alarmstrategy.topic and obj.alarmstrategy.topic.pk or None,
                'alarmstrategy_topic_name': obj.alarmstrategy.topic and obj.alarmstrategy.topic.name or None,
            })

        return results


class AlarmStrategyListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alarmstrategies.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlarmStrategyCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alarmstrategy_create.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyCreateView, self).get_context_data(**kwargs)
        context.update({
            'hosts': Host.objects.all()
        })
        return context


class AlarmStrategyUpdateView(LoginRequiredMixin, DetailView):
    model = AlarmStrategy
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'
    template_name = 'xm2cloud_cmp/alarmstrategy_update.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyUpdateView, self).get_context_data(**kwargs)
        context.update({
            'hosts': Host.objects.all(),
            'crontabs': CrontabSchedule.objects.all(),
            'intervals': IntervalSchedule.objects.all(),
            'messagetopics': MessageTopic.objects.all()
        })
        return context


class AlarmStrategyDetailView(LoginRequiredMixin, DetailView):
    model = AlarmStrategy
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'
    template_name = 'xm2cloud_cmp/alarmstrategy_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyDetailView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlarmStrategyDeleteView(LoginRequiredMixin, DetailView):
    model = AlarmStrategy
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'
    template_name = 'xm2cloud_cmp/alarmstrategy_delete.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyDeleteView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlarmStrategyApiListView(LoginRequiredMixin, JSONListView):
    model = AlarmStrategy

    def get_user_sort(self):
        return self.request.GET.get('sort', 'last_run_at')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        alarmstrategyid, alarmstrategygroupid, alarmstrategysearch = map(
            lambda field: self.request.GET.get(field, None),
            ['alarmstrategyId', 'alarmstrategygroupId', 'alarmstrategySearch']
        )
        queryset = super(AlarmStrategyApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if alarmstrategyid is not None:
            queryset = queryset.filter(pk=alarmstrategyid)
            return queryset.order_by(order_by_field)

        if alarmstrategygroupid is not None:
            queryset = queryset.filter(alarmstrategygroup__pk=alarmstrategygroupid).distinct()

        if alarmstrategysearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=alarmstrategysearch),
                Q(rules__contains=alarmstrategysearch),
                Q(notes__contains=alarmstrategysearch),
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(AlarmStrategyApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'grade': obj.grade,
                'rules': obj.rules,
                'enabled': obj.enabled,
                'hosts': obj.hosts.count(),
                'sevent_uuid': obj.sevent_uuid,
                'total_run_count': obj.total_run_count,
                'crontab_id': obj.crontab and obj.crontab.pk or None,
                'interval_id': obj.interval and obj.interval.pk or None,
                'crontab_hour': obj.crontab and obj.crontab.hour or None,
                'crontab_minute': obj.crontab and obj.crontab.minute or None,
                'interval_every': obj.interval and obj.interval.every or None,
                'interval_period': obj.interval and obj.interval.period or None,
                'crontab_day_of_week': obj.crontab and obj.crontab.day_of_week or None,
                'crontab_day_of_month': obj.crontab and obj.crontab.day_of_month or None,
                'crontab_month_of_year': obj.crontab and obj.crontab.month_of_year or None,
                'last_run_at': obj.last_run_at and obj.last_run_at.strftime('%Y-%m-%d %H:%M:%S') or None,
                'date_changed': obj.date_changed and obj.date_changed.strftime('%Y-%m-%d %H:%M:%S') or None
            })

        return results


class AlarmStrategyApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = AlarmStrategy
    fields = ['name', 'interval', 'crontab', 'enabled', 'rules', 'notes', 'grade', 'hosts', 'topic',
              'alarmstrategygroup']

    def get_uuid_pk(self, obj):
        return str(obj and obj.pk or '')

    def get_task_kwargs(self):
        data = {
            'owner': self.get_uuid_pk(self.request.user),
            'alarmstrategy': str(self.object.sevent_uuid)
        }

        return json.dumps(data)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.kwargs = self.get_task_kwargs()
        self.object.task = 'executor.analysetrigger'
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AlarmStrategyApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = AlarmStrategy
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'
    fields = ['name', 'interval', 'crontab', 'enabled', 'rules', 'notes', 'grade', 'hosts', 'topic',
              'alarmstrategygroup']

    def get_uuid_pk(self, obj):
        return str(obj and obj.pk or '')

    def get_task_kwargs(self):
        data = {
            'owner': self.get_uuid_pk(self.request.user),
            'alarmstrategy': str(self.object.sevent_uuid)
        }

        return json.dumps(data)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.kwargs = self.get_task_kwargs()
        self.object.task = 'executor.analysetrigger'
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AlarmStrategyApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = AlarmStrategy
    slug_url_kwarg = 'slug'
    slug_field = 'sevent_uuid'


class AlarmStrategyGroupListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alarmstrategygroups.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyGroupListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlarmStrategyGroupCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alarmstrategygroup_create.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyGroupCreateView, self).get_context_data(**kwargs)
        context.update({
            'alarmstrategies': AlarmStrategy.objects.all()
        })
        return context


class AlarmStrategyGroupUpdateView(LoginRequiredMixin, DetailView):
    model = AlarmStrategyGroup
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/alarmstrategygroup_update.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyGroupUpdateView, self).get_context_data(**kwargs)
        context.update({
            'alarmstrategies': AlarmStrategy.objects.all()
        })
        return context


class AlarmStrategyGroupDetailView(LoginRequiredMixin, DetailView):
    model = AlarmStrategyGroup
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/alarmstrategygroup_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyGroupDetailView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlarmStrategyGroupDeleteView(LoginRequiredMixin, DetailView):
    model = AlarmStrategyGroup
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/alarmstrategygroup_delete.html'

    def get_context_data(self, **kwargs):
        context = super(AlarmStrategyGroupDeleteView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlarmStrategyGroupApiListView(LoginRequiredMixin, JSONListView):
    model = AlarmStrategyGroup

    def get_user_sort(self):
        return self.request.GET.get('sort', 'update_time')

    def get_user_order(self):
        order = self.request.GET.get('order', 'desc')

        return (order == 'desc') and '-' or ''

    def get_ordering(self):
        sort = self.get_user_sort()
        order = self.get_user_order()

        return '{0}{1}'.format(order, sort)

    def get_queryset(self):
        alarmstrategyid, alarmstrategygroupid, alarmstrategygroupsearch = map(
            lambda field: self.request.GET.get(field, None),
            ['alarmstrategyid', 'alarmstrategygroupId', 'alarmstrategygroupSearch']
        )
        queryset = super(AlarmStrategyGroupApiListView, self).get_queryset().filter(owner__in=[
            self.request.user,
            self.request.user.profile.parent
        ])
        order_by_field = self.get_ordering()

        if alarmstrategygroupid is not None:
            queryset = queryset.filter(pk=alarmstrategygroupid)
            return queryset.order_by(order_by_field)

        if alarmstrategyid is not None:
            queryset = queryset.filter(alarmstrategy__sevent_uuid=alarmstrategyid)

        if alarmstrategygroupsearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(name__contains=alarmstrategygroupsearch),
                Q(notes__contains=alarmstrategygroupsearch)
            ])
            queryset = queryset.filter(condition_or_list).distinct()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(AlarmStrategyGroupApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'alarmstrategies': obj.alarmstrategy_set.count(),
                'update_time': obj.update_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return results


class AlarmStrategyGroupApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = AlarmStrategyGroup
    fields = ['name', 'notes']

    def get_alarmstrategy_set(self):
        alarmstrategy_ids = self.request.POST.getlist('alarmstrategy_set', [])

        return AlarmStrategy.objects.filter(sevent_uuid__in=alarmstrategy_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        alarmstrategy_set = self.get_alarmstrategy_set()
        self.object.alarmstrategy_set.add(*alarmstrategy_set)
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AlarmStrategyGroupApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = AlarmStrategyGroup
    pk_url_kwarg = 'id'
    fields = ['name', 'notes']

    def get_alarmstrategy_set(self):
        alarmstrategy_ids = self.request.POST.getlist('alarmstrategy_set', [])

        return AlarmStrategy.objects.filter(sevent_uuid__in=alarmstrategy_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.alarmstrategy_set = self.get_alarmstrategy_set()
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AlarmStrategyGroupApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = AlarmStrategyGroup
    pk_url_kwarg = 'id'
