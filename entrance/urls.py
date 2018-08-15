#! -*- coding: utf-8 -*-


from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view
from xm2cloud_cmp.rest_api.v1 import router as cmp_rest_router


from . import views


rest_api_urls = []
rest_api_urls.extend(cmp_rest_router.urls)

schema_view = get_swagger_view(title=u'XM2CLOUD API-DOCS')

urlpatterns = [
    url(r'^/?', include('xm2cloud_web.urls', namespace='xm2cloud_web')),
    url(r'^cmp/', include('xm2cloud_cmp.urls', namespace='xm2cloud_cmp')),
    url(r'^blog/', include('xm2cloud_blog.urls', namespace='xm2cloud_blog')),
    url(r'^accounts/', include('xm2cloud_auth.urls', namespace='xm2cloud_auth')),
    url(r'^terminal/', include('xm2cloud_term.urls', namespace='xm2cloud_term')),

    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/docs/', schema_view),
    url(r'^api/v1/', include(rest_api_urls)),
    url(r'^api/v1/auth/', include('rest_framework.urls', namespace='rest_framework_auth')),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='xm2cloud_media')
    ]

urlpatterns += [
    url(r'', views.HttpNotFoundView.as_view(), name='http_not_found'),
]
