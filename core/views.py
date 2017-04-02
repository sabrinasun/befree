from django import http
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.utils.html import escape
from django.forms.models import modelform_factory
from django.utils.translation import ugettext as _


try:
    from django.db.models.loading import get_models
except ImportError:
    from django.apps import apps
    get_model = apps.get_model


from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView

from userena.views import signup as userena_signup
from math import ceil
from decimal import Decimal

from core.models import Material, GiverMaterial, Order, OrderDetail, Category
from core.forms import MaterialForm, AuthorForm, PublisherForm, GiverMaterialForm, ContactForm, PayForm, ShippingCostForm
from accounts.models import Profile

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

from django.db.models import Q


def get_apps():
    return settings.INSTALLED_APPS

def send_email(template, context, title, to_address):
    template = get_template('email/' + template)
    content = template.render(context)
    send_mail(title, content, settings.DEFAULT_FROM_EMAIL,[to_address], fail_silently=False)

def index(request):
    msg = None
    inventories = None
    ebooks = None
    lang = ""
    location = ""
    cat = ""

    if request.method == 'POST':
        inventory = get_object_or_404(GiverMaterial,
                                      id=request.POST.get('inventory_id'))

        #quantity = int(request.POST.get('quantity', 0))
        quantity = 1
        """
        if request.user.is_authenticated():
            update_orders(request.user, material, quantity)
        else:
        """
        cart = request.session.get("cart", {})
        cart[str(inventory.pk)] = quantity + cart.get(str(inventory.pk), 0)
        request.session["cart"] = cart
    else:
        msg = request.GET.get('msg','')
        cat = request.GET.get('cat', '')
        lang = request.GET.get('lang', None) or request.session.get('lang',
                                                                    '')
        location = request.GET.get('loc', None) or request.session.get(
            "location", '')

    inventories = GiverMaterial.objects.all().order_by(
        'material__title').filter(quantity__gt=-1, status='ACTIVE')

    ebooks = Material.objects.all().filter (givermaterial__isnull=True)

    category = None

    if cat != 'all' and cat != '':
        inventories = inventories.filter(material__category = cat)
        category = Category.objects.get(pk = cat)
        ebooks =  ebooks.filter( category = cat)

    if lang != 'all' and lang != '':
        inventories = inventories.filter(material__language=lang)

    if location != 'all' and location != '':
        #users = [p.user for p in Profile.objects.all().filter( Q(state=location) | Q(domestic_pay_shipping='TRUE') | Q(domestic_free_shipping='TRUE') | Q(international_free_shipping='TRUE') )]
        #inventories = inventories.filter(giver__in=users)
        inventories = inventories.filter(
            Q(giver__profile__state=location) & (Q(
                giver__profile__domestic_pay_shipping=True) | Q(
                giver__profile__domestic_free_shipping=True) | Q(
                giver__profile__international_free_shipping=True)))

    request.session["lang"] = lang
    request.session["location"] = location
    request.session["cat"] = cat

    context = {
        'inventories': inventories,
        'msg': msg,
        'lang':lang,
        'location':location
    }

    # get categories and books in them
    #categories = dict(count=0, items=list())
    cats = Category.objects.all()
    #categories['count'] = cats.count()
    categories = [{'item':{'name':'All Categories', 'pk':'all'}, 'count':Material.objects.count()}]

    for cat in cats:
        count = Material.objects.filter(category=cat).count()
    #    item = dict(title=category.name, materials=count)
        categories.append( { 'item':cat, 'count':count} )

    context['categories'] = categories
    context['category'] = category
    context['ebooks'] = ebooks


    return render(request, 'index.html', context)

def user_profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    profile = get_object_or_404(Profile, user=user)
    inventory = GiverMaterial.objects.filter(giver = user)
    context = {
        'username': username,
        'user': user,
        'profile': profile,
        'inventory': inventory
    }
    return render(request, 'account/user_profile.html', context)

