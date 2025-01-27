from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from apps.common.admin import ImageInline, FileInline
from apps.products.forms import CategoryForm, ProducerForm, ProductForm
from apps.products.models import Category, Producer, Product, MeasureUnit
from django.utils.translation import gettext_lazy as _
from admin_auto_filters.filters import AutocompleteFilter
from admin_numeric_filter.admin import NumericFilterModelAdmin
from apps.common.admin import CustomSliderNumericFilter
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, TabbedTranslationAdmin):
    form = CategoryForm

    list_display = ('tree_actions', 'indented_title', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('indented_title',)
    search_fields = ('title',)
    search_help_text = _('search by category title')
    prepopulated_fields = {"slug": ["title"]}
    draggable_fields = ('title',)


@admin.register(Producer)
class ProducerAdmin(TabbedTranslationAdmin):
    form = ProducerForm

    search_fields = ('title',)
    list_display = ('title', 'is_active',)
    list_editable = ('is_active',)


@admin.register(MeasureUnit)
class MeasureUnitAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title',)


class CategoryFilter(AutocompleteFilter):
    title = _('категория')
    field_name = 'category'


class ProducerFilter(AutocompleteFilter):
    title = _('производител')
    field_name = 'producer'


class MeasureUnitFilter(AutocompleteFilter):
    title = _('мерна единица')
    field_name = 'measure_unit'


@admin.register(Product)
class ProductAdmin(NumericFilterModelAdmin, TabbedTranslationAdmin):
    form = ProductForm
    inlines = (ImageInline, FileInline)

    list_display = ('get_image', 'title', 'is_active')
    list_filter = ('is_active', 'is_new',
                   CategoryFilter, ProducerFilter, MeasureUnitFilter,
                   ('price', CustomSliderNumericFilter),)
    list_editable = ('is_active',)
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ('title', 'nomenclature_number',)

    # for more convenient display in admin gui for many to many fields lazy loading
    autocomplete_fields = ('related_products', 'freq_bought_together',)
