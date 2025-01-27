from django.db import models
from django.utils.translation import gettext_lazy as _


class DiscountTypes(models.TextChoices):
    percentage = 'percentage', _('процент')
    fixed = 'fixed', _('фиксирана')


class PromoCodeStatuses(models.TextChoices):
    generated = 'generated', _('генериран')
    used = 'used', _('използван')
