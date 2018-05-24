# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db.models import Q, Count
from django.http.response import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import classonlymethod
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, View


from .base import JSONListView, JSONCreateView, JSONDeleteView, JSONUpdateView
from .models import (Cluster, Host, IpLine, IpLinePackage, Continent, HostGroup, AlertContactGroup, DashBoardScreen,
                     Manufacturer, Region, OemInfo, OperatingSystem)


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

    def get_ordering(self):
        return '-create_time'

    def get_queryset(self):
        clusterid, clustersearch = map(
            lambda field: self.request.GET.get(field, None),
            ['clusterId', 'clusterSearch']
        )
        queryset, order_by_field = super(ClusterApiListView, self).get_queryset(), self.get_ordering()

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

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results


class ClusterApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = Cluster
    fields = ['name', 'notes']

    def get_hostgroup_set(self):
        hostgroup_ids = self.request.POST.getlist('hostgroup_set', [])

        return HostGroup.objects.filter(pk__in=hostgroup_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.hostgroup_set = self.get_hostgroup_set()
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
        self.object.hostgroup_set = self.get_hostgroup_set()
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

    def get_ordering(self):
        return 'id'

    def get_queryset(self):
        clusterid, hostgroupid, hostid, hostgroupsearch = map(
            lambda field: self.request.GET.get(field, None),
            ['clusterId', 'hostgroupId', 'hostId', 'hostgroupSearch']
        )
        queryset, order_by_field = super(HostgroupApiListView, self).get_queryset(), self.get_ordering()

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

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results


class HostgroupApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = HostGroup
    fields = ['name', 'notes', 'cluster', 'alertcontactgroup']

    def get_host_set(self):
        host_ids = self.request.POST.getlist('host_set', [])

        return Host.objects.filter(pk__in=host_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.host_set = self.get_host_set()
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class HostgroupApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = HostGroup
    pk_url_kwarg = 'id'
    fields = ['name', 'notes', 'cluster', 'alertcontactgroup']

    def get_host_set(self):
        host_ids = self.request.POST.getlist('host_set', [])

        return Host.objects.filter(pk__in=host_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.host_set = self.get_host_set()
        self.object.save()

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

    def get_ordering(self):
        return 'id'

    def get_queryset(self):
        hostid, iplineid, regionid, hostgroupid, continentid, manufacturerid, hostsearch = map(
            lambda field: self.request.GET.get(field, None),
            ['hostId', 'iplineId', 'regionId', 'hostgroupId', 'continentId', 'manufacturerId', 'hostSearch']
        )
        queryset, order_by_field = super(HostApiListView, self).get_queryset(), self.get_ordering()

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
            hostgroups = HostGroup.objects.filter(pk=hostgroupid)
            queryset = queryset.filter(hostgroups__in=hostgroups).distinct()

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
                'checkstate': obj.checkstate(),
                'agentstate': obj.agentstate(),
                'binds': obj.ipline_set.count(),
                'hostgroups': obj.hostgroups.count(),
                'expiry_time': obj.expiry_time.strftime('%Y-%m-%d %H:%M'),
            }
            results['rows'].append(ins)

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results


class HostApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = Host
    fields = ['name', 'vmcpu', 'vmmem', 'notes', 'expiry_time', 'area', 'firm', 'oems', 'vmos', 'hostgroups']

    def get_ipline_set(self):
        ipline_ids = self.request.POST.getlist('ipline_set', [])

        return IpLine.objects.filter(pk__in=ipline_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.ipline_set = self.get_ipline_set()
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class HostApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = Host
    pk_url_kwarg = 'id'
    fields = ['name', 'vmcpu', 'vmmem', 'notes', 'expiry_time', 'area', 'firm', 'oems', 'vmos', 'hostgroups']

    def get_ipline_set(self):
        ipline_ids = self.request.POST.getlist('ipline_set', [])

        return IpLine.objects.filter(pk__in=ipline_ids)

    def form_valid(self, form):
        self.object = form.save()
        self.object.ipline_set = self.get_ipline_set()
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class HostApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Host
    pk_url_kwarg = 'id'


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

    def get_ordering(self):
        return '-create_time'

    def get_queryset(self):
        iplineid, hostid, iplinepackageid, iplinesearch = map(
            lambda field: self.request.GET.get(field, None),
            ['iplineId', 'hostId', 'iplinepackageId', 'iplineSearch']
        )
        queryset, order_by_field = super(IpLineApiListView, self).get_queryset(), self.get_ordering()

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

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results


class IpLineApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = IpLine
    fields = ['band', 'is_preferred', 'ip', 'notes', 'line', 'host', 'package']

    def form_valid(self, form):
        form.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class IpLineApiUpdateView(LoginRequiredMixin, JSONUpdateView):
    model = IpLine
    pk_url_kwarg = 'id'
    fields = ['band', 'is_preferred', 'ip', 'notes', 'line', 'host', 'package']

    def form_valid(self, form):
        form.save()

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

    def get_ordering(self):
        return '-create_time'

    def get_queryset(self):
        iplinepackageid, iplineid, iplinepackagesearch = map(
            lambda field: self.request.GET.get(field, None),
            ['iplinePackageId', 'iplineId', 'iplinePackageSearch']
        )
        queryset, order_by_field = super(IpLinePackageApiListView, self).get_queryset(), self.get_ordering()

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

        sort, order = map(self.request.GET.get, ['sort', 'order'])
        results['rows'].sort(key=lambda r: r[sort or 'id'], reverse=True if order == 'desc' else False)

        return results


class IpLinePackageApiCreateView(LoginRequiredMixin, JSONCreateView):
    model = IpLinePackage
    fields = ['band', 'name', 'line', 'notes']

    def get_ipline_set(self):
        ipline_ids = self.request.POST.getlist('ipline_set', [])

        return IpLine.objects.filter(pk__in=ipline_ids)

    def form_valid(self, form):
        self.object = form.save()
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
        self.object.ipline_set = self.get_ipline_set()
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class IpLinePackageApiDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = IpLinePackage
    pk_url_kwarg = 'id'


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


