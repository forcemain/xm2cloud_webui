# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from djcelery.models import TaskMeta
from django.db.models import Q, Count
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import classonlymethod
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, View


from .base import JSONListView, JSONCreateView, JSONDeleteView, JSONUpdateView
from .models import (
    Cluster, Host, Continent, Project, Envirment, HostGroup, AlertContactGroup, GraphiteStatusCheck,
    CheckHostResult, Notification, DashBoardScreen, DashBoardScreenTarget, Region, Manufacturer,
    ReportTask, Reporting
)


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
            'render_url': reverse_lazy('xm2cloud_cmp:api_graphite_metric_render'),
            'finder_url': reverse_lazy('xm2cloud_cmp:api_graphite_metric_finder'),
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
            'projects': Project.objects.all(),
            'envirments': Envirment.objects.all(),
        })

        return context


class ClusterUpdateView(LoginRequiredMixin, DetailView):
    model = Cluster
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/cluster_update.html'

    def get_context_data(self, **kwargs):
        context = super(ClusterUpdateView, self).get_context_data(**kwargs)
        context.update({
            'projects': Project.objects.all(),
            'envirments': Envirment.objects.all(),
        })

        return context


class ClusterApiListView(LoginRequiredMixin, JSONListView):
    model = Cluster

    def get_ordering(self):
        return 'id'

    def get_queryset(self):
        queryset = super(ClusterApiListView, self).get_queryset()
        order_by_field = self.get_ordering()

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
                'alerts': 0,
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'env': obj.env.name,
                'project': obj.project.name,
                'create_time': obj.create_time,
                'hostgroups': obj.hostgroup_set.count(),
                'hosts': Host.objects.filter(hostgroups__in=obj.hostgroup_set.all()).distinct().count()
            })

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results


class ClusterApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = Cluster
    fields = ['name', 'env', 'project', 'notes']


class ClusterApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = Cluster
    pk_url_kwarg = 'id'
    fields = ['name', 'env', 'project', 'notes']


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
            'clusters': Cluster.objects.all(),
            'alertcontactgroups': AlertContactGroup.objects.all(),
        })

        return context


class HostgroupApiListView(LoginRequiredMixin, JSONListView):
    model = HostGroup

    def get_ordering(self):
        return 'id'

    def get_queryset(self):
        clusterid = self.request.GET.get('clusterId', None)
        queryset = super(HostgroupApiListView, self).get_queryset()
        order_by_field = self.get_ordering()

        if clusterid is None:
            return queryset.order_by(order_by_field)
        cluster = get_object_or_404(Cluster, pk=clusterid)
        return queryset.filter(cluster=cluster).order_by(order_by_field)

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
                'alerts': 0,
                'name': obj.name,
                'notes': obj.notes,
                'cluster': {
                    'id': obj.cluster.pk,
                    'name': obj.cluster.name,
                },
                'create_time': obj.create_time,
                'update_time': obj.update_time,
                'hosts': obj.host_set.count(),
                'hosts_annotate': list(obj.host_set.values_list('area__continent__id', 'area__continent__name').annotate(Count('area__id')))
            })

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results


class HostgroupApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = HostGroup
    fields = ['name', 'notes', 'cluster', 'alertcontactgroup']


class HostgroupApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = HostGroup
    pk_url_kwarg = 'id'
    fields = ['name', 'notes', 'cluster', 'alertcontactgroup']


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
    pass


class HostDetailView(LoginRequiredMixin, DetailView):
    model = Host
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/host_detail.html'

    def get_context_data(self, **kwargs):
        metrics = [
            {'suffix': 'band', 'desc': '网络 - 单位: M'},
            {'suffix': 'cpu', 'desc': 'CPU - 单位: %'},
            {'suffix': 'mem', 'desc': '内存 - 单位: %'}
        ]

        for metric in metrics:
            metric.update({'prefix': self.object.remoteip.replace('.', '-')})

        context = super(HostDetailView, self).get_context_data(**kwargs)
        context.update({
            'metrics': metrics,
            'render_url': reverse_lazy('xm2cloud_cmp:api_graphite_metric_render'),
            'terminal_url': reverse_lazy('xm2cloud_term:web_terminal', kwargs={'id': self.object.pk, 'protocol': 'ssh'})
        })

        return context


class HostUpdateView(LoginRequiredMixin, DetailView):
    pass


