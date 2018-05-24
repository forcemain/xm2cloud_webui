# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import pyotp


from io import BytesIO
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse, JsonResponse
from django.views.generic import View, TemplateView, UpdateView, CreateView
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordResetView,
                                       PasswordResetConfirmView)


from .common import email
from .models import Profile
from .common.checkcode import create_checkcode
from .base import JSONResponseMixin, LoginRequiredMixin
from .common.otp import default_otp_generator, default_gotp_generator


class AuthCheckCodeView(View):
    def get(self, request, *args, **kwargs):
        f = BytesIO()
        img, code = create_checkcode()
        request.session['checkcode'] = code
        img.save(f, 'PNG')

        return HttpResponse(f.getvalue())


class AuthRegisterView(TemplateView):
    template_name = 'xm2cloud_auth/register.html'

    def get_context_data(self, **kwargs):
        context = super(AuthRegisterView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AuthMfaChangeView(LoginRequiredMixin, TemplateView):
    secret_key = None
    otp_generator = default_gotp_generator
    template_name = 'xm2cloud_auth/mfa_change_form.html'

    def get_secret_key(self):
        if self.request.user.profile.mfa_secret_key:
            return self.request.user.profile.mfa_secret_key
        return pyotp.random_base32()

    def get_gotp_qurls(self, secret_key):
        if self.request.user.profile.mfa_gotp_qurls:
            return self.request.user.profile.mfa_gotp_qurls
        user_name = self.request.user.username
        issuer_name = 'xm2coud mfa authenticator'
        return self.otp_generator.make_otp(secret_key, user_name, issuer_name)

    def get_context_data(self, **kwargs):
        secret_key = self.get_secret_key()
        gotp_qurls = self.get_gotp_qurls(secret_key)

        context = super(AuthMfaChangeView, self).get_context_data(**kwargs)
        context.update({'secret_key': secret_key, 'gotp_qurls': gotp_qurls})

        return context


class AuthEmailChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_auth/email_change_form.html'

    def get_context_data(self, **kwargs):
        context = super(AuthEmailChangeView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AuthPhoneChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_auth/phone_change_form.html'

    def get_context_data(self, **kwargs):
        context = super(AuthPhoneChangeView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AuthProtectionChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_auth/protection_change_form.html'

    def get_context_data(self, **kwargs):
        context = super(AuthProtectionChangeView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AuthProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_auth/profile.html'

    def get_context_data(self, **kwargs):
        context = super(AuthProfileView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AuthProfileBaseInfoView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_auth/profile_baseinfo.html'

    def get_context_data(self, **kwargs):
        context = super(AuthProfileBaseInfoView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AuthProfileSecurityView(LoginRequiredMixin, TemplateView):
    template_name = 'xm2cloud_auth/profile_security.html'

    def get_context_data(self, **kwargs):
        context = super(AuthProfileSecurityView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AuthLoginView(LoginView):
    template_name = 'xm2cloud_auth/login.html'

    def get_context_data(self, **kwargs):
        context = super(AuthLoginView, self).get_context_data(**kwargs)
        context.update({

        })

        return context


class AuthLogoutView(LogoutView):
    template_name = 'xm2cloud_auth/logged_out.html'

    def get_next_page(self):
        return super(AuthLogoutView, self).get_next_page() or reverse_lazy('xm2cloud_auth:login')


class AuthPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    title = u'修改密码 - XM2CLOUD - 业界领先的云端运维平台'
    template_name = 'xm2cloud_auth/password_change_form.html'


class AuthPasswordResetView(PasswordResetView):
    title = '密码重置 - XM2CLOUD - 业界领先的云端运维平台'
    template_name = 'xm2cloud_auth/password_reset_form.html'


class AuthPasswordResetConfirmView(PasswordResetConfirmView):
    title = '密码重置 - XM2CLOUD - 业界领先的云端运维平台'
    success_url = reverse_lazy('xm2cloud_auth:login')
    template_name = 'xm2cloud_auth/password_reset_confirm.html'

    def get_success_url(self):
        return self.success_url or reverse_lazy('xm2cloud_auth:login')

    @staticmethod
    def valid_checkcode(request):
        pst_checkcode = request.POST.get('checkcode')
        get_checkcode = request.session.get('checkcode')

        check_ready = False

        if get_checkcode and pst_checkcode:
            if get_checkcode.lower() == pst_checkcode.lower():
                check_ready = True

        return check_ready

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_checkcode(request) is False:
            form_errors.append('Please enter a correct checkcode. Note that both fields may be case-sensitive.')
            return JsonResponse({'checkcode': form_errors}, status=403)

        return super(AuthPasswordResetConfirmView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=403)

    def form_valid(self, form):
        super(AuthPasswordResetConfirmView, self).form_valid(form)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthVerifyMfaCodeApiView(LoginRequiredMixin, JSONResponseMixin, View):
    otp_generator = default_gotp_generator

    def get_success_url(self):
        return '#'

    def get_secret_key(self):
        if self.request.user.profile.mfa_secret_key:
            return self.request.user.profile.mfa_secret_key
        return pyotp.random_base32()

    def valid_checkcode(self, request):
        secret_key = self.get_secret_key()
        checkcode = request.POST.get('checkcode')

        return self.otp_generator.check_otp(secret_key, checkcode)

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_checkcode(request) is False:
            form_errors.append('Please enter a correct checkcode. Note that both fields may be case-sensitive.')
            return JsonResponse({'checkcode': form_errors}, status=403)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthEmailCodeSendApiView(LoginRequiredMixin, JSONResponseMixin, View):
    otp_generator = default_otp_generator
    from_email = settings.DEFAULT_FROM_EMAIL
    subject_template_name = 'xm2cloud_auth/checkcode_verify_subject.txt'
    email_template_name = 'xm2cloud_auth/checkcode_verify_email.html'
    html_email_template_name = 'xm2cloud_auth/checkcode_verify_html.html'

    def get_success_url(self):
        return '#'

    def get_to_email(self, request):
        return request.POST.get('email')

    def post(self, request, *args, **kwargs):
        to_email = self.get_to_email(request)
        context = {'email': to_email, 'checkcode': default_otp_generator.make_otp()}

        email.send(self.subject_template_name, self.email_template_name, context, self.from_email, to_email,
                   html_email_template_name=self.html_email_template_name)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthEmailIdentityApiView(AuthEmailCodeSendApiView):
    subject_template_name = 'xm2cloud_auth/checkcode_identity_subject.txt'
    email_template_name = 'xm2cloud_auth/checkcode_identity_email.html'
    html_email_template_name = 'xm2cloud_auth/checkcode_identity_html.html'
    
    def get_to_email(self, request):
        to_email = super(AuthEmailIdentityApiView, self).get_to_email(request)
        return to_email or request.user.email


class AuthVerifyEmailCodeApiView(LoginRequiredMixin, JSONResponseMixin, View):
    otp_generator = default_otp_generator

    def get_success_url(self):
        return '#'

    def valid_checkcode(self, request):
        checkcode = request.POST.get('checkcode')
        return self.otp_generator.check_otp(checkcode)

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_checkcode(request) is False:
            form_errors.append('Please enter a correct checkcode. Note that both fields may be case-sensitive.')
            return JsonResponse({'checkcode': form_errors}, status=403)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthPhoneCodeSendApiView(LoginRequiredMixin, JSONResponseMixin, View):
    otp_generator = default_otp_generator

    def get_success_url(self):
        return '#'

    def post(self, request, *args, **kwargs):
        data = {'next': self.get_success_url()}

        return HttpResponse(data, status=403)


class AuthPhoneIdentityApiView(AuthPhoneCodeSendApiView):
    pass


class AuthVerifyPhoneCodeApiView(LoginRequiredMixin, JSONResponseMixin, View):
    otp_generator = default_otp_generator

    def get_success_url(self):
        return '#'

    def valid_checkcode(self, request):
        checkcode = request.POST.get('checkcode')
        return self.otp_generator.check_otp(checkcode)

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_checkcode(request) is False:
            form_errors.append('Please enter a correct checkcode. Note that both fields may be case-sensitive.')
            return JsonResponse({'checkcode': form_errors}, status=403)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthRegisterApiView(JSONResponseMixin, CreateView):
    model = User
    pk_url_kwarg = 'id'
    fields = ['username', 'password']

    def get_success_url(self):
        return reverse_lazy('xm2cloud_auth:login')

    @staticmethod
    def valid_checkcode(request):
        pst_checkcode = request.POST.get('checkcode')
        get_checkcode = request.session.get('checkcode')

        check_ready = False

        if get_checkcode and pst_checkcode:
            if get_checkcode.lower() == pst_checkcode.lower():
                check_ready = True

        return check_ready

    @staticmethod
    def valid_password(request):
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

        check_ready = password1 == password2

        return check_ready

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_password(request) is False:
            form_errors.append('Please enter a correct password2. Note that both fields may be case-sensitive.')
            return JsonResponse({'password2': form_errors}, status=403)
        if self.valid_checkcode(request) is False:
            form_errors.append('Please enter a checkcode . Note that both fields may be case-sensitive.')
            return JsonResponse({'checkcode': form_errors}, status=403)

        return super(AuthRegisterApiView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=403)

    def form_valid(self, form):
        raw_password = form.cleaned_data.get('password')
        super(AuthRegisterApiView, self).form_valid(form)
        self.object.set_password(raw_password)
        self.object.save()

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthLoginApiView(JSONResponseMixin, LoginView):
    def get_success_url(self):
        return reverse_lazy('xm2cloud_auth:profile')

    @staticmethod
    def valid_checkcode(request):
        pst_checkcode = request.POST.get('checkcode')
        get_checkcode = request.session.get('checkcode')

        check_ready = False

        if get_checkcode and pst_checkcode:
            if get_checkcode.lower() == pst_checkcode.lower():
                check_ready = True

        return check_ready

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_checkcode(request) is False:
            form_errors.append('Please enter a correct checkcode. Note that both fields may be case-sensitive.')
            return JsonResponse({'checkcode': form_errors}, status=403)

        return super(AuthLoginApiView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=403)

    def form_valid(self, form):
        super(AuthLoginApiView, self).form_valid(form)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthPasswordChangeApiView(LoginRequiredMixin, JSONResponseMixin, PasswordChangeView):
    otp_generator = default_gotp_generator

    def get_success_url(self):
        return '#'

    def get_secret_key(self):
        if self.request.user.profile.mfa_secret_key:
            return self.request.user.profile.mfa_secret_key
        return pyotp.random_base32()

    def valid_checkcode(self, request):
        secret_key = self.get_secret_key()
        checkcode = request.POST.get('checkcode')
        if not checkcode:
            return True
        return self.otp_generator.check_otp(secret_key, checkcode)

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_checkcode(request) is False:
            form_errors.append('Please enter a correct checkcode. Note that both fields may be case-sensitive.')
            return JsonResponse({'checkcode': form_errors}, status=403)

        return super(AuthPasswordChangeApiView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=403)

    def form_valid(self, form):
        super(AuthPasswordChangeApiView, self).form_valid(form)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthPasswordResetApiView(JSONResponseMixin, PasswordResetView):
    subject_template_name = 'xm2cloud_auth/password_reset_subject.txt'
    email_template_name = 'xm2cloud_auth/password_reset_email.html'
    html_email_template_name = 'xm2cloud_auth/password_reset_html.html'

    def get_success_url(self):
        return reverse_lazy('xm2cloud_auth:login')

    @staticmethod
    def valid_email(request):
        email = request.POST.get('email')

        return User.objects.filter(email=email).exists()

    @staticmethod
    def valid_checkcode(request):
        pst_checkcode = request.POST.get('checkcode')
        get_checkcode = request.session.get('checkcode')

        check_ready = False

        if get_checkcode and pst_checkcode:
            if get_checkcode.lower() == pst_checkcode.lower():
                check_ready = True

        return check_ready

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_email(request) is False:
            form_errors.append('Please enter a correct email. Note that both fields may be case-sensitive.')
            return JsonResponse({'email': form_errors}, status=403)
        if self.valid_checkcode(request) is False:
            form_errors.append('Please enter a correct checkcode. Note that both fields may be case-sensitive.')
            return JsonResponse({'checkcode': form_errors}, status=403)

        return super(AuthPasswordResetApiView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=403)

    def form_valid(self, form):
        super(AuthPasswordResetApiView, self).form_valid(form)

        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthProfileUpdateApiView(LoginRequiredMixin, JSONResponseMixin, UpdateView):
    model = Profile
    pk_url_kwarg = 'id'
    fields = ['nationality', 'province', 'city', 'district', 'address', 'phone', 'telephone', 'avatar', 'thumbs',
              'mfa_secret_key', 'mfa_gotp_qurls', 'mfa_protect_is_enable', 'operate_protect_intensity',
              'operate_protect_method']

    def get_success_url(self):
        return '#'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=403)

    def form_valid(self, form):
        super(AuthProfileUpdateApiView, self).form_valid(form)
        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class AuthUserUpdateApiView(LoginRequiredMixin, JSONResponseMixin, UpdateView):
    model = User
    pk_url_kwarg = 'id'
    otp_generator = default_otp_generator
    fields = ['username', 'email', 'first_name', 'last_name']

    def get_success_url(self):
        return self.request.path

    def valid_checkcode(self, request):
        checkcode = request.POST.get('checkcode')
        return self.otp_generator.check_otp(checkcode)

    def post(self, request, *args, **kwargs):
        form_errors = []
        if self.valid_checkcode(request) is False:
            form_errors.append('Please enter a correct checkcode. Note that both fields may be case-sensitive.')
            return JsonResponse({'checkcode': form_errors}, status=403)

        return super(AuthUserUpdateApiView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=403)

    def form_valid(self, form):
        super(AuthUserUpdateApiView, self).form_valid(form)
        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)
