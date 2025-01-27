from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product


class AccentBase(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('заглавие'), default='')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class AccentPromotion(AccentBase):
    class Meta:
        verbose_name = _('Промоционален Акцент')
        verbose_name_plural = _('Промоционални Акценти')


class AccentNew(AccentBase):
    class Meta:
        verbose_name = _('Нов Акцент')
        verbose_name_plural = _('Нови Акценти')


class AccentNewProduct(models.Model):
    accent_new = models.ForeignKey(AccentNew, verbose_name=_('акцент нови'), on_delete=models.CASCADE,
                                   related_name='accent_new_products')
    product = models.ForeignKey(Product, verbose_name=_('продукт'), on_delete=models.CASCADE,
                                related_name='accent_new_products')

    class Meta:
        verbose_name = _('Акцент нов продукт')
        verbose_name_plural = _('Акцент нови продукти')

    def __str__(self):
        return str(self.id)

        # todo repeating code

    def get_product_title(self):
        return self.product.title

    def get_product_main_image(self):
        return self.product.main_image

    def get_product_short_description(self):
        return self.product.short_description

    def get_product_producer(self):
        return self.product.producer

    def get_product_price(self):
        return self.product.price

    def get_product_promotional_price(self):
        return self.product.promotional_price

    def get_product_is_active(self):
        return self.product.is_active


class AccentPromotionProduct(models.Model):
    accent_promotion = models.ForeignKey(AccentPromotion, verbose_name=_('акцент промоции'), on_delete=models.CASCADE,
                                         related_name='accent_promotion_products')
    product = models.ForeignKey(Product, verbose_name=_('продукт'), on_delete=models.CASCADE,
                                related_name='accent_promotion_products')

    class Meta:
        verbose_name = _('Акцент промоционален продукт')
        verbose_name_plural = _('Акцент промоционалени продукти')

    def __str__(self):
        return str(self.id)

    def get_product_title(self):
        return self.product.title

    def get_product_main_image(self):
        return self.product.main_image

    def get_product_short_description(self):
        return self.product.short_description

    def get_product_producer(self):
        return self.product.producer

    def get_product_price(self):
        return self.product.price

    def get_product_promotional_price(self):
        return self.product.promotional_price

    def get_product_is_active(self):
        return self.product.is_active
