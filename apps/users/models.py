from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.validators import validate_phone, validate_postal_code


class BaseUser(models.Model):
    username = models.CharField(verbose_name=_('потребителско име'), max_length=255, default='')
    email = models.EmailField(verbose_name=_('имейл'), default='')
    password = models.CharField(verbose_name=_('парола'), max_length=255, default='')

    full_name = models.CharField(verbose_name=_('имена'), max_length=255, default='', blank=True)
    phone_number = models.CharField(verbose_name=_('телефонен номер'), max_length=10, default='',
                                    blank=True, validators=[validate_phone])
    address = models.CharField(verbose_name=_('адрес'), max_length=255, default='', blank=True)
    region = models.CharField(verbose_name=_('област'), max_length=255, default='', blank=True)
    populated_place = models.CharField(verbose_name=_('населено място'), max_length=255, default='', blank=True)
    postal_code = models.CharField(verbose_name=_('пощенски код'), max_length=4, default='', blank=True,
                                   validators=[validate_postal_code])
    delivery_address = models.CharField(verbose_name=_('адрес'), max_length=255, default='', blank=True)
    date_registered = models.DateField(verbose_name=_('дата на регистрация'), auto_now_add=True)
    dundio_club_card = models.CharField(verbose_name=_('дундио клуб карта'), max_length=255, default='',
                                        blank=True)

    is_active = models.BooleanField(verbose_name=_('активност'), default=False)
    is_confirmed = models.BooleanField(verbose_name=_('потвърденост'), default=False)

    def __str__(self):
        return self.username

    def is_company(self):
        return isinstance(self, CompanyUser)

    def is_physical_user(self):
        return isinstance(self, PhysicalUser)


class PhysicalUser(BaseUser):
    class Meta:
        verbose_name = _('Физическо лице')
        verbose_name_plural = _('Физически лица')


class CompanyUser(BaseUser):
    dds = models.CharField(verbose_name=_('ддс'), max_length=255, default='', blank=True)
    mol = models.CharField(verbose_name=_('мол'), max_length=255, default='', blank=True)
    eik = models.CharField(verbose_name=_('еик'), max_length=255, default='', blank=True)
    contact_person = models.CharField(verbose_name=_('лице за контакт'), max_length=255, default='', blank=True)

    class Meta:
        verbose_name = _('Юридическо лице')
        verbose_name_plural = _('Юридически лица')


class UserConfirmationToken(models.Model):
    user = models.ForeignKey(BaseUser, verbose_name=_('потребител'), on_delete=models.CASCADE,
                             limit_choices_to={'is_active': True})
    token = models.CharField(max_length=255, verbose_name=_('токен'))
    date_created = models.DateTimeField(verbose_name=_('дата на създаване'), default=timezone.now)
    is_used = models.BooleanField(verbose_name=_('използван'), default=False)

    class Meta:
        verbose_name = _('Потвърждаващ токен')
        verbose_name_plural = _('Потвърждаващи токени')
