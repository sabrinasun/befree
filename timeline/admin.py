from django.contrib import admin
from .models import Language, ItemCategory, ItemTopic, Teacher

# Register your models here.
admin.site.register(ItemTopic)
admin.site.register(Teacher)
admin.site.register(Language,
                    list_display=('order', 'name', 'lang_code')
                    )
admin.site.register(ItemCategory,
                    list_display=('order', 'name', 'link_form', 'text_form')
                    )
