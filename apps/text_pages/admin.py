from django.contrib import admin

from apps.common.admin import ImageInline, FileInline
from apps.text_pages.forms import TextPageForm
from apps.text_pages.models import TextPage, FooterMenu
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(TextPage)
class TextPageAdmin(TabbedTranslationAdmin):
    form = TextPageForm

    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'is_active',)
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title',)
    inlines = (ImageInline, FileInline)


@admin.register(FooterMenu)
class FooterMenuAdmin(TabbedTranslationAdmin):
    list_display = ('title',)
    list_filter = ('column',)
    search_fields = ('title',)
