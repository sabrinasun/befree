from django.views.generic import View
from django.shortcuts import render


class IndexView(View):

    template_name = 'network/index.html'

    def get(self, request):

        context = {
            'prompt': 'Post a general message:',
            'keywords': ['a', 'b', 'c', 'd']
        }

        return render(request, self.template_name, context)
