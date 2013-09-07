from django import http
from django.db import transaction
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from core.models import Material, Order
from core.forms import MaterialForm, AuthorForm, PublisherForm
from accounts.models import Profile

def index(request):
    if request.method == 'POST' and request.user.is_authenticated():
        material = get_object_or_404(Material, id=request.POST.get('material_id'))
        quantity = request.POST.get('quantity')
        print material, quantity
        with transaction.commit_on_success():
            quantity = int(quantity)
            if Order.objects.filter(reader=request.user, material=material):
                order = Order.objects.filter(reader=request.user, material=material)[0]
                order.quantity += quantity
                order.save(update_fields=['quantity'])
            else:
                Order.objects.create(reader=request.user, material=material, quantity=quantity)
            material.quantity -= quantity
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

@login_required
def check_out(request):
    orders = Order.objects.filter(reader=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'check_out.html', context)

@login_required
def account_reading_orders(request):
    orders = Order.objects.filter(reader=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'account/orders/reading.html', context)

@login_required
def account_giving_orders(request):
    orders = Order.objects.filter(material__giver=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'account/orders/giving.html', context)

@login_required
def ship_order(request, order_id):
    next = request.GET.get('next', '/')
    try:
        order = Order.objects.get(id=order_id, material__giver=request.user)
    except Order.DoesNotExist:
        pass
    else:
        order.ship_date = timezone.now()
        order.save(update_fields=['ship_date'])
    return redirect(next)

@login_required
def account_material(request):
    materials = Material.objects.filter(giver=request.user)
    context = {
        'materials': materials,
    }
    return render(request, 'account/material.html', context)

@login_required
def account_material_edit(request, material_id=None):
    material = None
    if material_id is not None:
        material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            new_material = form.save(commit=False)
            new_material.giver = request.user
            new_material.save()
            form.save_m2m()
            return redirect('account_material')
    else:
        form = MaterialForm(instance=material)
    context = {
        'form': form,
        'is_editing': material is not None,
    }
    return render(request, 'account/material_edit.html', context)

@login_required
def account_add_author(request):
    next = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next or 'account_material')
    else:
        form = AuthorForm()
    return render(request, 'account/add_author.html', {'form': form, 'next': next})

@login_required
def account_add_publisher(request):
    next = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next or 'account_material')
    else:
        form = PublisherForm()
    return render(request, 'account/add_publisher.html', {'form': form, 'next': next})
