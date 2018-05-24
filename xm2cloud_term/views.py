# -*- coding: utf-8 -*-


from xm2cloud_cmp.models import Host
from django.views.generic import DetailView
from django.utils.decorators import classonlymethod
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)

        return login_required(view)


class WebTermView(LoginRequiredMixin, DetailView):
    model = Host
    pk_url_kwarg = 'id'
    template_name = 'xm2cloud_term/terminal.html'

    def get_wsserver(self):
        return self.request.get_host()

    def get_ssh_host(self):
        return self.object.iplines.filter(is_preferred=True).first().ip

    def get_context_data(self, **kwargs):
        context = super(WebTermView, self).get_context_data(**kwargs)

        context.update({
            'ssh_host': self.get_ssh_host(),
            'wsserver': self.get_wsserver(),
            'protocol': self.kwargs['protocol']
        })

        return context


