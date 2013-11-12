from django.contrib import admin
from core.models import *

class MaterialAdmin(admin.ModelAdmin):
    filter_horizontal = ('author', )
    #~ save_as = True

admin.site.register(Material, MaterialAdmin)
admin.site.register(GiverMaterial)

admin.site.register(Author)

admin.site.register(Order,
    list_display = ('reader', 'giver'),
)

admin.site.register(OrderDetail)

admin.site.register(Publisher)
