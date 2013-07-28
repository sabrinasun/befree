from django.contrib import admin
from core.models import *

class MaterialAdmin(admin.ModelAdmin):
    filter_horizontal = ('author', )

admin.site.register(Material, MaterialAdmin)

admin.site.register(Author)
