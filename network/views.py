# coding=utf-8
from .models import UserNetwork
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from timeline.views import SubHeaderCategoryMixin, TimeLineItemListView, TopTopicMixin


class UserPublicPage(SubHeaderCategoryMixin, TopTopicMixin, TimeLineItemListView):
    template_name = 'network/user_public.html'

    def get_context_data(self, **kwargs):
        context = super(UserPublicPage, self).get_context_data(**kwargs)
        view_user = User.objects.get(pk=self.kwargs['pk'])
        context['view_user'] = view_user
        if self.request.user.is_authenticated:
            context['has_followed'] = UserNetwork.objects.has_followed(
                view_user, self.request.user)
        else:
            context['has_followed'] = False
        context['follower_count'] = UserNetwork.objects.get_follower_count(
            view_user)
        context['following_count'] = UserNetwork.objects.get_following_count(
            view_user)
        context['post_count'] = view_user.user_items.count()
        return context

    def get_queryset(self):
        queryset = super(UserPublicPage, self).get_queryset()
        return queryset.filter(users__id=self.kwargs['pk'])


@login_required
@require_POST
def follow_user(request, follow_user_id):
    following_user = get_object_or_404(User, pk=follow_user_id)
    UserNetwork.objects.follow_user(request.user, following_user)
    response_data = {}
    response_data['follower_count'] = UserNetwork.objects.get_follower_count(
        following_user)
    return JsonResponse(response_data)


@login_required
@require_POST
def unfollow_user(request, unfollow_user_id):
    unfollow_user = get_object_or_404(User, pk=unfollow_user_id)
    UserNetwork.objects.unfollow_user(request.user, unfollow_user)
    response_data = {}
    response_data['follower_count'] = UserNetwork.objects.get_follower_count(
        unfollow_user)
    return JsonResponse(response_data)
