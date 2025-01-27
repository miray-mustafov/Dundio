from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.contacts.models import Object, Feedback, Contact
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Contact)
class ContactAdmin(TabbedTranslationAdmin):
    group_fieldsets = True
    list_display = ('title', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    search_fields = ('title', 'phone_number',)


@admin.register(Object)
class ObjectsAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title', 'phone_number', 'email',)

    fieldsets = (
        (None, {
            'fields': ('title', 'email', 'address', 'phone_number', 'work_time', 'is_active',)
        }),
        (_('Coordinates'), {
            'fields': ('lat', 'lng',)
        }),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('names', 'message_theme',)
    search_fields = ('names', 'message_theme', 'phone_number',)

    def has_change_permission(self, request, obj=None):
        return False
