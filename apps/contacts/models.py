from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.validators import validate_phone


class ContactsBase(models.Model):
    title = models.CharField(verbose_name=_('заглавие'), max_length=255, default='')
    address = models.CharField(verbose_name=_('адрес'), max_length=255, default='', blank=True)
    phone_number = models.CharField(verbose_name=_('телефонен номер'), max_length=10, default='', blank=True,
                                    validators=(validate_phone,))
    work_time = models.CharField(verbose_name=_('работно време'), max_length=255, default='', blank=True)
    is_active = models.BooleanField(verbose_name=_('активност'), default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Contact(ContactsBase):
    department = models.CharField(verbose_name=_('отдел'), max_length=100, default='', blank=True)

    class Meta:
        verbose_name = _('Контакт')
        verbose_name_plural = _('Контакти')


class Object(ContactsBase):
    email = models.EmailField(verbose_name=_('имейл'), default='')
    lat = models.CharField(verbose_name=_('географска ширина'), max_length=255, default='', blank=True)
    lng = models.CharField(verbose_name=_('географска дължина'), max_length=255, default='', blank=True)

    class Meta:
        verbose_name = _('Обект')
        verbose_name_plural = _('Обекти')


class Feedback(models.Model):
    names = models.CharField(verbose_name=_('заглавие'), max_length=255, default='')
    email = models.EmailField(verbose_name=_('имейл'), default='')
    message_theme = models.CharField(verbose_name=_('тема на съобщението'), max_length=255, default='')
    phone_number = models.CharField(verbose_name=_('телефонен номер'), max_length=10, default='', blank=True,
                                    validators=(validate_phone,))
    message = models.TextField(verbose_name=_('съобщение'), default='', blank=True)

    class Meta:
        verbose_name = _('Обратна връзка')
        verbose_name_plural = _('Обратни връзки')

    def __str__(self):
        return self.message_theme
