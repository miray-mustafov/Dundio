from apps.common.forms import BaseForm
from django.utils.translation import gettext_lazy as _

from apps.promotional_packages.models import PromotionalPackage


class PromotionalPackageForm(BaseForm):
    class Meta:
        model = PromotionalPackage
        fields = (
            'title',
            'slug',
            'category',
            'measure_unit',

            'valid_from_date',
            'valid_to_date',
            'you_save',

            'related_packages',
            'products',
            'main_image',

            'youtube_link',
            'is_active',
            'is_new',
            'meta_title',
            'meta_description',
            'meta_key_words',
        )

    def clean(self):
        super(PromotionalPackageForm, self).clean()

        if self.instance:  # edit mode
            if self.instance in self.cleaned_data.get('related_packages'):
                self.add_error('related_packages', _('You cannot relate a package to itself'))

        # check if user accidentally inserted: you_save >= price
        products_price = sum(p.price for p in self.cleaned_data.get('products'))
        if self.cleaned_data.get('you_save') and self.cleaned_data.get('you_save') >= products_price:
            self.add_error('you_save', _('Value must be less than the total price of the package'))
        # price formation handling at form level:
        # self.cleaned_data['price'] = products_price - self.cleaned_data.get('you_save')

        return self.cleaned_data
