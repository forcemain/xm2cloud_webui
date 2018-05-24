#! -*- coding: utf-8 -*-


from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'xm2cloud_web/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({

        })

        return context
