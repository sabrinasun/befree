# coding=utf-8
from django.views.generic import TemplateView, CreateView
from django.views.generic.base import ContextMixin
from .models import ItemCategory, TimelineItem
from .forms import LinkForm, TextForm
from django.core.urlresolvers import reverse_lazy


class SubHeaderCategoryMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(SubHeaderCategoryMixin,
                        self).get_context_data(**kwargs)
        context['categories'] = ItemCategory.objects.get_all_catergories()
        return context


class Home(SubHeaderCategoryMixin, TemplateView):
    template_name = 'home.html'


class ShareLink(SubHeaderCategoryMixin, CreateView):
    form_class = LinkForm
    model = TimelineItem
    template_name = 'timeline/link_form.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(ShareLink, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ShareText(SubHeaderCategoryMixin, CreateView):
    template_name = 'timeline/text_form.html'
    model = TimelineItem
    form_class = TextForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(ShareText, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
