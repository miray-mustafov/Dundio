from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Prefetch
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from apps.common.models import CommonMeta, BaseModel


class Category(MPTTModel):
    ICON_CHOICES = (
        ('category_icon_1', _('Бебешки колички')),
        ('category_icon_2', _('Всичко за детето')),
        ('category_icon_3', _('Безопастност')),
        ('category_icon_4', _('Хигиена')),
        ('category_icon_5', _('Спорт')),
        ('category_icon_6', _('Уреди')),
        ('category_icon_7', _('За кола')),
        ('category_icon_8', _('За баня')),
        ('category_icon_9', _('Играчки')),
        ('category_icon_10', _('Хранене')),
        ('category_icon_11', _('Всичко за майката')),
        ('category_icon_12', _('Обзавеждане за стая')),
        ('category_icon_13', _('Облекло и аксесоари'))
    )
    parent = TreeForeignKey('self', verbose_name=_('под категория на'), on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')
    title = models.CharField(verbose_name=_('заглавие'), max_length=255)
    slug = models.SlugField(verbose_name=_('слъг'), max_length=255, editable=True)
    icon = models.CharField(verbose_name=_('икона'), max_length=100, choices=ICON_CHOICES)
    is_active = models.BooleanField(verbose_name=_('активност'), default=False)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.title

    @classmethod
    def get_active_categories_with_prefetch(cls):
        """Gets active lvl_1 categories and prefetches the active children categories"""
        categories = cls.objects.filter(is_active=True, parent=None).prefetch_related(
            Prefetch('children', queryset=Category.objects.filter(is_active=True).prefetch_related('children'))
        )
        return categories


class Producer(models.Model):
    title = models.CharField(verbose_name=_('заглавие'), max_length=255, default='')
    is_active = models.BooleanField(verbose_name=_('активност'), default=False)

    class Meta:
        verbose_name = _('Производител')
        verbose_name_plural = _('Производители')

    def __str__(self):
        return self.title


class MeasureUnit(models.Model):
    title = models.CharField(verbose_name=_('заглавие'), max_length=255, default='')
    is_active = models.BooleanField(verbose_name=_('активност'), default=False)

    class Meta:
        verbose_name = _('Мерна единица')
        verbose_name_plural = _('Мерни единици')

    def __str__(self):
        return self.title


class Product(BaseModel, CommonMeta):
    category = models.ForeignKey(Category, verbose_name=_('категория'), on_delete=models.CASCADE,
                                 related_name='products', limit_choices_to={'is_active': True})
    producer = models.ForeignKey(Producer, verbose_name=_('производител'), on_delete=models.CASCADE,
                                 related_name='products', limit_choices_to={'is_active': True})
    measure_unit = models.ForeignKey(MeasureUnit, verbose_name=_('мерна единица'), on_delete=models.CASCADE,
                                     related_name='products', limit_choices_to={'is_active': True})

    related_products = models.ManyToManyField('self', verbose_name=_('свързани продукти'), blank=True,
                                              limit_choices_to={'is_active': True}, )
    freq_bought_together = models.ManyToManyField('self', verbose_name=_('често купувани заедно'), blank=True,
                                                  limit_choices_to={'is_active': True}, )

    title = models.CharField(verbose_name=_('заглавие'), max_length=255, default='')
    slug = models.SlugField(verbose_name=_('слъг'), max_length=255, editable=True, default='')
    short_description = models.CharField(max_length=160, verbose_name=_('кратко описание'), default='', blank=True)
    description = RichTextField(default='', blank=True)
    main_image = models.ImageField(verbose_name=_('основна снимка'), upload_to='product_images/',
                                   validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    youtube_link = models.URLField(verbose_name=_('ютюб линк'), default='', blank=True)
    nomenclature_number = models.CharField(verbose_name=_('вътрешен номер'), default='', max_length=100)
    price = models.DecimalField(verbose_name=_('цена'), max_digits=6, decimal_places=2, default=0.0)
    promotional_price = models.DecimalField(verbose_name=_('промоционална цена'), max_digits=6, decimal_places=2,
                                            null=True, blank=True)
    available_quantity = models.DecimalField(verbose_name=_('налично количество'), max_digits=10, decimal_places=3,
                                             default=0.0)
    weight_in_kilograms = models.DecimalField(verbose_name=_('тегло в килограми'), max_digits=10, decimal_places=3,
                                              default=0.0)

    is_active = models.BooleanField(verbose_name=_('активност'), default=False)
    is_new = models.BooleanField(verbose_name=_('нов'), default=False)

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукти')

    def __str__(self):
        return self.title

    def get_image(self):
        return mark_safe(f'<img src="{self.main_image.url}" height="60"/>')
