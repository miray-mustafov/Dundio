from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CarouselBanner(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('заглавие'), default='', blank=False)
    is_active = models.BooleanField(verbose_name=_('активност'), default=True)

    class Meta:
        verbose_name = _('Карусел банер')
        verbose_name_plural = _('Карусел банери')

    def __str__(self):
        return self.title


class CarouselImage(models.Model):
    carousel_banner = models.ForeignKey(CarouselBanner, on_delete=models.CASCADE, related_name='carousel_images')
    title = models.CharField(max_length=100, verbose_name=_('заглавие'), default='', blank=False)
    image = models.ImageField(verbose_name=_('снимка'), upload_to='carousel_images/',
                              validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    short_description = models.CharField(max_length=160, verbose_name=_('кратко описание'), default='', blank=True)
    link = models.URLField(verbose_name=_('линк'), default='', blank=True)

    class Meta:
        verbose_name = _('Карусел снимка')
        verbose_name_plural = _('Карусел снимки')

    def __str__(self):
        return f'{self.title}'
