# coding=utf-8
from django.views.generic import CreateView, ListView, DetailView, FormView, UpdateView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden
from django.db.models import Count
from .models import ItemCategory, TimelineItem, ItemTopic, Language
from .forms import LinkForm, TextForm, CommentForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from network.models import UserNetwork
from dal import autocomplete



class SubHeaderCategoryMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(SubHeaderCategoryMixin,
                        self).get_context_data(**kwargs)
        context['categories'] = ItemCategory.objects.get_all_catergories()
        if self.request.user.is_authenticated:
            context['languages'] = self.request.user.languages.all()
        else:
            context['languages'] = Language.objects.all().order_by('order')
        return context


class TopTopicMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(TopTopicMixin,
                        self).get_context_data(**kwargs)
        context['top_topics'] = ItemTopic.objects.annotate(topic_count=Count(
            'timelineitems')).order_by('-topic_count')[:50].values('id', 'name', 'topic_count')
        return context


class TimeLineItemListView(ListView):
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(TimeLineItemListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            like_items = TimelineItem.objects.all().filter(likes=self.request.user)
            context['likes_ids'] = [like_item.id for like_item in like_items]
        return context

    def get_queryset(self):
        queryset = TimelineItem.objects.all().order_by('-created')

        if 'category' in self.request.GET and self.request.GET['category']:
            queryset = queryset.filter(
                item_category__id=self.request.GET['category'])

        if 'topic' in self.request.GET and self.request.GET['topic']:
            queryset = queryset.filter(
                topics__id=self.request.GET['topic'])

        if 'usertype' in self.request.GET and self.request.GET['usertype'] == 'following' and self.request.user.is_authenticated:
            following_users = UserNetwork.objects.get_following_users(
                self.request.user)
            queryset = queryset.filter(created_user__in=following_users)

        if 'language' in self.request.GET and self.request.GET['language'] and self.request.GET['language'] != 'all':
            queryset = queryset.filter(
                language__id=self.request.GET['language'])
        return queryset


class Home(SubHeaderCategoryMixin, TopTopicMixin, TimeLineItemListView):
    template_name = 'home.html'
    paginate_by = 20


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


class ShareLinkUpdateView(SubHeaderCategoryMixin, UpdateView):
    form_class = LinkForm
    model = TimelineItem
    template_name = 'timeline/link_form.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(ShareLinkUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ShareTextUpdateView(SubHeaderCategoryMixin, UpdateView):
    template_name = 'timeline/text_form.html'
    model = TimelineItem
    form_class = TextForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(ShareTextUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class TimeLineItemView(SubHeaderCategoryMixin, DetailView):
    template_name = 'timeline/timelineitem_detail.html'
    model = TimelineItem

    def get_context_data(self, **kwargs):
        context = super(TimeLineItemView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def get_context_object_name(self, obj):
        return 'timelineitem'


class TimeLineItemComment(SingleObjectMixin, FormView):
    template_name = 'timeline/timelineitem_detail.html'
    form_class = CommentForm
    model = TimelineItem

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        return super(TimeLineItemComment, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('timelineitem_detail', kwargs={'pk': self.get_object().pk})

    def form_valid(self, form):
        form.instance.comment_user = self.request.user
        form.instance.item = self.get_object()
        form.save()
        return super(TimeLineItemComment, self).form_valid(form)



class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Country.objects.none()

        qs = Country.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs



@login_required
@require_POST
def reblog(request, timelineitem_id):
    timeline_item = get_object_or_404(TimelineItem, pk=timelineitem_id)
    timeline_item.reblog(request.user)
    response_data = {}
    response_data['reblog_count'] = timeline_item.total_reblogs
    return JsonResponse(response_data)


@login_required
@require_POST
def like_timelineitem(request, timelineitem_id):
    timeline_item = get_object_or_404(TimelineItem, pk=timelineitem_id)
    timeline_item.like(request.user)
    response_data = {}
    response_data['likes_count'] = timeline_item.total_likes
    return JsonResponse(response_data)


@login_required
@require_POST
def unlike_timelineitem(request, timelineitem_id):
    timeline_item = get_object_or_404(TimelineItem, pk=timelineitem_id)
    timeline_item.unlike(request.user)
    response_data = {}
    response_data['likes_count'] = timeline_item.total_likes
    return JsonResponse(response_data)
