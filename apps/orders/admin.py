from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.orders.models import Order, OrderPromotionalPackage, OrderItem
from apps.common.admin import CustomSliderNumericFilter
from modeltranslation.admin import TabbedTranslationAdmin


class OrderPromotionalPackageInline(admin.StackedInline):
    model = OrderPromotionalPackage
    extra = 0
    autocomplete_fields = ['promotional_package']


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ['product']


@admin.register(Order)
class OrderAdmin(TabbedTranslationAdmin):
    list_display = ('name',)
    readonly_fields = ('total_price', 'date_created',)
    list_filter = (
        'delivery_method', 'pay_method', 'pay_status', 'order_status', 'is_invoice_wanted',
        ('price_with_vat', CustomSliderNumericFilter),
    )
    search_fields = ('name',)
    inlines = [OrderPromotionalPackageInline, OrderItemInline]
    fieldsets = (
        (_('User Info'), {
            'fields': ('user', 'name', 'email', 'populated_place', 'delivery_address', 'phone_number',)
        }),
        (_('Prices'), {
            'fields': ('price_with_vat', 'price_delivery', 'code', 'discount',)
        }),
        (_('Choices'), {
            'fields': ('delivery_method', 'pay_method', 'pay_status', 'order_status', 'is_invoice_wanted',)
        }),
        (_('Readonly'), {
            'fields': ('total_price', 'date_created',)
        }),

    )

    @staticmethod
    def total_price(obj):
        return obj.total_price
