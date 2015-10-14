from network.views.common.post_category_view import PostCategoryView


class IndexView(PostCategoryView):

    template_name = 'network/index.html'

    def get(self, request):
        self.pre_populate_context()
        self.update_context({
            'prompt': 'Post a general message:',
        })
        return self.response()
