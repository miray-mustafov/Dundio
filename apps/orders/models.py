from django.core.validators import MinValueValidator
from django.db import models
from apps.common.validators import validate_phone
from apps.products.models import Product
from apps.promotional_packages.models import PromotionalPackage
from apps.users.models import BaseUser
from django.utils.translation import gettext_lazy as _
from apps.orders import choices


class Order(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True, blank=True,
                             limit_choices_to={'is_active': True})

    name = models.CharField(verbose_name=_('имена'), max_length=255, default='')
    email = models.EmailField(verbose_name=_('имейл'), default='')
    populated_place = models.CharField(verbose_name=_('населено място'), max_length=255, default='', blank=True)
    delivery_address = models.CharField(verbose_name=_('адрес за доставка'), max_length=255, default='', blank=True)
    phone_number = models.CharField(verbose_name=_('телефонен номер'), max_length=10, default='',
                                    blank=True, validators=[validate_phone])
    price_with_vat = models.DecimalField(verbose_name=_('цена с ддс'), max_digits=8, decimal_places=2, default=0.00,
                                         validators=[MinValueValidator(0.00)])
    price_delivery = models.DecimalField(verbose_name=_('цена за доставка'), max_digits=8, decimal_places=2,
                                         default=0.00, validators=[MinValueValidator(0.00)])
    code = models.CharField(verbose_name=_('код'), max_length=255, default='', blank=True)
    discount = models.DecimalField(verbose_name=_('отстъпка'), max_digits=8, decimal_places=2, default=0.00,
                                   validators=[MinValueValidator(0.00)])

    date_created = models.DateTimeField(verbose_name=_('дата на създаване'), auto_now_add=True)

    delivery_method = models.CharField(verbose_name=_('начин на доставка'), max_length=255,
                                       choices=choices.DeliveryMethods.choices)
    pay_method = models.CharField(verbose_name=_('начин на плащането'), max_length=255,
                                  choices=choices.PayMethods.choices)
    pay_status = models.CharField(verbose_name=_('статус на плащането'), max_length=255,
                                  choices=choices.PayStatuses.choices)
    order_status = models.CharField(verbose_name=_('статус на поръчката'), max_length=255,
                                    choices=choices.OrderStatuses.choices)

    is_invoice_wanted = models.BooleanField(verbose_name=_('желая фактура'), default=False)

    @property
    def total_price(self):
        res = self.price_with_vat + self.price_delivery  # - self.discount
        return res if res > 0 else 0

    class Meta:
        verbose_name = _('Поръчка')
        verbose_name_plural = _('Поръчки')

    def __str__(self):
        return f'Order for {self.name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('поръчка'), on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name=_('продукт'), on_delete=models.CASCADE, related_name='order_item')
    quantity = models.DecimalField(verbose_name=_('количество'), max_digits=10, decimal_places=3,
                                   default=0.0)

    def get_title(self):
        return self.product.title

    def get_category(self):
        return self.product.category

    def get_producer(self):
        return self.product.producer

    def get_nomenclature_number(self):
        return self.product.nomenclature_number

    def get_price(self):
        return self.product.price

    def get_promotional_price(self):
        return self.product.promotional_price

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукти')

    def __str__(self):
        return f'{self.get_title()}'


class OrderPromotionalPackage(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('поръчка'), on_delete=models.CASCADE,
                              related_name='order_promotional_packages')
    promotional_package = models.ForeignKey(PromotionalPackage, verbose_name=_('промоционален пакет'),
                                            on_delete=models.CASCADE,
                                            related_name='order_promotional_package')
    quantity = models.DecimalField(verbose_name=_('количество'), max_digits=10, decimal_places=3,
                                   default=0.0)

    def get_title(self):
        return self.promotional_package.title

    def get_category(self):
        return self.promotional_package.category

    def get_price(self):
        return self.promotional_package.price

    class Meta:
        verbose_name = _('Промоционален пакет')
        verbose_name_plural = _('Промоционални пакети')

    def __str__(self):
        return f'{self.get_title()}'
