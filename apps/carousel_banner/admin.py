from django.contrib import admin

from .models import CarouselBanner, CarouselImage
from modeltranslation.admin import TranslationStackedInline, TabbedTranslationAdmin


class CarouselImageInline(TranslationStackedInline):
    model = CarouselImage
    extra = 0


@admin.register(CarouselBanner)
class CarouselBannerAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active',)
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title',)
    inlines = (CarouselImageInline,)
