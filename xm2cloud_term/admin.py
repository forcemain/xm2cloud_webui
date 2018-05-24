# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin


from . import models


class IdentificationAdmin(admin.ModelAdmin):
    search_fields = ['pk']


admin.site.register(models.Identification, IdentificationAdmin)
