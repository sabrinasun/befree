from django import http
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from core.models import Material
from accounts.models import Profile

def index(request):
    context = {
        'materials': Material.objects.all(),
    }
    return render(request, 'index.html', context)

def user_profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    profile = get_object_or_404(Profile, user=user)
    context = {
        'username': username,
        'user': user,
        'profile': profile,
    }
    return render(request, 'account/user_profile.html', context)
