from abc import ABCMeta

from django.views.generic import View
from django.shortcuts import render


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
