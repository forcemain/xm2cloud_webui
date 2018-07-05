# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from . import models


class IpLineAdmin(admin.ModelAdmin):
    search_fields = ['ip', 'notes']


class ScriptAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class OemInfoAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class HostAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class RegionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ClusterAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class HostGroupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ContinentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ScriptLogAdmin(admin.ModelAdmin):
    pass


class TimedTaskAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class TaskWorkFlowAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class WorkFlowTaskAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ScriptGroupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class AlertContactAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class IpLinePackageAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ClusterContextAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class DashBoardScreenAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class HostGroupContextAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class OperatingSystemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class AlertContactGroupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class DashBoardScreenTargetAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


admin.site.register(models.Host, HostAdmin)
admin.site.register(models.Script, ScriptAdmin)
admin.site.register(models.IpLine, IpLineAdmin)
admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.Cluster, ClusterAdmin)
admin.site.register(models.OemInfo, OemInfoAdmin)
admin.site.register(models.ScriptLog, ScriptLogAdmin)
admin.site.register(models.HostGroup, HostGroupAdmin)
admin.site.register(models.Continent, ContinentAdmin)
admin.site.register(models.TimedTask, TimedTaskAdmin)
admin.site.register(models.ScriptGroup, ScriptGroupAdmin)
admin.site.register(models.AlertContact, AlertContactAdmin)
admin.site.register(models.Manufacturer, ManufacturerAdmin)
admin.site.register(models.TaskWorkFlow, TaskWorkFlowAdmin)
admin.site.register(models.WorkFlowTask, WorkFlowTaskAdmin)
admin.site.register(models.IpLinePackage, IpLinePackageAdmin)
admin.site.register(models.ClusterContext, ClusterContextAdmin)
admin.site.register(models.OperatingSystem, OperatingSystemAdmin)
admin.site.register(models.DashBoardScreen, DashBoardScreenAdmin)
admin.site.register(models.HostGroupContext, HostGroupContextAdmin)
admin.site.register(models.AlertContactGroup, AlertContactGroupAdmin)
admin.site.register(models.DashBoardScreenTarget, DashBoardScreenTargetAdmin)