class HostDeleteView(LoginRequiredMixin, JSONDeleteView):
    pass


class HostApiListView(LoginRequiredMixin, JSONListView):
    model = Host

    def get_ordering(self):
        return 'id'

    def get_queryset(self):
        regionid, clusterid, hostgroupid, continentid, manufacturerid, hostsearch = map(
            lambda field: self.request.GET.get(field, None),
            ['regionId', 'clusterId', 'hostgroupId', 'continentId', 'manufacturerId', 'hostSearch']
        )
        queryset, order_by_field = super(HostApiListView, self).get_queryset(), self.get_ordering()

        if regionid is not None:
            area = get_object_or_404(Region, pk=regionid)
            queryset = queryset.filter(area=area)

        if manufacturerid is not None:
            firm = get_object_or_404(Manufacturer, pk=manufacturerid)
            queryset = queryset.filter(firm=firm)

        if continentid is not None:
            queryset = queryset.filter(area__continent__pk=continentid)

        if hostgroupid is not None:
            hostgroups = HostGroup.objects.filter(pk=hostgroupid)
            queryset = queryset.filter(hostgroups__in=hostgroups).distinct()

        if clusterid is not None:
            cluster = get_object_or_404(Cluster, pk=clusterid)
            queryset = queryset.filter(hostgroups__in=cluster.hostgroup_set.all()).distinct()

        if hostsearch is not None:
            condition_or_list = Q()
            map(lambda q: condition_or_list.add(q, Q.OR), [
                Q(pk__contains=hostsearch),
                Q(name__contains=hostsearch),
                Q(notes__contains=hostsearch),
                Q(iplines__ip__contains=hostsearch),
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
                'vmos': {
                    'name': obj.vmos.name,
                    'type': obj.vmos.type
                },
                'firm': {
                    'name': obj.firm.name,
                },
                'vmcpu': obj.vmcpu,
                'vmmem': obj.vmmem,
                'remoteip': obj.remoteip,
                'is_unusual': obj.is_unusual(),
                'ippool': list(obj.iplines.values('ip', 'band', 'name')),
                'create_time': obj.create_time.strftime('%Y-%m-%d %H:%M'),
            }
            results['rows'].append(ins)

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results


class HostApiSummaryView(LoginRequiredMixin, JSONListView):
    model = Host

    def get_data(self, **context):
        context = super(HostApiSummaryView, self).get_context_data(**context)
        results = {
            'total_nums': 0,
            'is_running': 0,
            'is_outdate': 0,
            'is_overdue': 0,
            'is_unusual': 0
        }
        objects_list = context['object_list']
        for obj in objects_list:
            results['total_nums'] += 1
            if obj.is_running():
                results['is_running'] += 1
            if obj.is_outdate():
                results['is_outdate'] += 1
            if obj.is_overdue():
                results['is_overdue'] += 1
            if obj.is_unusual():
                results['is_unusual'] += 1

        return results


class HostApiCreateView(LoginRequiredMixin, JSONCreateView):
    pass


class HostApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    pass


class HostApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    pass


class MonitorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/monitor_dashboard.html'

    def get_context_data(self, **kwargs):
        metrics = [
            {'suffix': 'band', 'desc': '网络 单位: M'},
            {'suffix': 'cpu', 'desc': 'CPU 单位: %'},
            {'suffix': 'mem', 'desc': '内存 单位: %'}
        ]

        context = super(MonitorDashboardView, self).get_context_data(**kwargs)
        context.update({
            'metrics': metrics,
            'clusters': Cluster.objects.all(),
            'render_url': reverse_lazy('xm2cloud_cmp:api_graphite_metric_render'),
        })

        return context


class AlertCheckListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alert_checks.html'

    def get_context_data(self, **kwargs):
        context = super(AlertCheckListView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AlertHttpCheckListView(LoginRequiredMixin, TemplateView):
    pass


class AlertHttpCheckDetailView(LoginRequiredMixin, DetailView):
    pass


class AlertHttpCheckCreateView(LoginRequiredMixin, TemplateView):
    pass


class AlertHttpCheckUpdateView(LoginRequiredMixin, DetailView):
    pass


class AlertHttpCheckDeleteView(LoginRequiredMixin, JSONDeleteView):
    pass


class AlertPortCheckListView(LoginRequiredMixin, TemplateView):
    pass


class AlertPortCheckDetailView(LoginRequiredMixin, DetailView):
    pass


class AlertPortCheckCreateView(LoginRequiredMixin, TemplateView):
    pass


class AlertPortCheckUpdateView(LoginRequiredMixin, DetailView):
    pass


class AlertPortCheckDeleteView(LoginRequiredMixin, JSONDeleteView):
    pass


class AlertGraphiteCheckListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alert_graphitechecks.html'

    def get_context_data(self, **kwargs):
        context = super(AlertGraphiteCheckListView, self).get_context_data(**kwargs)
        return context


class AlertGraphiteCheckDetailView(LoginRequiredMixin, DetailView):
    pass


class AlertGraphiteCheckCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/graphitecheck_create.html'

    def get_context_data(self, **kwargs):
        context = super(AlertGraphiteCheckCreateView, self).get_context_data(**kwargs)

        return context


class AlertGraphiteCheckUpdateView(LoginRequiredMixin, DetailView):
    pass


class AlertGraphiteCheckDeleteView(LoginRequiredMixin, JSONDeleteView):
    pass


class AlertGraphiteCheckApiListView(LoginRequiredMixin, JSONListView):
    model = GraphiteStatusCheck

    def get_ordering(self):
        return 'name'

    def get_queryset(self):
        queryset = super(AlertGraphiteCheckApiListView, self).get_queryset()
        order_by_field = self.get_ordering()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page-1)*rows, page*rows

    def get_data(self, **context):
        context = super(AlertGraphiteCheckApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'metric': obj.metric,
                'enabled': obj.enabled,
                'successive': obj.successive,
                'calculated_status': obj.calculated_status,
                'interval': obj.interval and {
                    'every': obj.interval.every,
                    'period': obj.interval.period,
                } or None,
                'crontab': obj.crontab and {
                    'minute': obj.crontab.minute,
                    'hour': obj.crontab.hour,
                    'day_of_week': obj.crontab.day_of_week,
                    'day_of_month': obj.crontab.day_of_month,
                    'month_of_year': obj.crontab.month_of_year,
                } or None,
                'warning_value': obj.warning_value,
                'error_value': obj.error_value,
                'critical_value': obj.critical_value,
                'from_value': obj.from_value,
                'from_units': obj.from_units,
                'compare_method': obj.compare_method
            })

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results


