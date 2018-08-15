#! -*- coding: utf-8 -*-


from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^home/$', views.HomeView.as_view(),
        name='home'),

    url(r'^dashboard/$', views.DashboardView.as_view(),
        name='dashboard'),

    url(r'^agent/(?P<id>[0-9a-z_\-]+)/installation/$', views.AgentInstallView.as_view(),
        name='agent_install'),

    url(r'^clusters/$', views.ClusterListView.as_view(),
        name='clusters'),
    url(r'^cluster/create/$', views.ClusterCreateView.as_view(),
        name='cluster_create'),
    url(r'^cluster/update/(?P<id>[0-9a-z_\-]+)/$', views.ClusterUpdateView.as_view(),
        name='cluster_update'),
    url(r'^cluster/delete/(?P<id>[0-9a-z_\-]+)/$', views.ClusterDeleteView.as_view(),
        name='cluster_delete'),
    url(r'^cluster/manage/$', views.ClusterManageView.as_view(),
        name='cluster_manage'),
    url(r'^cluster/(?P<id>[0-9a-z_\-]+)/$', views.ClusterDetailView.as_view(),
        name='cluster_detail'),

    url(r'^hostgroups/$', views.HostgroupListView.as_view(),
        name='hostgroups'),
    url(r'^hostgroup/create/$', views.HostgroupCreateView.as_view(),
        name='hostgroup_create'),
    url(r'^hostgroup/update/(?P<id>[0-9a-z_\-]+)/$', views.HostgroupUpdateView.as_view(),
        name='hostgroup_update'),
    url(r'^hostgroup/delete/(?P<id>[0-9a-z_\-]+)/$', views.HostgroupDeleteView.as_view(),
        name='hostgroup_delete'),
    url(r'^hostgroup/manage/$', views.HostgroupManageView.as_view(),
        name='hostgroup_manage'),
    url(r'^hostgroup/(?P<id>[0-9a-z_\-]+)/$', views.HostgroupDetailView.as_view(),
        name='hostgroup_detail'),

    url(r'^hosts/$', views.HostListView.as_view(),
        name='hosts'),
    url(r'^host/create/$', views.HostCreateView.as_view(),
        name='host_create'),
    url(r'^host/update/(?P<id>[0-9a-z_\-]+)/$', views.HostUpdateView.as_view(),
        name='host_update'),
    url(r'^host/delete/(?P<id>[0-9a-z_\-]+)/$', views.HostDeleteView.as_view(),
        name='host_delete'),
    url(r'^host/manage/$', views.HostManageView.as_view(),
        name='host_manage'),
    url(r'^host/(?P<id>[0-9a-z_\-]+)/$', views.HostDetailView.as_view(),
        name='host_detail'),

    url(r'^iplines/$', views.IpLineListView.as_view(),
        name='iplines'),
    url(r'^ipline/create/$', views.IpLineCreateView.as_view(),
        name='ipline_create'),
    url(r'^ipline/update/(?P<id>[0-9a-z_\-]+)/$', views.IpLineUpdateView.as_view(),
        name='ipline_update'),
    url(r'^ipline/delete/(?P<id>[0-9a-z_\-]+)/$', views.IpLineDeleteView.as_view(),
        name='ipline_delete'),
    url(r'^ipline/(?P<id>[0-9a-z_\-]+)/$', views.IpLineDetailView.as_view(),
        name='ipline_detail'),

    url(r'^iplinepackages/$', views.IpLinePackageListView.as_view(),
        name='iplinepackages'),
    url(r'^iplinepackage/create/$', views.IpLinePackageCreateView.as_view(),
        name='iplinepackage_create'),
    url(r'^iplinepackage/update/(?P<id>[0-9a-z_\-]+)/$', views.IpLinePackageUpdateView.as_view(),
        name='iplinepackage_update'),
    url(r'^iplinepackage/delete/(?P<id>[0-9a-z_\-]+)/$', views.IpLinePackageDeleteView.as_view(),
        name='iplinepackage_delete'),
    url(r'^iplinepackage/(?P<id>[0-9a-z_\-]+)/$', views.IpLinePackageDetailView.as_view(),
        name='iplinepackage_detail'),

    url(r'^scripts/$', views.ScriptListView.as_view(),
        name='scripts'),
    url(r'^script/logs/$', views.ScriptLogListView.as_view(),
        name='script_logs'),
    url(r'^script/log/manage/$', views.ScriptLogManageView.as_view(),
        name='script_log_manage'),
    url(r'^script/create/$', views.ScriptCreateView.as_view(),
        name='script_create'),
    url(r'^script/manage/$', views.ScriptManageView.as_view(),
        name='script_manage'),
    url(r'^script/execute/$', views.ScriptExecuteView.as_view(),
        name='script_execute'),
    url(r'^script/update/(?P<id>[0-9a-z_\-]+)/$', views.ScriptUpdateView.as_view(),
        name='script_update'),
    url(r'^script/delete/(?P<id>[0-9a-z_\-]+)/$', views.ScriptDeleteView.as_view(),
        name='script_delete'),
    url(r'^script/(?P<id>[0-9a-z_\-]+)/$', views.ScriptDetailView.as_view(),
        name='script_detail'),

    url(r'^timedtasks/', views.TimedTaskListView.as_view(),
        name='timedtasks'),
    url(r'^timedtask/create/$', views.TimedTaskCreateView.as_view(),
        name='timedtask_create'),
    url(r'^timedtask/manage/$', views.TimedTaskManageView.as_view(),
        name='timedtask_manage'),
    url(r'^timedtask/update/(?P<slug>[0-9a-z_\-]+)/$', views.TimedTaskUpdateView.as_view(),
        name='timedtask_update'),
    url(r'^timedtask/delete/(?P<slug>[0-9a-z_\-]+)/$', views.TimedTaskDeleteView.as_view(),
        name='timedtask_delete'),
    url(r'^timedtask/(?P<slug>[0-9a-z_\-]+)/$', views.TimedTaskDetailView.as_view(),
        name='timedtask_detail'),

    url(r'^crontab/create/$', views.CrontabCreateView.as_view(),
        name='crontab_create'),
    url(r'^crontab/update/(?P<id>[0-9]+)/$', views.CrontabUpdateView.as_view(),
        name='crontab_update'),
    url(r'^crontab/delete/(?P<id>[0-9]+)/$', views.CrontabDeleteView.as_view(),
        name='crontab_delete'),

    url(r'^interval/create/$', views.IntervalCreateView.as_view(),
        name='interval_create'),
    url(r'^interval/update/(?P<id>[0-9]+)/$', views.IntervalUpdateView.as_view(),
        name='interval_update'),
    url(r'^interval/delete/(?P<id>[0-9]+)/$', views.IntervalDeleteView.as_view(),
        name='interval_delete'),

    url(r'^taskworkflows/', views.TaskWorkFlowListView.as_view(),
        name='taskworkflows'),
    url(r'^taskworkflow/create/$', views.TaskWorkFlowCreateView.as_view(),
        name='taskworkflow_create'),
    url(r'^taskworkflow/manage/$', views.TaskWorkFlowManageView.as_view(),
        name='taskworkflow_manage'),
    url(r'^taskworkflow/update/(?P<id>[0-9a-z_\-]+)/$', views.TaskWorkFlowUpdateView.as_view(),
        name='taskworkflow_update'),
    url(r'^taskworkflow/delete/(?P<id>[0-9a-z_\-]+)/$', views.TaskWorkFlowDeleteView.as_view(),
        name='taskworkflow_delete'),
    url(r'^taskworkflow/(?P<id>[0-9a-z_\-]+)/$', views.TaskWorkFlowDetailView.as_view(),
        name='taskworkflow_detail'),

    url(r'^dashboardscreen/default/$', views.DashBoardScreenDefaultView.as_view(),
        name='dashboardscreen_default'),
    url(r'^dashboardscreen/create/$', views.DashBoardScreenCreateView.as_view(),
        name='dashboardscreen_create'),
    url(r'^dashboardscreen/update/(?P<id>[0-9a-z_\-]+)/$', views.DashBoardScreenUpdateView.as_view(),
        name='dashboardscreen_update'),
    url(r'^dashboardscreen/(?P<id>[0-9a-z_\-]+)/$', views.DashBoardScreenDetailView.as_view(),
        name='dashboardscreen_detail'),

    url(r'^dashboardscreentarget/create/$', views.DashBoardScreenTargetCreateView.as_view(),
        name='dashboardscreentarget_create'),
    url(r'^dashboardscreentarget/update/(?P<id>[0-9a-z_\-]+)/$', views.DashBoardScreenTargetUpdateView.as_view(),
        name='dashboardscreentarget_update'),

    url(r'^alarmstrategy/manage/$', views.AlarmStrategyManageView.as_view(),
        name='alarmstrategy_manage'),

    url(r'^messagetopics/$', views.MessageTopicListView.as_view(),
        name='messagetopics'),

    url(r'^alarmhistories/$', views.AlarmHistoryListView.as_view(),
        name='alarmhistories'),
    url(r'^alarmhistory/(?P<id>[0-9a-z_\-]+)/$', views.AlarmHistoryDetailView.as_view(),
        name='alarmhistory_detail'),

    url(r'^alarmstrategies/$', views.AlarmStrategyListView.as_view(),
        name='alarmstrategies'),
    url(r'^alarmstrategy/create/$', views.AlarmStrategyCreateView.as_view(),
        name='alarmstrategy_create'),
    url(r'^alarmstrategy/update/(?P<slug>[0-9a-z_\-]+)/$', views.AlarmStrategyUpdateView.as_view(),
        name='alarmstrategy_update'),
    url(r'^alarmstrategy/delete/(?P<slug>[0-9a-z_\-]+)/$', views.AlarmStrategyDeleteView.as_view(),
        name='alarmstrategy_delete'),
    url(r'^alarmstrategy/(?P<slug>[0-9a-z_\-]+)/$', views.AlarmStrategyDetailView.as_view(),
        name='alarmstrategy_detail'),

    url(r'^alarmstrategygroups/$', views.AlarmStrategyGroupListView.as_view(),
        name='alarmstrategygroups'),
    url(r'^alarmstrategygroup/create/$', views.AlarmStrategyGroupCreateView.as_view(),
        name='alarmstrategygroup_create'),
    url(r'^alarmstrategygroup/update/(?P<id>[0-9a-z_\-]+)/$', views.AlarmStrategyGroupUpdateView.as_view(),
        name='alarmstrategygroup_update'),
    url(r'^alarmstrategygroup/delete/(?P<id>[0-9a-z_\-]+)/$', views.AlarmStrategyGroupDeleteView.as_view(),
        name='alarmstrategygroup_delete'),
    url(r'^alarmstrategygroup/(?P<id>[0-9a-z_\-]+)/$', views.AlarmStrategyGroupDetailView.as_view(),
        name='alarmstrategygroup_detail'),

    url(r'^api/alarmstrategy/$', views.AlarmStrategyApiListView.as_view(),
        name='api_alarmstrategy_list'),
    url(r'^api/alarmstrategy/create/$', views.AlarmStrategyApiCreateView.as_view(),
        name='api_alarmstrategy_create'),
    url(r'^api/alarmstrategy/update/(?P<slug>[0-9a-z_\-]+)/$', views.AlarmStrategyApiUpdateView.as_view(),
        name='api_alarmstrategy_update'),
    url(r'^api/alarmstrategy/delete/(?P<slug>[0-9a-z_\-]+)/$', views.AlarmStrategyApiDeleteView.as_view(),
        name='api_alarmstrategy_delete'),

    url(r'api/messagetopic/$', views.MessageTopicApiListView.as_view(),
        name='api_messagetopic_list'),

    url(r'^api/alarmhistory/$', views.AlarmHistoryApiListView.as_view(),
        name='api_alarmhistory_list'),

    url(r'^api/alarmstrategygroup/$', views.AlarmStrategyGroupApiListView.as_view(),
        name='api_alarmstrategygroup_list'),
    url(r'^api/alarmstrategygroup/create/$', views.AlarmStrategyGroupApiCreateView.as_view(),
        name='api_alarmstrategygroup_create'),
    url(r'^api/alarmstrategygroup/update/(?P<id>[0-9a-z_\-]+)/$', views.AlarmStrategyGroupApiUpdateView.as_view(),
        name='api_alarmstrategygroup_update'),
    url(r'^api/alarmstrategygroup/delete/(?P<id>[0-9a-z_\-]+)/$', views.AlarmStrategyGroupApiDeleteView.as_view(),
        name='api_alarmstrategygroup_delete'),

    url(r'^api/dashboardscreen/$', views.DashBoardScreenApiListView.as_view(),
        name='api_dashboardscreen_list'),
    url(r'^api/dashboardscreen/create/$', views.DashBoardScreenApiCreateView.as_view(),
        name='api_dashboardscreen_create'),
    url(r'^api/dashboardscreen/update/(?P<id>[0-9a-z_\-]+)/$', views.DashBoardScreenApiUpdateView.as_view(),
        name='api_dashboardscreen_update'),
    url(r'^api/dashboardscreen/delete/(?P<id>[0-9a-z_\-]+)/$', views.DashBoardScreenApiDeleteView.as_view(),
        name='api_dashboardscreen_delete'),

    url(r'^api/dashboardscreentarget/$', views.DashBoardScreenTargetApiListView.as_view(),
        name='api_dashboardscreentarget_list'),
    url(r'^api/dashboardscreentarget/create/$', views.DashBoardScreenTargetApiCreateView.as_view(),
        name='api_dashboardscreentarget_create'),
    url(r'^api/dashboardscreentarget/update/(?P<id>[0-9a-z_\-]+)/$', views.DashBoardScreenTargetApiUpdateView.as_view(),
        name='api_dashboardscreentarget_update'),
    url(r'^api/dashboardscreentarget/delete/(?P<id>[0-9a-z_\-]+)/$', views.DashBoardScreenTargetApiDeleteView.as_view(),
        name='api_dashboardscreentarget_delete'),

    url(r'^api/cluster/$', views.ClusterApiListView.as_view(),
        name='api_cluster_list'),
    url(r'^api/cluster/create/$', views.ClusterApiCreateView.as_view(),
        name='api_cluster_create'),
    url(r'^api/cluster/update/(?P<id>[0-9a-z_\-]+)/$', views.ClusterApiUpdateView.as_view(),
        name='api_cluster_update'),
    url(r'^api/cluster/delete/(?P<id>[0-9a-z_\-]+)/$', views.ClusterApiDeleteView.as_view(),
        name='api_cluster_delete'),

    url(r'^api/hostgroup/$', views.HostgroupApiListView.as_view(),
        name='api_hostgroup_list'),
    url(r'^api/hostgroup/create/$', views.HostgroupApiCreateView.as_view(),
        name='api_hostgroup_create'),
    url(r'^api/hostgroup/update/(?P<id>[0-9a-z_\-]+)/$', views.HostgroupApiUpdateView.as_view(),
        name='api_hostgroup_update'),
    url(r'^api/hostgroup/delete/(?P<id>[0-9a-z_\-]+)/$', views.HostgroupApiDeleteView.as_view(),
        name='api_hostgroup_delete'),

    url(r'^api/host/$', views.HostApiListView.as_view(),
        name='api_host_list'),
    url(r'^api/host/create/$', views.HostApiCreateView.as_view(),
        name='api_host_create'),
    url(r'^api/host/update/(?P<id>[0-9a-z_\-]+)/$', views.HostApiUpdateView.as_view(),
        name='api_host_update'),
    url(r'^api/host/delete/(?P<id>[0-9a-z_\-]+)/$', views.HostApiDeleteView.as_view(),
        name='api_host_delete'),

    url(r'^api/ipline/$', views.IpLineApiListView.as_view(),
        name='api_ipline_list'),
    url(r'^api/ipline/create/$', views.IpLineApiCreateView.as_view(),
        name='api_ipline_create'),
    url(r'^api/ipline/update/(?P<id>[0-9a-z_\-]+)/$', views.IpLineApiUpdateView.as_view(),
        name='api_ipline_update'),
    url(r'^api/ipline/delete/(?P<id>[0-9a-z_\-]+)/$', views.IpLineApiDeleteView.as_view(),
        name='api_ipline_delete'),

    url(r'^api/iplinepackage/$', views.IpLinePackageApiListView.as_view(),
        name='api_iplinepackage_list'),
    url(r'^api/iplinepackage/create/$', views.IpLinePackageApiCreateView.as_view(),
        name='api_iplinepackage_create'),
    url(r'^api/iplinepackage/update/(?P<id>[0-9a-z_\-]+)/$', views.IpLinePackageApiUpdateView.as_view(),
        name='api_iplinepackage_update'),
    url(r'^api/iplinepackage/delete/(?P<id>[0-9a-z_\-]+)/$', views.IpLinePackageApiDeleteView.as_view(),
        name='api_iplinepackage_delete'),

    url(r'^api/scripts/$', views.ScriptApiListView.as_view(),
        name='api_script_list'),
    url(r'^api/script/create/$', views.ScriptApiCreateView.as_view(),
        name='api_script_create'),
    url(r'^api/script/update/(?P<id>[0-9a-z_\-]+)/$', views.ScriptApiUpdateView.as_view(),
        name='api_script_update'),
    url(r'^api/script/delete/(?P<id>[0-9a-z_\-]+)/$', views.ScriptApiDeleteView.as_view(),
        name='api_script_delete'),

    url(r'^api/script/logs/$', views.ScriptLogApiListView.as_view(),
        name='api_script_log_list'),
    url(r'^api/script/log/create/$', views.ScriptLogApiCreateView.as_view(),
        name='api_script_log_create'),
    url(r'^api/script/log/result/$', views.ScriptLogApiResultView.as_view(),
        name='api_script_log_result'),
    url(r'^api/script/log/delete/(?P<id>[0-9a-z_\-]+)/$', views.ScriptLogApiDeleteView.as_view(),
        name='api_script_log_delete'),

    url(r'^api/timedtasks/$', views.TimedTaskApiListView.as_view(),
        name='api_timedtask_list'),
    url(r'^api/timedtask/create/$', views.TimedTaskApiCreateView.as_view(),
        name='api_timedtask_create'),
    url(r'^api/timedtask/update/(?P<slug>[0-9a-z_\-]+)/$', views.TimedTaskApiUpdateView.as_view(),
        name='api_timedtask_update'),
    url(r'^api/timedtask/delete/(?P<slug>[0-9a-z_\-]+)/$', views.TimedTaskApiDeleteView.as_view(),
        name='api_timedtask_delete'),

    url(r'^api/crontabs/$', views.CrontabApiListView.as_view(),
        name='api_crontab_list'),
    url(r'^api/crontab/create/$', views.CrontabApiCreateView.as_view(),
        name='api_crontab_create'),
    url(r'^api/crontab/update/(?P<id>[0-9]+)/$', views.CrontabApiUpdateView.as_view(),
        name='api_crontab_update'),
    url(r'^api/crontab/delete/(?P<id>[0-9]+)/$', views.CrontabApiDeleteView.as_view(),
        name='api_crontab_delete'),

    url(r'^api/intervals/$', views.IntervalApiListView.as_view(),
        name='api_interval_list'),
    url(r'^api/interval/create/$', views.IntervalApiCreateView.as_view(),
        name='api_interval_create'),
    url(r'^api/interval/update/(?P<id>[0-9]+)/$', views.IntervalApiUpdateView.as_view(),
        name='api_interval_update'),
    url(r'^api/interval/delete/(?P<id>[0-9]+)/$', views.IntervalApiDeleteView.as_view(),
        name='api_interval_delete'),

    url(r'^api/taskworkflows/', views.TaskWorkFlowApiListView.as_view(),
        name='api_taskworkflow_list'),

    url(r'^api/monitor/metrics/query/$', views.MonitorMetricsApiQueryView.as_view(),
        name='api_monitor_metrics_query'),
    url(r'^api/monitor/metrics/suggest/$', views.MonitorMetricsApiSuggestView.as_view(),
        name='api_monitor_metrics_suggest'),
]
