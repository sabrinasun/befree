from network.views.common.common_base_view import CommonBaseView

from network.models import Keyword
from network.models import Category


class IndexView(CommonBaseView):
    template_name = 'network/index.html'
    category = 'general'

    def get(self, request):
        self.pre_populate_context()
        return self.response()

    def post(self, request):
        return self.response()

    def pre_populate_context(self):
        self.category = self.request.GET.get('category', 'general')
        self.update_context({
            'keywords': Keyword.objects.all(),
            'categories': Category.objects.all(),
            'category': self.category,
            'prompt': self.get_prompt_message()
        })

    def get_prompt_message(self):
        available_prompt_messages = {
            'general': 'Post a general message',
            'quote': 'Post a Quote'
            # to be continue ...
        }

        return available_prompt_messages.get(self.category, 'Enter a message')