class AlertGraphiteCheckApiCreateView(LoginRequiredMixin, JSONCreateView):
    pass


class AlertGraphiteCheckApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    pass


class AlertGraphiteCheckApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    pass


class AlertLogListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alert_logs.html'

    def get_context_data(self, **kwargs):
        context = super(AlertLogListView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AlertRunningLogListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alert_runninglogs.html'

    def get_context_data(self, **kwargs):
        context = super(AlertRunningLogListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlertNotifyingLogListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/alert_notifyinglogs.html'

    def get_context_data(self, **kwargs):
        context = super(AlertNotifyingLogListView, self).get_context_data(**kwargs)
        context.update({

        })
        return context


class AlertNotifyingLogDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_cmp/alert_notifyinglog_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AlertNotifyingLogDetailView, self).get_context_data(**kwargs)
        context.update({
        })

        return context


class AlertRunningLogApiListView(LoginRequiredMixin, JSONListView):
    model = CheckHostResult

    def get_ordering(self):
        return '-end_time'

    def get_queryset(self):
        queryset = super(AlertRunningLogApiListView, self).get_queryset()
        order_by_field = self.get_ordering()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(AlertRunningLogApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'host': {
                    'id': obj.host.id,
                    'name': obj.host.name,
                },
                'sub_metric': obj.sub_metric,
                'messages': obj.messages,
                'sta_status': obj.sta_status,
                'sta_time': obj.sta_time,
                'end_time': obj.end_time,
                'end_status': obj.end_status,
                'alert_status': obj.alert_status,
                'check_result': obj.check_result.id
            })

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=False if order == 'desc' else True)

        return results


