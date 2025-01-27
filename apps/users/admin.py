from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from rangefilter.filters import DateRangeFilter
from apps.users.models import PhysicalUser, CompanyUser


class BaseUserAdmin(TabbedTranslationAdmin):
    list_display = ('username', 'is_active', 'is_confirmed')
    list_editable = ('is_active', 'is_confirmed',)
    list_filter = ('is_active', 'is_confirmed', ('date_registered', DateRangeFilter),)
    search_fields = ('username', 'email', 'phone_number',)
    readonly_fields = ('date_registered',)

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'full_name', 'phone_number',)
        }),
        (_('Address'), {
            'fields': ('address', 'region', 'populated_place', 'postal_code', 'delivery_address',)
        }),
        (_('Cards'), {
            'fields': ('dundio_club_card',)
        }),
        (_('Statuses'), {
            'fields': ('is_active', 'is_confirmed',)
        }),
        (_('Readonly'), {
            'fields': ('date_registered',)
        }),
    )


@admin.register(PhysicalUser)
class PhysicalUserAdmin(BaseUserAdmin):
    pass


@admin.register(CompanyUser)
class CompanyUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Legal Entity'), {'fields': ('dds', 'mol', 'eik', 'contact_person',)},),
    )
