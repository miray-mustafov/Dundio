from django.db import models
from django.utils.translation import gettext_lazy as _


class ClubCardTypes(models.TextChoices):
    accumulating_points = 'accumulating_points', _('натрупване на точки')
    vip = 'vip', _('вип')
