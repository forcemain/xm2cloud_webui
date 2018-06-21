#! -*- coding: utf-8 -*-


from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^home/$', views.HomeView.as_view(),
        name='home'),

    url(r'^clusters/$', views.ClusterListView.as_view(),
        name='clusters'),
    url(r'^cluster/create/$', views.ClusterCreateView.as_view(),
        name='cluster_create'),
    url(r'^cluster/update/(?P<id>[0-9]+)/$', views.ClusterUpdateView.as_view(),
        name='cluster_update'),

    url(r'^hostgroups/$', views.HostgroupListView.as_view(),
        name='hostgroups'),
    url(r'^hostgroup/create/$', views.HostgroupCreateView.as_view(),
        name='hostgroup_create'),
    url(r'^hostgroup/update/(?P<id>[0-9]+)/$', views.HostgroupUpdateView.as_view(),
        name='hostgroup_update'),

    url(r'^hosts/$', views.HostListView.as_view(),
        name='hosts'),
    url(r'^host/(?P<id>[0-9]+)/$', views.HostDetailView.as_view(),
        name='host_detail'),
    url(r'^host/create/$', views.HostCreateView.as_view(),
        name='host_create'),
    url(r'^host/update/(?P<id>[0-9]+)/$', views.HostUpdateView.as_view(),
        name='host_update'),

    url(r'^dashboard/$', views.DashboardView.as_view(),
        name='dashboard'),

    url(r'^monitors/$', views.MonitorDashboardView.as_view(),
        name='monitors'),

    url(r'^report/tasks/$', views.ReportTaskListView.as_view(),
        name='reporttasks'),

    url(r'^alert/checks/$', views.AlertCheckListView.as_view(),
        name='alertchecks'),

    url(r'^alert/httpchecks/$', views.AlertHttpCheckListView.as_view(),
        name='alerthttpchecks'),
    url(r'^alert/httpchecks/(?P<id>[0-9]+)/$', views.AlertHttpCheckDetailView.as_view(),
        name='alerthttpchecks_detail'),
    url(r'^alert/httpchecks/create/$', views.AlertHttpCheckCreateView.as_view(),
        name='alerthttpchecks_create'),
    url(r'^alert/graphitecheck/update/(?P<id>[0-9]+)/$', views.AlertGraphiteCheckUpdateView.as_view(),
        name='alerthttpchecks_update'),

    url(r'^alert/portchecks/$', views.AlertPortCheckListView.as_view(),
        name='alertportchecks'),
    url(r'^alert/portchecks/(?P<id>[0-9]+)/$', views.AlertPortCheckDetailView.as_view(),
        name='alertportchecks_detail'),
    url(r'^alert/portchecks/create/$', views.AlertPortCheckCreateView.as_view(),
        name='alertportchecks_create'),
    url(r'^alert/graphitecheck/update/(?P<id>[0-9]+)/$', views.AlertPortCheckUpdateView.as_view(),
        name='alertportchecks_update'),

    url(r'^alert/graphitechecks/$', views.AlertGraphiteCheckListView.as_view(),
        name='alertgraphitechecks'),
    url(r'^alert/graphitecheck/(?P<id>[0-9]+)/$', views.AlertGraphiteCheckDetailView.as_view(),
        name='alertgraphitecheck_detail'),
    url(r'^alert/graphitecheck/create/$', views.AlertGraphiteCheckCreateView.as_view(),
        name='alertgraphitecheck_create'),
    url(r'^alert/graphitecheck/update/(?P<id>[0-9]+)/$', views.AlertGraphiteCheckUpdateView.as_view(),
        name='alertgraphitecheck_update'),

    url(r'^alert/logs/$', views.AlertLogListView.as_view(),
        name='alertlogs'),

    url(r'^alert/running/logs/$', views.AlertRunningLogListView.as_view(),
        name='alertrunninglogs'),

    url(r'^alert/notifying/logs/$', views.AlertNotifyingLogListView.as_view(),
        name='alertnotifyinglogs'),
    url(r'^alert/notifying/logs/(?P<id>[0-9]+)/$', views.AlertNotifyingLogDetailView.as_view(),
        name='alertnotifyinglog_detail'),

    url(r'^api/dashboardscreen/$', views.DashboardScreenListApiView.as_view(),
        name='api_dashboardscreen_list'),
    url(r'^api/dashboardscreen/create/$', views.DashboardScreenCreateApiView.as_view(),
        name='api_dashboardscreen_create'),
    url(r'^api/dashboardscreen/update/(?P<id>[0-9]+)/$', views.DashboardScreenUpdateApiView.as_view(),
        name='api_dashboardscreen_update'),
    url(r'^api/dashboardscreen/delete/(?P<id>[0-9]+)/$', views.DashboardScreenDeleteApiView.as_view(),
        name='api_dashboardscreen_delete'),

    url(r'^api/cluster/$', views.ClusterApiListView.as_view(),
        name='api_cluster_list'),
    url(r'^api/cluster/create/$', views.ClusterApiCreateView.as_view(),
        name='api_cluster_create'),
    url(r'^api/cluster/update/(?P<id>[0-9]+)/$', views.ClusterApiUpdateView.as_view(),
        name='api_cluster_update'),
    url(r'^api/cluster/delete/(?P<id>[0-9]+)/$', views.ClusterApiDeleteView.as_view(),
        name='api_cluster_delete'),

    url(r'^api/hostgroup/$', views.HostgroupApiListView.as_view(),
        name='api_hostgroup_list'),
    url(r'^api/hostgroup/create/$', views.HostgroupApiCreateView.as_view(),
        name='api_hostgroup_create'),
    url(r'^api/hostgroup/update/(?P<id>[0-9]+)/$', views.HostgroupApiUpdateView.as_view(),
        name='api_hostgroup_update'),
    url(r'^api/hostgroup/delete/(?P<id>[0-9]+)/$', views.HostgroupApiDeleteView.as_view(),
        name='api_hostgroup_delete'),

    url(r'^api/host/$', views.HostApiListView.as_view(),
        name='api_host_list'),
    url(r'^api/host/summary/$', views.HostApiSummaryView.as_view(),
        name='api_host_summary'),
    url(r'^api/host/create/$', views.HostApiCreateView.as_view(),
        name='api_host_create'),
    url(r'^api/host/update/(?P<id>[0-9]+)/$', views.HostApiUpdateView.as_view(),
        name='api_host_update'),
    url(r'^api/host/delete/(?P<id>[0-9]+)/$', views.HostApiDeleteView.as_view(),
        name='api_host_delete'),

    url(r'^api/alert/graphitechecks/$', views.AlertGraphiteCheckApiListView.as_view(),
        name='api_alertgraphitecheck_list'),
    url(r'^api/alert/graphitechecks/create/$', views.AlertGraphiteCheckApiCreateView.as_view(),
        name='api_alertgraphitecheck_create'),
    url(r'^api/alert/graphitechecks/update/(?P<id>[0-9]+)/$', views.AlertGraphiteCheckApiUpdateView,
        name='api_alertgraphitecheck_update'),
    url(r'^api/alert/graphitechecks/update/(?P<id>[0-9]+)/$', views.AlertGraphiteCheckApiUpdateView,
        name='api_alertgraphitecheck_update'),
    url(r'^api/alert/graphitechecks/delete/(?P<id>[0-9]+)/$', views.AlertGraphiteCheckApiDeleteView,
        name='api_alertgraphitecheck_delete'),

    url(r'^api/alert/running/logs/$', views.AlertRunningLogApiListView.as_view(),
        name='api_alertrunninglog_list'),

    url(r'^api/alert/notifying/logs/$', views.AlertNotifyingLogApiListView.as_view(),
        name='api_alertnotifyinglog_list'),

    url(r'^api/graphite/metric/render/$', views.GraphiteMetricRenderApiView.as_view(),
        name='api_graphite_metric_render'),
    url(r'^api/graphite/metric/finder/$', views.GraphiteMetricFinderApiView.as_view(),
        name='api_graphite_metric_finder'),

    url(r'^api/report/tasks/$', views.ReportTaskApiListView.as_view(),
        name='api_reporttasks_list')
]
