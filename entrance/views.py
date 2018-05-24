#! -*- coding: utf-8 -*-


from django.views.generic import TemplateView


class HttpNotFoundView(TemplateView):
    template_name = 'entrance/404.html'

    def get_context_data(self, **kwargs):
        context = super(HttpNotFoundView, self).get_context_data(**kwargs)
        context.update({})

        return context
