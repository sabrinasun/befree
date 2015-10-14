from django.contrib import admin

from network.models import Post, Category


class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', )
    ordering = ('id', )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post)
