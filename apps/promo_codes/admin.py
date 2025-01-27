from django.contrib import admin
from apps.promo_codes.models import PromoCode, PromoCodeGenerator
from rangefilter.filters import DateRangeFilter


@admin.register(PromoCodeGenerator)
class PromoCodeGeneratorAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('discount_type',)
    list_filter = ('discount_type', ('valid_from_date', DateRangeFilter), ('valid_to_date', DateRangeFilter),)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ['status', 'discount_type', ('valid_from_date', DateRangeFilter),
                   ('valid_to_date', DateRangeFilter), ]
    readonly_fields = ['generator', 'discount_type', 'discount_value', 'valid_from_date', 'valid_to_date', ]
    search_fields = ('title',)

    def has_add_permission(self, request):
        return False  # return request.user.is_superuser
