# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.http import JsonResponse
from django.utils.decorators import classonlymethod
from django.contrib.auth.decorators import login_required


class JSONResponseMixin(object):
    def get_data(self, **context):
        return context

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(**context),
            **response_kwargs
        )


class LoginRequiredMixin(object):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
