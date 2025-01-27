from modeltranslation.translator import register, TranslationOptions
from .models import CarouselBanner, CarouselImage


@register(CarouselBanner)
class CarouselBannerTranslations(TranslationOptions):
    fields = ('title',)


@register(CarouselImage)
class CarouselImageTranslations(TranslationOptions):
    fields = ('title', 'short_description',)
