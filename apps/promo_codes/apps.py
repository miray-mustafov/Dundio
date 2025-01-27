from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PromoCodesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.promo_codes'
    verbose_name = _('Промоционални кодове')

    def ready(self):
        import apps.promo_codes.signals
