# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView


class JSONResponseMixin(object):
    def get_data(self, **context):
        return context

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(**context),
            safe=False,
            **response_kwargs
        )


class JSONListView(JSONResponseMixin, ListView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class JSONDetailView(JSONResponseMixin, DetailView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class JSONCreateView(JSONResponseMixin, CreateView):
    def get_success_url(self):
        return '#'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=403)

    def form_valid(self, form):
        self.object = form.save()
        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class JSONDeleteView(JSONResponseMixin, DeleteView):
    def get_success_url(self):
        return '#'

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)


class JSONUpdateView(JSONResponseMixin, UpdateView):
    def get_success_url(self):
        return '#'

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=403)

    def form_valid(self, form):
        self.object = form.save()
        data = {'next': self.get_success_url()}

        return JsonResponse(data, status=200)

