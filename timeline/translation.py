from modeltranslation.translator import register, TranslationOptions
from .models import ItemCategory


@register(ItemCategory)
class ItemCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
