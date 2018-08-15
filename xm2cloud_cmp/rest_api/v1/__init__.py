#! -*- coding: utf-8 -*-


from django.conf.urls import url
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


from . import views


router = routers.DefaultRouter()
router.urls.extend(format_suffix_patterns([
    url(r'scripts/$', views.ScriptListApiView.as_view()),
    url(r'script/(?P<pk>[0-9a-z_\-]+)/$', views.ScriptDetailApiView.as_view())
]))
