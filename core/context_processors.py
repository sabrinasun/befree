
from core.models import Order

def order(request):
    context = {}
    context['order_items_count'] = 0
    if request.user.is_authenticated():
        items = sum(Order.objects.filter(reader=request.user).values_list('quantity', flat=True))
        context['order_items_count'] = items
    return context
