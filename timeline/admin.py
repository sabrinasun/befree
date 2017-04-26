from django.contrib import admin
from .models import Language, ItemCategory, ItemTopic, Teacher
from modeltranslation.admin import TranslationAdmin
# Register your models here.


class ItemCategoryAdmin(TranslationAdmin):
    list_display = ('order', 'name', 'link_form', 'text_form')
    pass


admin.site.register(ItemTopic)
admin.site.register(Teacher)
admin.site.register(Language,
                    list_display=('order', 'name', 'lang_code')
                    )
# admin.site.register(ItemCategory,
#                     list_display=('order', 'name', 'link_form', 'text_form')
#                     )
admin.site.register(ItemCategory, ItemCategoryAdmin)