"""
up to 1 pound: $2.53 + Packaging: $0.50
Up to 2 pounds: $2.98 + Packaging: $0.50
Up to 3 pounds: $3.43 + Packaging: $1.00
Up to 4 pounds: $3.88 + Packaging: $1.10
Up to 5 pounds: $4.33 + Packaging: $1.20
Up to 6 pounds: $4.78 + Packaging: $1.30
Up to 7 pounds: $5.23 + Packaging: $1.40
The increments for shipping cost are 43 cents per pound, plus packaing cost 10 cents, all the way up to $32.32 for the 70 lbs max.
"""
def get_shipping_cost(weight):
    weight = ceil(weight/16)
    shipping_cost = 0
    packaging_cost = 0
    if weight <= 7:
        shipping_cost = {0:0, 1:2.53, 2:2.98, 3:3.43, 4:3.88, 5:4.33, 6:4.78,7:5.23}[weight]
        packaging_cost= {0:0, 1:0.50, 2:0.50, 3:1.00, 4:1.10, 5:1.20, 6:1.30, 7:1.40}[weight]
    else:
        shipping_cost = 5.23 + .43 * ( weight - 7)
        packaging_cost = 1.40 + (weight-7)*.10

    return shipping_cost+packaging_cost

def get_order_from_bag(cart, user):
    inventories = GiverMaterial.objects.filter( pk__in = [ int(id) for id in cart ] ).order_by('giver__username', 'material__title')

    orders = {}
    for item in inventories:
        username = item.giver.username
        order_details = orders.get(username)
        detail = {"inventory": item, "quantity": cart[str(item.pk)]}
        if order_details:
            order_details.append(detail)
        else:
            order_details = [detail]
        orders[username]=order_details

    ret = []
    for key in orders:
        order_details = orders[key]
        weight = 0
        price = 0
        free_count = 0

        for detail in order_details:
            weight += detail['inventory'].material.weight
            price += detail['inventory'].price

            if price == 0:
                free_count += detail['quantity']

        #shipping cost according to location
        giver = detail['inventory'].giver
        shipping_cost = -1
        giver_country = giver.profile.country
        user_country = user.profile.country

        if giver_country == 'US' and  user_country == 'US':
            shipping_cost = get_shipping_cost(weight)

        shipping_cost_wave = False
        if giver_country == user_country:
            if giver.profile.domestic_free_shipping:
                shipping_cost_wave = True
        elif giver.profile.international_free_shipping:
            shipping_cost_wave = True

        warning = []
        if shipping_cost == -1:
            warning.append(_("We can't determine shipping cost. Wait for giver's advice after placing order. "))

        max_per_order = giver.profile.max_per_order
        if max_per_order != 0 and free_count > max_per_order:
            warning.append(_("You ordered %s items, which are more than a small quantity order of %s items for this giver, order will be in pending status until the giver approves it.") % (free_count,max_per_order)  )

        ret.append( {"giver":orders[key][0]['inventory'].giver, "order_details":orders[key], "price":price, "shipping_cost":shipping_cost,"total":"%.2f" % (price+Decimal(shipping_cost)), "weight":weight, "warning":warning, "shipping_cost_wave":shipping_cost_wave })

    return ret

def validate_orders():
    pass

def view_bag(request):
    outofstock_id = request.GET.get('outofstock_id','-1')
    cart = request.session.get("cart", {})

    if not request.user.is_authenticated():
        return redirect('/accounts/signup_reader/')
    elif not request.user.profile.has_reader_profile():
        return redirect(reverse_lazy('userena_profile_edit_from_view_bag', args=[request.user.username]) )

    orders = get_order_from_bag(cart, request.user)
    #validate orders

    context = { "orders": orders, "action":"view_bag", "outofstock_id": int(outofstock_id) }
    return render(request, 'show_order.html', context)

