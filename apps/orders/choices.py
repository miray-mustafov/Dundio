from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryMethods(models.TextChoices):
    to_office = 'to_office', _('до офис')
    to_address = 'to_address', _('до адрес')
    to_sofia_store = 'to_store_in_sofia', _('вземане от магазин в град София')


class PayMethods(models.TextChoices):
    cash_on_delivery = 'cash_on_delivery', _('наложен платеж')
    with_card_on_courier = 'with_card_on_courier', _('с карта на куриер')


class PayStatuses(models.TextChoices):
    expecting_cash_on_delivery_payment = 'expecting_cash_on_delivery_payment', _('очаква наложен платеж')
    paid_with_cash_on_delivery = 'paid_with_cash_on_delivery', _('платено с наложен платеж')
    expecting_bank_transfer = 'expecting_bank_transfer', _('очаква банков превод')
    paid_with_bank_transfer = 'paid_with_bank_transfer', _('платено с банков превод')
    paid_with_dundio_card = 'paid_with_dundio_card', _('платено с Dundio Club')


class OrderStatuses(models.TextChoices):
    new_order = 'new_order', _('нова поръчка')
    unfinished_order = 'unfinished_order', _('незавършена поръчка')
    processed_order = 'processed_order', _('обработена поръчка')
    canceled_order = 'canceled_order', _('анулирана поръчка')
