from network.views.common.common_base_view import CommonBaseView


class IndexView(CommonBaseView):

    template_name = 'network/index.html'

    def get(self, request):

        self.update_context({
            'prompt': 'Post a general message:',
            'keywords': ['a', 'b', 'c', 'd']
        })

        return self.response()
