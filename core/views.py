from django import http
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from core.models import Material, Order
from accounts.models import Profile

def index(request):
    if request.method == 'POST' and request.user.is_authenticated():
        material = get_object_or_404(Material, id=request.POST.get('material_id'))
        quantity = request.POST.get('quantity')
        print material, quantity
        with transaction.commit_on_success():
            Order.objects.create(reader=request.user, material=material, quantity=quantity)
            material.quantity -= int(quantity)
            material.save(update_fields=['quantity'])
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
