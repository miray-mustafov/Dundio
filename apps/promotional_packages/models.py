from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Sum

from apps.common.models import CommonMeta, BaseModel
from apps.products.models import Category, MeasureUnit, Product
from django.utils.translation import gettext_lazy as _


class PromotionalPackage(CommonMeta, BaseModel):
    """
    Advisable to be in products app because packages depend on products
    """

    category = models.ForeignKey(Category, verbose_name=_('категория'), on_delete=models.CASCADE,
                                 related_name='promotional_packages')
    measure_unit = models.ForeignKey(MeasureUnit, verbose_name=_('мерна единица'), on_delete=models.CASCADE,
                                     related_name='promotional_packages')

    related_packages = models.ManyToManyField('self', verbose_name=_('свързани пакети'), blank=True)

    products = models.ManyToManyField(Product, verbose_name=_('продукти'), blank=True,
                                      related_name='promotional_packages')

    title = models.CharField(verbose_name=_('заглавие'), max_length=255, default='')
    slug = models.SlugField(verbose_name=_('слъг'), max_length=255, editable=True, default='')
    main_image = models.ImageField(verbose_name=_('основна снимка'), upload_to='promotional_package_images/',
                                   validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    you_save = models.DecimalField(verbose_name=_('вие спестявате'), decimal_places=2, max_digits=6)
    youtube_link = models.URLField(verbose_name=_('ютюб линк'), default='', blank=True)

    valid_from_date = models.DateField(verbose_name=_('валиден от'))
    valid_to_date = models.DateField(verbose_name=_('валиден до'), null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_('активност'), default=False)
    is_new = models.BooleanField(verbose_name=_('нов'), default=False)

    price = models.DecimalField(verbose_name=_('цена'), decimal_places=2, max_digits=8, default=0.00)

    @property
    def weight_in_kilograms(self):
        total = self.products.aggregate(total=Sum('weight_in_kilograms'))['total']
        return total or 0

    class Meta:
        verbose_name = _('Промоционален пакет')
        verbose_name_plural = _('Промоционални пакети')

    def __str__(self):
        return self.title
