from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CommonMeta(models.Model):
    meta_title = models.TextField(verbose_name=_('мета заглавие'), default='', blank=True)
    meta_description = models.TextField(verbose_name=_('мета описание'), default='', blank=True)
    meta_key_words = models.TextField(verbose_name=_('мета ключови думи'), default='', blank=True)

    def get_meta_title(self):
        if not self.meta_title and hasattr(self, 'title'):
            return getattr(self, 'title')
        return self.meta_title

    def get_meta_description(self):
        if not self.meta_description and hasattr(self, 'short_description'):
            return getattr(self, 'short_description')
        return self.meta_description

    def get_meta_keywords(self):
        if not self.meta_key_words and hasattr(self, 'title'):
            return getattr(self, 'title')
        return self.meta_key_words

    class Meta:
        abstract = True


class BaseModel(models.Model):
    pass


class Image(models.Model):
    base_model = models.ForeignKey(BaseModel, verbose_name=_('базов модел'), on_delete=models.CASCADE,
                                   related_name='images')
    image = models.ImageField(verbose_name=_('снимка'), upload_to='images/', validators=[
        FileExtensionValidator(['png', 'jpg', 'jpeg'])
    ])

    class Meta:
        verbose_name = _('Снимка')
        verbose_name_plural = _('Снимки')


class File(models.Model):
    base_model = models.ForeignKey(BaseModel, verbose_name=_('базов модел'), on_delete=models.CASCADE,
                                   related_name='files')
    file = models.FileField(verbose_name=_('файл'), upload_to='files/',
                            validators=[FileExtensionValidator(['doc', 'docx', 'xls', 'xlsx', 'pdf', 'txt', 'pptx'])])

    class Meta:
        verbose_name = _('Файл')
        verbose_name_plural = _('Файлове')


class SubscribedNewsletterEmail(models.Model):
    email = models.EmailField(verbose_name=_('имейл'), default='')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Имейл за бюлетин')
        verbose_name_plural = _('Имейли за бюлетин')
