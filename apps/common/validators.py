import re
from django.core import exceptions
from django.utils.translation import gettext_lazy as _


def validate_phone(val):
    pattern = r'^0(2\d{7}|[3-9]\d{8})$'
    if not re.match(pattern, val):
        raise exceptions.ValidationError(_('Невалиден номер. Пример: 087xxxxxxx или 02xxxxxxx'))


def validate_postal_code(val):
    pattern = r'^\d{4}$'
    if not re.match(pattern, val):
        raise exceptions.ValidationError(_('Невалиден пощенски код. Пример 1712'))
