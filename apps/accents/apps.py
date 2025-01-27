from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accents'
    verbose_name = _('Акценти')
