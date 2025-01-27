from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TextPagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.text_pages'
    verbose_name = _('Страници')
