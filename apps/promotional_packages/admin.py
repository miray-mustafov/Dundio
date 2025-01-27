from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.promotional_packages.forms import PromotionalPackageForm
from apps.products.admin import CategoryFilter, MeasureUnitFilter, CustomSliderNumericFilter
from apps.promotional_packages.models import PromotionalPackage
from apps.common.admin import FileInline
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(PromotionalPackage)
class PromotionalPackageAdmin(TabbedTranslationAdmin):
    form = PromotionalPackageForm
    inlines = (FileInline,)

    list_display = ('title', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'is_new',
                   CategoryFilter, MeasureUnitFilter,
                   ('price', CustomSliderNumericFilter),)
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ('title',)

    # for more convenient display in admin gui for many to many fields
    autocomplete_fields = ('related_packages', 'products',)

    readonly_fields = ('price', 'weight_in_kg')
    fieldsets = (

        (_('Main'), {
            'fields': ('title', 'slug', 'main_image', 'youtube_link', 'you_save',)
        }),

        (_('Readonly'), {
            'fields': ('price', 'weight_in_kg',)
        }),

        (_('Relations'), {
            'fields': ('category', 'products', 'measure_unit', 'related_packages',)
        }),
        (_('Dates'), {
            'fields': ('valid_from_date', 'valid_to_date',)
        }),
        (_('Status'), {
            'fields': ('is_new', 'is_active',)
        }),
        (_('Meta'), {
            'fields': ('meta_title', 'meta_description', 'meta_key_words',)
        }),
    )

    @staticmethod
    def weight_in_kg(obj):
        return f"{obj.weight_in_kilograms} kg"
