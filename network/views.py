# coding=utf-8
from django.views.generic import TemplateView
from .models import UserNetwork
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


class UserPublicPage(TemplateView):
    template_name = 'network/user_public.html'

    def get_context_data(self, **kwargs):
        context = super(UserPublicPage, self).get_context_data(**kwargs)
        view_user = User.objects.get(pk=self.kwargs['pk'])
        context['view_user'] = view_user
        context['has_followed'] = UserNetwork.objects.has_followed(
            view_user, self.request.user)
        context['follower_count'] = UserNetwork.objects.get_follower_count(
            view_user)
        context['following_count'] = UserNetwork.objects.get_following_count(
            view_user)
        return context


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
