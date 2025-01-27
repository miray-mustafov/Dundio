from modeltranslation.translator import register, TranslationOptions
from .models import AccentPromotion, AccentNew


@register(AccentNew)
class AccentNewTranslations(TranslationOptions):
    fields = ('title',)


@register(AccentPromotion)
class AccentPromotionTranslations(TranslationOptions):
    fields = ('title',)
