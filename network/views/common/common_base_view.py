from abc import ABCMeta

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import QueryDict


class CommonBaseView(View):
    __metaclass__ = ABCMeta

    template_name = ''
    context = None

    def update_context(self, data):
        if not self.context:
            self.context = dict()

        if isinstance(data, dict):
            self.context.update(data)

    def response(self):
        return render(self.request, self.template_name, self.context)

    def redirect_to(self, url, **query_params):
        query_dict = QueryDict('', mutable=True)
        query_dict.update(**query_params)
        return HttpResponseRedirect(url + '?' + query_dict.urlencode())