def view_bag_delete(request, inventory_id):
    #delete everything from cart that has inventory id 1
    cart = request.session.get("cart", {})
    del cart[str(inventory_id)]
    request.session["cart"] = cart
    orders = get_order_from_bag(cart, request.user)
    context = { "orders": orders, "action":"view_bag" }
    return render(request, 'show_order.html', context)

def contact_user(request):
    user_id = None
    user = None
    contact_form  = None

    if request.method == "POST":
        contact_form = ContactForm(data = request.POST)
        if contact_form.is_valid():
            to_user = get_object_or_404(get_user_model(), id = contact_form.cleaned_data['user_id'] )
            message =  contact_form.cleaned_data['message']
            context = Context({'to_user': to_user.profile.get_display_name(),
                               'from_user': request.user.profile.get_display_name(),
                               'from_user_id': request.user.pk,
                               'message': message
                              })
            title = _("User %s has sent you a message via BuddhistExchange. ") % request.user.profile.get_display_name()
            send_email('contact-user.txt', context, title, to_user.email)
            return HttpResponse('<script type="text/javascript">document.write("Your message has been sent.");window.close();opener.alert("You email message has been sent.");</script>')

    else:
        user_id = int(request.GET.get('user_id'))
        user = get_object_or_404(get_user_model(), id = user_id )
        contact_form  = ContactForm(initial = request.GET)

    context = {"form": contact_form,
               "user": user}

    if not request.user.is_authenticated():
        return HttpResponse('<script type="text/javascript">alert("Please login to your account before you access the contact link.");document.location="/";</script>')

    return render(request, 'contact.html', context)

def check_out(request):
    shipping_wave = request.POST.getlist('shipping_wave')
    shipping_wave = [int(i) for i in shipping_wave]

    #if not login, need to redirect to reader login page
    if not request.user.is_authenticated():
        return redirect('/accounts/signup_reader/')


    cart = request.session['cart']
    orders = get_order_from_bag( cart, request.user)

    #[{'giver': <User: sunnywebtimes>,'order_details': [{'inventory': <GiverMaterial: GiverMaterial object>,'quantity': 1}],'price': 20}
    reader = request.user
    for one_order in orders:
        for item in one_order['order_details']:
            inventory = item['inventory']
            quantity  = item['quantity']
            left = inventory.quantity - quantity

            if ( left <0):
                return redirect('/view_bag?outofstock_id=' + str(inventory.id) )

    # if already login, need to validate the order
    # loop through the car to display order.

    cart = request.session.pop('cart', {})

    for one_order in orders:
        with transaction.atomic():
            giver = one_order['giver']
            order = Order.objects.create(reader=reader, giver = giver)

            shipping_cost = one_order['shipping_cost']
            status = 'NEW'
            if giver.id in shipping_wave:
                shipping_cost = 0
                one_order['shipping_cost'] = 0
                one_order['total'] = one_order['price']
            if shipping_cost == 0:
                status = "PAID"
            if shipping_cost == -1:
                status = "PENDING"

            order.shipping_cost = shipping_cost
            order.total_price = one_order['price']
            order.status = status

            order.save()

            total_free_item = 0

            for item in one_order['order_details']:
                inventory = item['inventory']
                quantity  = item['quantity']
                inventory.quantity -= quantity
                inventory.save(update_fields=['quantity'])
                total_free_item += quantity
                detail = OrderDetail.objects.create(order=order, inventory=inventory, quantity=quantity)
                detail.save()

            max_per_order = giver.profile.max_per_order
            if max_per_order != 0 and total_free_item > max_per_order:
                order.status = "PENDING"
                order.save()

            giver = one_order['giver']
            context = Context({ 'shipping_address': order.reader.profile.get_shipping_address(),
                                'total_free_item': total_free_item,
                                'max_per_order': max_per_order,
                                'giver_name': giver.profile.get_display_name(),
                                'reader_name': reader.profile.get_display_name(),
                                'order_number': order.pk,
                                'shipping_cost': order.shipping_cost,
                                'order_details': OrderDetail.objects.filter(order=order)})

            title = _('Order %s was placed by %s via BuddhistExchange.') % ( order.pk , reader.profile.get_display_name())
            send_email('email-giver-order-placed.txt', context, title,giver.email)

            title = _('You have placed an order via BuddhistExchange.')
            send_email('email-reader-order-placed.txt', context, title, reader.email)

    context = {
        'orders': orders,
        'action': "check_out"
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
    cart = request.session.get('cart', {})
    test = cart.values()
    pending_items = len (cart.values())
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
        'msg': request.GET.get('msg'),
        'pending_items' : pending_items
    }
    return render(request, 'account/summary.html', context)

