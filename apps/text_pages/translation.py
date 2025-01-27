from modeltranslation.translator import register, TranslationOptions
from .models import TextPage, FooterMenu


@register(TextPage)
class TextPageTranslations(TranslationOptions):
    fields = ('title', 'slug', 'short_description', 'meta_title', 'meta_description', 'meta_key_words',)


@register(FooterMenu)
class FooterMenuTranslations(TranslationOptions):
    fields = ('title',)
