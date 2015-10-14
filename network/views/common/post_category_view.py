from abc import ABCMeta

from network.views.common.common_base_view import CommonBaseView
from network.models import Keyword, Category

class PostCategoryView(CommonBaseView):
    __metaclass__ = ABCMeta
    category = ''

    def pre_populate_context(self):
        self.update_context({
            'keywords': Keyword.objects.all(),
            'categories': Category.objects.all()
        })

    def get_keywords(self):
        pass