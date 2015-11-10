from django.core.urlresolvers import reverse
from network.views.common.common_base_view import CommonBaseView
from network.forms.post_form import PostForm
from network.models import Keyword
from network.models import Category
from network.models import Post

DEFAULT_CATEGORY_ID = 1
DEFAULT_CATEGORY_CODE = 'teachings'


class IndexView(CommonBaseView):
    template_name = 'network/index.html'
    category_code = 'teachings'
    form = PostForm

    def get(self, request):
        self.pre_populate_context()
        return self.response()

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            self.pre_populate_context()
            self.update_context({
                'form': form
            })
            return self.response()

        self.crate_new_post(request, form)
        return self.redirect_to(reverse('network-index'))

    def crate_new_post(self, request, form):
        post = form.save()
        post.user = request.user
        keywords = self.process_keywords(request.POST.get('keywords', []))
        post.save()
        post.keyword_set.add(*keywords)

    def pre_populate_context(self):
        self.category_code = self.request.GET.get('category', '') or self.request.POST.get('category', '') or DEFAULT_CATEGORY_CODE
        category_id = DEFAULT_CATEGORY_ID if self.category_code == DEFAULT_CATEGORY_CODE else Category.objects.get(code=self.category_code).pk
        self.update_context({
            'keywords': Keyword.objects.all(),
            'categories': Category.objects.all(),
            'category_code': self.category_code,
            'category': category_id,
            'prompt': self.get_prompt_message(),
            'posts': Post.objects.all()
        })

    def get_prompt_message(self):
        available_prompt_messages = {
            DEFAULT_CATEGORY_CODE: 'Post a general message',
            'quotes': 'Post a Quote',
            'book-recommendations': 'Post a book recommendation'
            # to be continue ...
        }

        return available_prompt_messages.get(self.category_code, 'Post a general message')

    def process_keywords(self, keywords_string=''):
        if not keywords_string:
            return []

        keywords = keywords_string.split(',')
        if not keywords:
            return []

        keywords = [keyword.strip().lower() for keyword in keywords if keyword.strip()]
        keywords = [keyword for keyword in keywords if Keyword.objects.filter(name=keyword).count() == 0]
        return [Keyword.objects.create(name=keyword) for keyword in keywords]
