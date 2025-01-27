from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.cards.choices import ClubCardTypes
from decimal import Decimal

POINTS_PERCENTAGE = Decimal('0.07')


class ClubCard(models.Model):
    number = models.CharField(verbose_name=_('номер на карта'), max_length=255, default='', unique=True, )
    type = models.CharField(verbose_name=_('тип на карта'), max_length=255, choices=ClubCardTypes.choices,
                            default=ClubCardTypes.accumulating_points)
    # max_digits=1-9 => 5 bytes (9 turns out to be the optimal choice)
    points = models.DecimalField(verbose_name=_('точки за карта натрупване на точки'), max_digits=9, decimal_places=2,
                                 null=True, blank=True)
    fixed_discount = models.DecimalField(verbose_name=_('фиксирана отстъпка за Вип карта'), max_digits=9,
                                         decimal_places=2, null=True, blank=True)

    is_active = models.BooleanField(verbose_name=_('активност'), default=False)

    class Meta:
        verbose_name = _('Карта Dundio Club')
        verbose_name_plural = _('Карти Dundio Club')

    def __str__(self):
        hidden_chars_count = len(self.number) // 3
        return hidden_chars_count * '*' + self.number[hidden_chars_count:]
