from django.contrib import admin
from network.models import Post, Category, Keyword


class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'code')
    ordering = ('id',)


class KeywordAdmin(admin.ModelAdmin):
    fields = ('name',)
    ordering = ('name',)


class PostsAdmin(admin.ModelAdmin):
    ordering = ('id',)
    readonly_fields = ('last_update',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostsAdmin)
admin.site.register(Keyword, KeywordAdmin)
