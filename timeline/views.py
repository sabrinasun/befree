# coding=utf-8
from django.views.generic import CreateView, ListView, DetailView, FormView, UpdateView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Count
from .models import ItemCategory, TimelineItem, ItemTopic, Language, Teacher
from .forms import LinkForm, TextForm, CommentForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from network.models import UserNetwork
from django.utils.translation import ugettext as _
from django.utils.translation import activate, get_language


class SubHeaderCategoryMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(SubHeaderCategoryMixin,
                        self).get_context_data(**kwargs)
        context['categories'] = ItemCategory.objects.get_all_catergories()
        if self.request.user.is_authenticated:
            context['languages'] = self.request.user.languages.all()
        else:
            context['languages'] = Language.objects.all()

        if 'category_slug' in self.kwargs:
            context['category_slug'] = self.kwargs['category_slug']
        else:
            context['category_slug'] = 'all'

        if 'topic_slug' in self.kwargs:
            context['topic_slug'] = self.kwargs['topic_slug']
        else:
            context['topic_slug'] = 'all'
        return context


class TopTopicMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(TopTopicMixin,
                        self).get_context_data(**kwargs)
        context['top_topics'] = ItemTopic.objects.filter(timelineitems__language__in=Language.objects.filter(lang_code=get_language(
        ))).annotate(topic_count=Count('timelineitems')).order_by('-topic_count')[:50].values('id', 'slug', 'name', 'topic_count')

        if 'topic_slug' in self.kwargs:
            context['topic_slug'] = self.kwargs['topic_slug']
        else:
            context['topic_slug'] = 'all'
        return context


class TimeLineItemListView(ListView):
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(TimeLineItemListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            like_items = TimelineItem.objects.all().filter(likes=self.request.user)
            context['likes_ids'] = [like_item.id for like_item in like_items]

        if 'category_slug' in self.kwargs and self.kwargs['category_slug'] != 'all':
            category = ItemCategory.objects.get(
                slug=self.kwargs['category_slug'])
            context['search_category'] = category.name
        else:
            context['search_category'] = _('All')

        if 'topic_slug' in self.kwargs and self.kwargs['topic_slug'] != 'all':
            context['search_topic'] = ItemTopic.objects.get(
                slug=self.kwargs['topic_slug'])
        else:
            context['search_topic'] = _('All')

        context['search_language'] = Language.objects.get(
            lang_code=get_language())
        return context

    def get_queryset(self):
        queryset = TimelineItem.objects.all().order_by('-created')

        if 'category_slug' in self.kwargs and self.kwargs['category_slug'] != 'all':
            queryset = queryset.filter(
                item_category__slug=self.kwargs['category_slug'])

        if 'topic_slug' in self.kwargs and self.kwargs['topic_slug'] != 'all':
            queryset = queryset.filter(
                topics__slug=self.kwargs['topic_slug'])

        if 'language' in self.request.GET and self.request.GET['language']:
            queryset = queryset.filter(
                language__id=self.request.GET['language'])
            language = Language.objects.get(
                id=self.request.GET['language'])
            activate(language.lang_code)
        else:
            queryset = queryset.filter(
                language__lang_code=get_language())
        return queryset


class Home(SubHeaderCategoryMixin, TopTopicMixin, TimeLineItemListView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        if 'usertype' in self.request.GET and self.request.GET['usertype'] and self.request.GET['usertype'] == 'following':
            context['search_usertype'] = _('People I Follow')
        else:
            context['search_usertype'] = _('Everyone')

        context['msg'] = self.request.GET.get('msg', '')
        return context

    def get_queryset(self):
        queryset = super(Home, self).get_queryset()
        if 'usertype' in self.request.GET and self.request.GET['usertype'] == 'following' and self.request.user.is_authenticated:
            following_users = UserNetwork.objects.get_following_users(
                self.request.user)
            queryset = queryset.filter(created_user__in=following_users)
        return queryset


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
    slug_url_kwarg = 'post_slug'

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
        return reverse('timelineitem_detail', kwargs={'post_slug': self.get_object().slug, 'category_slug': 'all', 'topic_slug': 'all'})

    def form_valid(self, form):
        form.instance.comment_user = self.request.user
        form.instance.item = self.get_object()
        form.save()
        return super(TimeLineItemComment, self).form_valid(form)


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


@require_GET
def retrieve_titles(request):
    title = request.GET.get('title', None)
    response_data = {}
    if title:
        titles = TimelineItem.objects.filter(
            title__istartswith=title).values_list('title', flat=True).distinct()[:10]
        response_data['titles'] = list(titles)
    return JsonResponse(response_data)


@require_GET
def retrieve_topics(request):
    topic = request.GET.get('topic', None)
    response_data = {}
    if topic:
        topics = ItemTopic.objects.filter(
            name__istartswith=topic).values_list('name', flat=True).distinct()
        response_data['topics'] = list(topics)
    return JsonResponse(response_data)


@require_GET
def retrieve_teachers(request):
    teacher = request.GET.get('teacher', None)
    response_data = {}
    if teacher:
        teachers = Teacher.objects.filter(
            name__istartswith=teacher).values_list('name', flat=True).distinct()
        response_data['teachers'] = list(teachers)
    return JsonResponse(response_data)
