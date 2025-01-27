from django.db import models
from django.utils.translation import gettext_lazy as _


class FooterMenuColumns(models.TextChoices):
    information = 'information', _('Информация')
    customer_service = 'customer_service', _('Обслужване на клиенти')
    additional_information = 'additional_information', _('Допълнителна информация')
    my_profile = 'my_profile', _('Моят профил')
