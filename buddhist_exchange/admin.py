
from django.contrib import admin
from buddhist_exchange.models import Translator


class TranslatorAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False


admin.site.register(Translator, TranslatorAdmin)
