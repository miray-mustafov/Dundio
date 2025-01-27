from modeltranslation.translator import register, TranslationOptions
from .models import Order


@register(Order)
class OrderTranslations(TranslationOptions):
    fields = ('name', 'populated_place',)
