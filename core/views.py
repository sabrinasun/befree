from django import http
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.utils.html import escape
from django.forms.models import modelform_factory
from django.db.models.loading import get_models, get_app, get_apps
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView

from userena.views import signup as userena_signup

from core.models import Material, GiverMaterial, Order, OrderDetail
from core.forms import MaterialForm, AuthorForm, PublisherForm, GiverMaterialForm
from accounts.models import Profile
                  
def index(request):
    if request.method == 'POST':
        inventory = get_object_or_404(GiverMaterial, id=request.POST.get('inventory_id'))
        quantity = int(request.POST.get('quantity', 0))
        
        """
        if request.user.is_authenticated():
            update_orders(request.user, material, quantity)
        else:
        """
        cart = request.session.get("cart", {})
        cart[inventory.pk] = quantity + cart.get(inventory, 0)
        request.session["cart"] = cart
    
    inventories =  GiverMaterial.objects.all().order_by('material__title')
    
    context = {
        'inventories': inventories,
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

def get_order_from_bag(cart):
    inventories = GiverMaterial.objects.filter( pk__in = [ int(id) for id in cart ] ).order_by('giver__username', 'material__title')

    orders = {}
    for item in inventories:
        username = item.giver.username    
        order_details = orders.get(username)
        detail = {"inventory": item, "quantity": cart[item.pk]}
        if order_details: 
            order_details.append(detail)
        else:
            order_details = [detail]
        orders[username]=order_details
    ret = [{"giver":orders[key][0]['inventory'].giver, "order_details":orders[key], "price":20 } for key in orders ]    
    return ret
    
def view_bag(request):
    cart = request.session.get("cart", {})    
    ret = get_order_from_bag(cart)
    context = { "orders": ret } 
    return render(request, 'show_order.html', context)    
    

def check_out(request):
    #if not login, need to redirect to reader login page
    if not request.user.is_authenticated():
        return redirect('/accounts/signup_reader/')

    # if already login, need to validate the order
    # loop through the car to display order.
    cart = request.session.pop('cart', {})
    orders = get_order_from_bag( cart)
    
    #[{'giver': <User: sunnywebtimes>,'order_details': [{'inventory': <GiverMaterial: GiverMaterial object>,'quantity': 1}],'price': 20}
    reader = request.user
    for one_order in orders: 
        with transaction.commit_on_success():
            order = Order.objects.create(reader=reader, giver = one_order['giver'])
            order.save()
                                
            for item in one_order['order_details']: 
                inventory = item['inventory']
                quantity  = item['quantity']
                inventory.quantity -= quantity
                inventory.save(update_fields=['quantity'])
                detail = OrderDetail.objects.create(order=order, inventory=inventory, quantity=quantity)
                detail.save()

    context = {
        'orders': orders
    }
    return render(request, 'show_order.html', context)

@login_required
def confirm_check_out(request):
    """
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
    """
    pass


@login_required
def account_summary(request):
    reading_orders = Order.objects.filter(reader=request.user)
    giver_materials = GiverMaterial.objects.filter(giver=request.user)
    giving_orders = Order.objects.filter(giver=request.user)
    materials = Material.objects.filter(id__in=
                [g.material.pk for g in giver_materials if g.material])
    context = {
        'reading_orders_new': reading_orders.filter(ship_date=None, pay_date=None).count(),
        'reading_orders_shipped': reading_orders.exclude(ship_date=None).filter(pay_date=None).count(),
        'reading_orders_delivered': reading_orders.exclude(pay_date=None).count(),
        'giving_orders_new': giving_orders.filter(ship_date=None, pay_date=None).count(),
        'giving_orders_shipped': giving_orders.exclude(ship_date=None).filter(pay_date=None).count(),
        'giving_orders_delivered': giving_orders.exclude(pay_date=None).count(),
        'materials_active': giver_materials.filter(status='Active').count(),
        'materials_inactive': giver_materials.filter(status='Inactive').count(),
    }
    return render(request, 'account/summary.html', context)

@login_required
def account_reading_orders(request):
    order_details = OrderDetail.objects.filter(order__reader = request.user )
    orders = Order.objects.filter(reader = request.user).order_by('order_date')
    
    ret = [{'order':order, 'detail': order_details.filter(order = order) } for order in orders]
        
    #{'orders': [{'details': [<OrderDetail: OrderDetail object>], 'order': <Order: Order object>}]}    
    context = {
        'orders': ret
    }
    
    return render(request, 'account/orders/reading.html', context)

@login_required
def account_giving_orders(request):
    order_details = OrderDetail.objects.filter(order__giver = request.user )
    orders = Order.objects.filter(giver = request.user).order_by('order_date')
    
    ret = [{'order':order, 'detail': order_details.filter(order = order) } for order in orders]
        
    #{'orders': [{'details': [<OrderDetail: OrderDetail object>], 'order': <Order: Order object>}]}    
    context = {
        'orders': ret
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

    giver_materials = GiverMaterial.objects.filter(giver=request.user)

    materials = Material.objects.all()
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
def add_new_model(request, model_name):
    if (model_name.lower() == model_name):
            normal_model_name = model_name.capitalize()
    else:
        normal_model_name = model_name
    app_list = get_apps()
    for app in app_list:
        for model in get_models(app):
            if model.__name__ == normal_model_name:
                form = modelform_factory(model)
            
                if request.method == 'POST':
                    form = form(request.POST)
                    if form.is_valid():
                        try:
                            new_obj = form.save()
                        except forms.ValidationError as error:
                            new_obj = None
                    
                        if new_obj:
                            return HttpResponse('<script type="text/javascript">opener.location.reload();window.close();</script>')
                else:
                    form = form()
                page_context = {'form': form, 'field': normal_model_name}
                return render_to_response('popup.html', page_context, context_instance=RequestContext(request))

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

def signup(request, **kwargs):
    response = userena_signup(request, **kwargs)
    if response.status_code == 302:
        messages.success(request, 'You have been signed up.')
    return response
    

class GiverMaterialCreateView(CreateView):
    model = GiverMaterial
    form_class = GiverMaterialForm
    success_url = reverse_lazy("account_material")
    template_name = "account/givermaterial_form.html"
    
    def get_initial(self):
        initial = super(GiverMaterialCreateView, self).get_initial()
        material_pk = self.request.GET.get('material', '')
        if material_pk:
            initial['material'] = Material.objects.get(pk=material_pk)
        initial['giver'] = self.request.user
        return initial
        
        
class GiverMaterialEditView(UpdateView):
    model = GiverMaterial
    form_class = GiverMaterialForm
    success_url = reverse_lazy("account_material")
    template_name = "account/givermaterial_form.html"
    
    def get_object(self, queryset=None):
        obj = GiverMaterial.objects.get(pk=self.kwargs['pk'])
        return obj