class AlertNotifyingLogApiListView(LoginRequiredMixin, JSONListView):
    model = Notification

    def get_ordering(self):
        return '-notifytime'

    def get_queryset(self):
        queryset = super(AlertNotifyingLogApiListView, self).get_queryset()
        order_by_field = self.get_ordering()

        return queryset.order_by(order_by_field)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(AlertNotifyingLogApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            results['rows'].append({
                'id': obj.pk,
                'notice_way': obj.notice_way,
                'alarms_way': obj.alarms_way,
                'is_success': obj.is_success,
                'notifytime': obj.notifytime,
                'retrytimes': obj.retrytimes,
                'targethost': {
                    'id': obj.checkhostresult.host.id,
                    'name': obj.checkhostresult.host.name
                },
                'messages': obj.checkhostresult.messages,
                'sta_time': obj.checkhostresult.sta_time,
                'end_time': obj.checkhostresult.end_time,
                'end_values': obj.checkhostresult.end_values,
                'sub_metric': obj.checkhostresult.sub_metric,
                'sta_status': obj.checkhostresult.sta_status,
                'end_status': obj.checkhostresult.end_status,
                'alert_status': obj.checkhostresult.alert_status,
            })

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=False if order == 'desc' else True)

        return results


class DashboardScreenListApiView(LoginRequiredMixin, JSONListView):
    nodes = []
    model = DashBoardScreen

    def get_children(self, obj, nodes):
        nodes.append({'id': obj.pk, 'text': obj.name, 'children': []})
        for index, child in enumerate(obj.children.all()):
            nodes[0]['children'].append({'id': child.pk, 'text': child.name, 'children': []})
            if not child.children.count():
                continue
            self.get_children(child, nodes)

    def get_ordering(self):
        return 'name'

    def get_q(self):
        return Q(parent__isnull=True)

    def get_queryset(self):
        queryset = super(DashboardScreenListApiView, self).get_queryset()
        q = self.get_q()
        order_by = self.get_ordering()

        return queryset.filter(q).order_by(order_by)

    def get_data(self, **context):
        context = super(DashboardScreenListApiView, self).get_data(**context)
        results = []

        for obj in context['object_list']:
            self.nodes = []
            self.get_children(obj, self.nodes)

            results.extend(self.nodes)

        return results


class DashboardScreenCreateApiView(LoginRequiredMixin, JSONCreateView):
    pass


class DashboardScreenUpdateApiView(LoginRequiredMixin, JSONUpdateView):
    pass


class DashboardScreenDeleteApiView(LoginRequiredMixin, JSONDeleteView):
    pass


class GraphiteMetricRenderApiView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        params.update({'target': request.GET.getlist('target')})

        data = GraphiteCheck.render_metric(params=params)

        return JsonResponse(data, status=200, safe=False)


class GraphiteMetricFinderApiView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        params.update({'query': '{0}*'.format(request.GET.get('q'))})

        data = {}

        return JsonResponse(data, status=200, safe=False)


class ReportTaskListView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_cmp/report_tasks.html'

    def get_context_data(self, **kwargs):
        context = super(ReportTaskListView, self).get_context_data(**kwargs)

        context.update({

        })

        return context


class ReportTaskApiListView(LoginRequiredMixin, JSONListView):
    model = ReportTask

    def get_ordering(self):
        return 'id'

    def get_q(self):
        return Q()

    def get_queryset(self):
        queryset = super(ReportTaskApiListView, self).get_queryset()
        q = self.get_q()
        order_by = self.get_ordering()

        return queryset.filter(q).order_by(order_by)

    def get_paginate_range(self, queryset):
        page = int(self.request.GET.get('page') or 1)
        rows = int(self.request.GET.get('rows') or queryset.count())

        return (page - 1) * rows, page * rows

    def get_data(self, **context):
        context = super(ReportTaskApiListView, self).get_context_data(**context)
        results = {'total': context['object_list'].count(), 'rows': []}
        page, rows = self.get_paginate_range(context['object_list'])
        objects_list = context['object_list'][page: rows]

        for obj in objects_list:
            task_status = 'WAITTING'
            last_run_at = obj.last_run_at
            queryset = TaskMeta.objects.filter(task_id=obj.task_id)
            if queryset.exists():
                task_status = queryset.first().status
                last_run_at = queryset.first().date_done
            results['rows'].append({
                'id': obj.pk,
                'name': obj.name,
                'notes': obj.notes,
                'period': obj.period,
                'enabled': obj.enabled,
                'task_type': obj.task_type,
                'task_status': task_status,
                'last_run_at': last_run_at.strftime('%Y-%m-%d %H:%M:%S'),
                'create_time': obj.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'contactgroups': list(obj.contactgroups.values('id', 'name'))
            })

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results



