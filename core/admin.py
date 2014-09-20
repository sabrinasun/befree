from django.contrib import admin
from core.models import *

#class MaterialAdmin(admin.ModelAdmin):
#    filter_horizontal = ('author', )
    #~ save_as = True

admin.site.register(Material, 
    list_display = ('id','title','publisher','weight','price','language','create_date')
)
admin.site.register(GiverMaterial, 
    list_display = ('id','giver', 'material','condition','price','quantity','status', 'create_date'),
)

admin.site.register(Author,
    list_display = ('id','name')                    
)

admin.site.register(Order,
    list_display = ('id','reader', 'giver', 'shipping_cost', 'total_price', 'payment_detail', 'status','order_date','ship_date','pay_date','cancel_date'),
)

admin.site.register(OrderDetail,
    list_display = ('id','order','inventory','quantity')
)

admin.site.register(Publisher,
    list_display = ('id','name')                    
)
