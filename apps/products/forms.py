from apps.products.models import Category, Producer, Product
from django.utils.translation import gettext_lazy as _

from apps.common.forms import BaseForm


class CategoryForm(BaseForm):
    class Meta:
        model = Category
        fields = ('parent', 'title', 'slug', 'icon', 'is_active',)

    def clean(self):  # for validations
        # data from the form is fetched using super function
        super(CategoryForm, self).clean()

        # restricting the nesting up to 3 levels (allowed levels 0, 1, 2)
        parent = self.cleaned_data.get('parent')
        if parent and parent.level >= 2:
            self.add_error('parent', _('You cannot create a category more than 3 levels deep'))

        return self.cleaned_data


class ProducerForm(BaseForm):
    class Meta:
        model = Producer
        fields = ('title', 'is_active',)


class ProductForm(BaseForm):
    MAX_REL = 3

    class Meta:
        model = Product
        fields = (
            'title',
            'slug',
            'category',
            'producer',
            'measure_unit',
            'related_products',
            'freq_bought_together',
            'short_description',
            'description',
            'main_image',
            'youtube_link',
            'nomenclature_number',
            'price',
            'promotional_price',
            'available_quantity',
            'weight_in_kilograms',
            'is_active',
            'is_new',
            'meta_title',
            'meta_description',
            'meta_key_words',
        )

    def clean(self):
        super(ProductForm, self).clean()

        related_products = self.cleaned_data.get('related_products')
        freq_bought_together = self.cleaned_data.get('freq_bought_together')
        if self.instance:  # edit mode
            if self.instance in related_products:
                self.add_error('related_products', _('You cannot relate a product to itself'))
            if self.instance in freq_bought_together:
                self.add_error('freq_bought_together', _('You cannot relate a product to itself'))

        if len(freq_bought_together) > self.MAX_REL:  # the way
            self.add_error('freq_bought_together', _(f'Не можеш да свършеш повече от {self.MAX_REL} продукта'))
        else:
            for f in freq_bought_together:
                f_related = f.freq_bought_together.all()
                if len(f_related) >= self.MAX_REL and (not self.instance or self.instance not in f_related):
                    self.add_error('freq_bought_together',
                                   _(f'Подадените свързани продукти са на път да превишат максимума от {self.MAX_REL} продукта'))

        # restricting negative number values
        non_negative_expected_msg = _('Non-negative value expected')
        fields_to_check = {
            'price': non_negative_expected_msg,
            'promotional_price': non_negative_expected_msg,
            'available_quantity': non_negative_expected_msg,
            'weight_in_kilograms': non_negative_expected_msg,
        }
        for field_name, error_msg in fields_to_check.items():
            if self.cleaned_data.get(field_name) and self.cleaned_data.get(field_name) <= 0:
                self.add_error(field_name, error_msg)

        return self.cleaned_data
