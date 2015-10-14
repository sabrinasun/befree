from abc import ABCMeta

from network.views.common.common_base_view import CommonBaseView

class PostCategoryView(CommonBaseView):
    __metaclass__ = ABCMeta
    category = ''

    def pre_populate_context(self):
        self.update_context({
            'keywords': []
        })

    def get_keywords(self):
        pass