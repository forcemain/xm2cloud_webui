#! -*- coding: utf-8 -*-


from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^checkcode/$', views.AuthCheckCodeView.as_view(),
        name='checkcode'),

    url(r'^profile/$', views.AuthProfileView.as_view(),
        name='profile'),
    url(r'^profile/baseinfo/$', views.AuthProfileBaseInfoView.as_view(),
        name='profile_baseinfo'),
    url(r'^profile/security/$', views.AuthProfileSecurityView.as_view(),
        name='profile_security'),
    url(r'^mfa_change/$', views.AuthMfaChangeView.as_view(),
        name='mfa_change'),
    url(r'^phone_change/$', views.AuthPhoneChangeView.as_view(),
        name='phone_change'),
    url(r'^email_change/$', views.AuthEmailChangeView.as_view(),
        name='email_change'),
    url(r'^protection_change/$', views.AuthProtectionChangeView.as_view(),
        name='protection_change'),

    url(r'^register/$', views.AuthRegisterView.as_view(),
        name='register'),
    url(r'^login/$', views.AuthLoginView.as_view(),
        name='login'),
    url(r'^logout/$', views.AuthLogoutView.as_view(),
        name='logout'),
    url(r'^password_change/$', views.AuthPasswordChangeView.as_view(),
        name='password_change'),
    url(r'^password_reset/$', views.AuthPasswordResetView.as_view(),
        name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.AuthPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),

    url(r'^api/profile/update/(?P<id>[0-9a-z_\-]+)/$', views.AuthProfileUpdateApiView.as_view(),
        name='api_profile_update'),
    url(r'^api/user/update/(?P<id>[0-9]+)/$', views.AuthUserUpdateApiView.as_view(),
        name='api_user_update'),
    url(r'^api/password_change/$', views.AuthPasswordChangeApiView.as_view(),
        name='api_password_change'),
    url(r'^api/password_reset/$', views.AuthPasswordResetApiView.as_view(),
        name='api_password_reset'),

    url(r'^api/verify_mfa/$', views.AuthVerifyMfaCodeApiView.as_view(),
        name='api_verify_mfa'),
    url(r'^api/verify_email/$', views.AuthVerifyEmailCodeApiView.as_view(),
        name='api_verify_email'),
    url(r'^api/verify_phone/$', views.AuthVerifyPhoneCodeApiView.as_view(),
        name='api_verify_phone'),
    url(r'^api/email_identify/$', views.AuthEmailIdentityApiView.as_view(),
        name='api_email_identify'),
    url(r'^api/phone_identify/$', views.AuthPhoneIdentityApiView.as_view(),
        name='api_phone_identify'),
    url(r'^api/email_code_send/$', views.AuthEmailCodeSendApiView.as_view(),
        name='api_email_code_send'),
    url(r'^api/phone_code_send/$', views.AuthPhoneCodeSendApiView.as_view(),
        name='api_phone_code_send'),

    url(r'^api/register/$', views.AuthRegisterApiView.as_view(),
        name='api_register'),
    url(r'^api/login/$', views.AuthLoginApiView.as_view(),
        name='api_login')
]