@login_required
def account_reading_orders(request):
    order_id = request.GET.get('order_id')
    status   = request.GET.get('status')

    if order_id:
        order_id = int(order_id)
        order = Order.objects.get(id = order_id)
        order.status = status

        if status == 'CANCEL':
            order.cancel_date = timezone.now()
        order.save()

        context = Context(
                  {'reader_name': order.reader.profile.get_display_name(),
                   'order_number': order_id,
                   'giver_name': order.giver.profile.get_display_name(),
                   'shipping_cost': order.shipping_cost,
                   'order_details': OrderDetail.objects.filter(order=order)
                    })

        title = "Your order %s has been cancelled. " % order.pk
        send_email('email-reader-order-cancelled-by-reader.txt', context, title, order.reader.email)
        title = "You have cancelled order %s. " % order.pk
        send_email('email-giver-order-cancelled-by-reader.txt', context, title, order.giver.email)


    order_details = OrderDetail.objects.filter(order__reader = request.user )
    orders = Order.objects.filter(reader = request.user).order_by('-order_date')

    ret = [{'order':order, 'detail': order_details.filter(order = order) } for order in orders]

    #{'orders': [{'details': [<OrderDetail: OrderDetail object>], 'order': <Order: Order object>}]}
    context = {
        'orders': ret
    }

    return render(request, 'account/orders/reading.html', context)

@login_required
def account_giving_orders(request):
    order_id = request.GET.get('order_id')
    status   = request.GET.get('status')

    if order_id:
        order_id = int(order_id)
        order = Order.objects.get(id = order_id)
        order.status = status
        if status == "SHIPPED":
            order.ship_date = timezone.now()
        if status == "CANCEL":
            order.cancel_date = timezone.now()
        order.save() #order.save(update_fields=['ship_date'])

        context = Context(
                  {'reader_name': order.reader.profile.get_display_name(),
                   'order_number': order_id,
                   'giver_name': request.user.profile.get_display_name(),
                   'shipping_cost': order.shipping_cost,
                   'order_details': OrderDetail.objects.filter(order=order)
                    })
        #here send email for changing status.
        if status == "SHIPPED":
            title = _("Your order %s has been shipped. ") % order.pk
            send_email('email-reader-order-shipped.txt', context, title, order.reader.email)

        elif status == "CANCEL":
            title = _("Your order %s has been cancelled. ") % order.pk
            send_email('email-reader-order-cancelled-by-giver.txt', context, title, order.reader.email)
            title = _("You have cancelled order %s. ") % order.pk
            send_email('email-giver-order-cancelled-by-giver.txt', context, title, order.giver.email)

        elif status == "NEW":
            title = _("Your order %s has been approved. ") % order.pk
            send_email('email-reader-order-approved.txt', context, title, order.reader.email)
            title = _("You have approved order %s. ") % order.pk
            send_email('email-giver-order-approved.txt', context, title, order.giver.email)

    #below happens when pending
    shipping_form = None
    if request.method == "POST":
        shipping_form = ShippingCostForm(data=request.POST)
        if shipping_form.is_valid():
            order = Order.objects.get(id=shipping_form.cleaned_data['order_id'])
            order.shipping_cost = shipping_form.cleaned_data['shipping_cost']

            #check the total quantity of the order
            quantity = 0
            for detail in OrderDetail.objects.filter(order=order):
                quantity += detail.quantity

            max_per_order = order.giver.profile.max_per_order
            if max_per_order != 0 and quantity > max_per_order:
                order.status = 'PENDING'
            else:
                order.status = 'NEW'
            order.save()

            context = Context(
                      {'reader_name': order.reader.profile.get_display_name(),
                       'order_number': order.pk,
                       'giver_name': order.giver.profile.get_display_name(),
                       'shipping_cost': order.shipping_cost,
                       'order_details': OrderDetail.objects.filter(order=order),
                       'order_status': order.status
                        })
            title = _("The shipping cost for your order %s is $%s. ") % ( order.pk, order.shipping_cost)
            send_email('email-reader-order-shipping-cost.txt', context, title, order.reader.email)


    order_details = OrderDetail.objects.filter(order__giver = request.user )
    orders = Order.objects.filter(giver = request.user).order_by('-order_date')

    ret = [{'order':order, 'detail': order_details.filter(order = order) } for order in orders]

    #{'orders': [{'details': [<OrderDetail: OrderDetail object>], 'order': <Order: Order object>}]}
    context = {
        'orders': ret
    }

    if shipping_form and not shipping_form.is_valid():
        context['form'] = shipping_form
        context['form_order_id'] = shipping_form.cleaned_data['order_id']

    return render(request, 'account/orders/giving.html', context)


