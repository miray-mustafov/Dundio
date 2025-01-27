from modeltranslation.translator import register, TranslationOptions
from .models import PhysicalUser, CompanyUser, BaseUser


@register(BaseUser)
class UserBaseTranslations(TranslationOptions):
    fields = ('full_name', 'address', 'region', 'populated_place', 'delivery_address',)


@register(PhysicalUser)
class PhysicalUserTranslations(TranslationOptions):
    pass


@register(CompanyUser)
class CompanyUserTranslations(TranslationOptions):
    fields = ('contact_person',)
