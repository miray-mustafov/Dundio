from modeltranslation.translator import register, TranslationOptions
from .models import PromotionalPackage


@register(PromotionalPackage)
class PromotionalPackageTranslations(TranslationOptions):
    fields = ('title', 'slug', 'meta_title', 'meta_description', 'meta_key_words',)
