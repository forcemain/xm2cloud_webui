# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


from . import models


class HostAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class RegionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ClusterAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class HostGroupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class EnvirmentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ContinentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class AlertContactAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class OperatingSystemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class AlertContactGroupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'notes']


class IpLineAdmin(admin.ModelAdmin):
    search_fields = ['ip', 'notes']


class GraphiteStatusCheckAdmin(admin.ModelAdmin):
    search_fields = ['name']


class HttpStatusCheckAdmin(admin.ModelAdmin):
    search_fields = ['name']


class PortStatusCheckAdmin(admin.ModelAdmin):
    search_fields = ['name']


class DashBoardScreenAdmin(admin.ModelAdmin):
    search_fields = ['name']


class DashBoardScreenTargetAdmin(admin.ModelAdmin):
    search_fields = ['name']


class SSHIdentificationAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ReportTaskAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ReportingAdmin(admin.ModelAdmin):
    search_fields = ['task_id']


admin.site.register(models.Host, HostAdmin)
admin.site.register(models.IpLine, IpLineAdmin)
admin.site.register(models.Region, RegionAdmin)
admin.site.register(models.Cluster, ClusterAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.HostGroup, HostGroupAdmin)
admin.site.register(models.Envirment, EnvirmentAdmin)
admin.site.register(models.Continent, ContinentAdmin)
admin.site.register(models.Reporting, ReportingAdmin)
admin.site.register(models.ReportTask, ReportTaskAdmin)
admin.site.register(models.AlertContact, AlertContactAdmin)
admin.site.register(models.Manufacturer, ManufacturerAdmin)
admin.site.register(models.HttpStatusCheck, HttpStatusCheckAdmin)
admin.site.register(models.PortStatusCheck, PortStatusCheckAdmin)
admin.site.register(models.OperatingSystem, OperatingSystemAdmin)
admin.site.register(models.DashBoardScreen, DashBoardScreenAdmin)
admin.site.register(models.AlertContactGroup, AlertContactGroupAdmin)
admin.site.register(models.SSHIdentification, SSHIdentificationAdmin)
admin.site.register(models.GraphiteStatusCheck, GraphiteStatusCheckAdmin)
admin.site.register(models.DashBoardScreenTarget, DashBoardScreenTargetAdmin)
