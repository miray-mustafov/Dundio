from django.db import models
from .choices import DiscountTypes, PromoCodeStatuses
from django.utils.translation import gettext_lazy as _


class PromoCodeGenerator(models.Model):
    count = models.PositiveIntegerField(verbose_name=_('брой'), default=0)
    discount_type = models.CharField(
        verbose_name=_('вид отстъпка'), max_length=255, choices=DiscountTypes.choices, default=DiscountTypes.percentage)
    discount_value = models.PositiveIntegerField(verbose_name=_('стойност на отстъпката'), default=0)
    valid_from_date = models.DateTimeField(verbose_name=_('валидна от'), null=True, blank=True)
    valid_to_date = models.DateTimeField(verbose_name=_('валидна до'), null=True, blank=True)

    class Meta:
        verbose_name = _('Генератор на код')
        verbose_name_plural = _('Генератори на код')

    def __str__(self):
        return f'{self.discount_type}({self.discount_value})-{self.count}'


class PromoCode(models.Model):
    title = models.CharField(verbose_name=_('заглавие'), max_length=255, default='', unique=True)
    generator = models.ForeignKey(PromoCodeGenerator, verbose_name=_('генератор на код'),
                                  on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    discount_type = models.CharField(verbose_name=_('вид отстъпка'), max_length=255, choices=DiscountTypes.choices)
    discount_value = models.PositiveIntegerField(verbose_name=_('стойност на отстъпката'), default=0)
    valid_from_date = models.DateTimeField(verbose_name=_('валидна от'), null=True, blank=True)
    valid_to_date = models.DateTimeField(verbose_name=_('валидна до'), null=True, blank=True)

    status = models.CharField(verbose_name=_('статус'), max_length=255, choices=PromoCodeStatuses.choices,
                              default=PromoCodeStatuses.generated)

    class Meta:
        verbose_name = _('Код')
        verbose_name_plural = _('Кодове')

    def __str__(self):
        return self.title
