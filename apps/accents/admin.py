from django.contrib import admin
from apps.accents.models import AccentPromotion, AccentNew, AccentNewProduct, AccentPromotionProduct
from modeltranslation.admin import TabbedTranslationAdmin


class AccentPromotionProductInline(admin.StackedInline):
    model = AccentPromotionProduct
    extra = 0
    autocomplete_fields = ['product']


class AccentNewProductInline(admin.StackedInline):
    model = AccentNewProduct
    extra = 0
    autocomplete_fields = ['product']


@admin.register(AccentPromotion)
class AccentPromotionAdmin(TabbedTranslationAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = (AccentPromotionProductInline,)


@admin.register(AccentNew)
class AccentNewAdmin(TabbedTranslationAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = (AccentNewProductInline,)