@login_required
def account_material(request):

    if not request.user.profile.has_giver_profile():
        return redirect(reverse_lazy('userena_profile_edit_from_inventory', args=[request.user.username]))
    inventory = GiverMaterial.objects.filter(giver=request.user)
    inventory_ids = [item.material.id for item in inventory]

    materials = Material.objects.exclude(id__in=inventory_ids)

    context = {
       'inventory': inventory,
       'materials': materials

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
    from django.apps import apps
    if (model_name.lower() == model_name):
            normal_model_name = model_name.capitalize()
    else:
        normal_model_name = model_name
    app_list = get_apps()
    for app in app_list:
        for model in apps.get_models(app):
            if model.__name__ == normal_model_name:
                form = modelform_factory(model, exclude=())

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
                return render(request, 'popup.html', page_context)

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
        messages.success(request, _('You have been signed up.'))
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

def pay_giver(request):
    pay_form =  None
    order = None
    user_display_name = request.user.profile.get_display_name()

    if request.method == "POST":
        pay_form = PayForm(data = request.POST)
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        if pay_form.is_valid():
            pay_method = pay_form.cleaned_data['pay_method']
            if pay_method == "other":
                pay_method = "'other payment method' you specified in your giver's profile"
            message = pay_form.cleaned_data['message']
            giver_email = order.giver.email
            order.payment_detail ="Type: %s. Message: %s " % (pay_method, message)
            order.status = 'PAID'
            order.save()

            context = Context({'shipping_address': order.reader.profile.get_shipping_address(),
                       'giver_name': order.giver.profile.get_display_name(),
                       'order_number':order.pk,
                       'reader_name': user_display_name,
                       'payment_method': pay_method ,
                       'payment_note': message,
                       'shipping_cost': order.shipping_cost,
                       'order_details': OrderDetail.objects.filter(order=order) })

            title = 'Order No.%s is paid per reader %s ' % ( order.pk , user_display_name )

            send_email('email-giver-order-paid.txt', context, title, giver_email)
            send_email('email-reader-order-paid.txt', context, title, request.user.email)

            return HttpResponse('<script type="text/javascript">opener.location="/account/orders/reading/";window.close();</script>')

    else:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id=order_id)
        pay_form  = PayForm(initial = request.GET)

    context = {"form": pay_form, "order":order}
    return render(request, 'pay_giver.html', context)

def file_claim(request):
    context = {}
    return render(request, 'file_claim.html', context)
