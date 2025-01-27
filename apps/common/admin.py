from decimal import Decimal

from admin_numeric_filter.admin import SliderNumericFilter
from django.contrib import admin

from apps.common.models import File, Image


class FileInline(admin.StackedInline):
    model = File
    extra = 0


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class CustomSliderNumericFilter(SliderNumericFilter):
    MAX_DECIMALS = 2
    STEP = 1

    # todo fix visualization (possibly customization with js need)

    def queryset(self, request, queryset):
        filters = {}

        value_from = self.used_parameters.get(self.parameter_name + '_from', None)
        if value_from is not None and value_from != '':
            list_one_string_param = self.used_parameters.get(self.parameter_name + '_from', None)
            decimal_param_from = Decimal(list_one_string_param[0])
            filters.update({
                self.parameter_name + '__gte': decimal_param_from,
            })

        value_to = self.used_parameters.get(self.parameter_name + '_to', None)
        if value_to is not None and value_to != '':
            list_one_string_param = self.used_parameters.get(self.parameter_name + '_to', None)
            decimal_param_to = Decimal(list_one_string_param[0])
            filters.update({
                self.parameter_name + '__lte': decimal_param_to,
            })

        return queryset.filter(**filters)
