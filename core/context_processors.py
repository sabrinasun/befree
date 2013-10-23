
from core.models import Order

def order(request):
    context = {}
    cart = request.session.get('cart', {})
    count = 0
    for key in cart.values(): 
        count += key
    context['order_items_count'] = count
        
    if request.user.is_authenticated():
        items = sum(Order.objects.filter(reader=request.user).values_list('quantity', flat=True))
        context['order_items_count'] = items
    return context
