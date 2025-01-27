from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import CommonMeta, BaseModel
from apps.text_pages.choices import FooterMenuColumns


class TextPage(BaseModel, CommonMeta):
    title = models.CharField(max_length=255, verbose_name=_('заглавие'), default='')
    slug = models.SlugField(verbose_name=_('слъг'), max_length=255, editable=True, default='')
    short_description = models.CharField(max_length=160, verbose_name=_('кратко описание'), default='', blank=True)
    description = RichTextField(default='', blank=True)
    main_image = models.ImageField(verbose_name=_('основна снимка'), upload_to='text_page_images/',
                                   validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    youtube_link = models.URLField(verbose_name=_('ютюб линк'), default='', blank=True)
    is_active = models.BooleanField(verbose_name=_('активност'), default=False)

    class Meta:
        verbose_name = _('Текстова страница')
        verbose_name_plural = _('Текстови страници')

    def __str__(self):
        return self.title


class FooterMenu(models.Model):
    column = models.CharField(
        verbose_name=_('колона за подменюто'), max_length=255, choices=FooterMenuColumns.choices, default=FooterMenuColumns.information)
    title = models.CharField(max_length=255, verbose_name=_('заглавие'), default='')
    link = models.CharField(verbose_name=_('линк'), max_length=255, default='', blank=True,
                            help_text='Start with https:// or /')

    class Meta:
        verbose_name = _('Подменю')
        verbose_name_plural = _('Подменюта')

    def __str__(self):
        return self.title

    @classmethod
    def get_footer_elements_dict(cls):
        footer_elements = FooterMenu.objects.all()
        footer_elements_dict = {
            FooterMenuColumns.information.label: [],
            FooterMenuColumns.customer_service.label: [],
            FooterMenuColumns.additional_information.label: [],
            FooterMenuColumns.my_profile.label: [],
        }
        for fe in footer_elements:
            footer_elements_dict[FooterMenuColumns(fe.column).label].append(fe)
        return footer_elements_dict
