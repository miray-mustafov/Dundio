from modeltranslation.translator import register, TranslationOptions
from .models import Contact, Object, Feedback


@register(Contact)
class ContactTranslations(TranslationOptions):
    fields = ('title', 'department',)


@register(Object)
class ObjectTranslations(TranslationOptions):
    fields = ('title',)
