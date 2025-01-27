from django import forms
from django.utils.translation import gettext_lazy as _
from apps.users.models import PhysicalUser, CompanyUser, BaseUser, UserConfirmationToken
from django.contrib.auth.hashers import make_password, check_password


def _validate_email_uniqueness(self, cleaned_data, exclude_id=None):
    email = cleaned_data.get('email')
    if BaseUser.objects.filter(email=email).exclude(id=exclude_id).exists():
        self.add_error('email', _('Този имейл е зает'))


def _validate_username_uniqueness(self, cleaned_data, exclude_id=None):
    username = cleaned_data.get('username')
    if BaseUser.objects.filter(username=username).exclude(id=exclude_id).exists():
        self.add_error('username', _('Това потребителско име е заето'))


class RegisterUserFormBase(forms.ModelForm):
    full_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    region = forms.CharField(required=True)
    populated_place = forms.CharField(required=True)
    postal_code = forms.CharField(required=True)
    delivery_address = forms.CharField(required=True)

    re_password = forms.CharField(required=True)
    is_personal_data = forms.BooleanField(required=True)

    class Meta:
        model = None
        fields = (
            'username',
            'email',
            'password',
            'full_name',
            'phone_number',
            'address',
            'region',
            'populated_place',
            'postal_code',
            'delivery_address',
            'dundio_club_card',
        )

    def clean(self):
        cleaned_data = super().clean()

        _validate_username_uniqueness(self, cleaned_data)
        _validate_email_uniqueness(self, cleaned_data)

        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')
        if password != re_password:
            self.add_error('re_password', _('Паролите не съвпадат'))
        cleaned_data['password'] = make_password(password)

        return cleaned_data


class RegisterPhysicalUserForm(RegisterUserFormBase):
    class Meta:
        model = PhysicalUser
        fields = RegisterUserFormBase.Meta.fields


class RegisterCompanyUserForm(RegisterUserFormBase):
    dds = forms.CharField(required=True)
    mol = forms.CharField(required=True)
    eik = forms.CharField(required=True)
    contact_person = forms.CharField(required=True)
    address = forms.CharField(required=True)

    delivery_address = forms.CharField(required=False)
    is_no_address_match = forms.BooleanField(required=False)

    class Meta:
        model = CompanyUser
        fields = RegisterUserFormBase.Meta.fields + (
            'dds',
            'mol',
            'eik',
            'contact_person',
        )

    def clean(self):
        cleaned_data = super().clean()

        is_no_address_match = cleaned_data.get('is_no_address_match', False)
        if is_no_address_match and not cleaned_data.get('delivery_address'):
            # delivery_address must be specified
            self.add_error(
                'delivery_address',
                _('Ако сте посочили, че адресите не съвпадат, то трябва да посочите Адрес за доставка'))

        return cleaned_data


class LoginUserForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = BaseUser.objects.filter(username=username, is_active=True, is_confirmed=True).first()

        if user and check_password(password, user.password):
            cleaned_data['custom_user_id'] = user.id
            return cleaned_data

        self.add_error(None, _('Грешни данни за вход или акаунта не е активиран'))
        return cleaned_data


class ForgottenPassForm(forms.Form):
    email = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        user = BaseUser.objects.filter(email=email, is_active=True, is_confirmed=True).first()
        if not user:
            self.add_error('email', _('Няма регистрация с този имейл'))

        self.cleaned_data['user'] = user
        return cleaned_data


class ChangePassForm(forms.Form):
    new_password = forms.CharField(required=True)
    re_password = forms.CharField(required=True)
    token = forms.CharField(required=True)
    email = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get('new_password')
        re_password = cleaned_data.get('re_password')
        if new_password != re_password:
            self.add_error(None, _('Паролите не съвпадат'))
            return cleaned_data

        token = cleaned_data.get('token')
        email = cleaned_data.get('email')
        confirmation_token = UserConfirmationToken.objects.filter(token=token, user__email=email, is_used=False).first()
        if not confirmation_token:
            self.add_error(None, _('Токенът може да е изтекал или вече да е използван'))
        cleaned_data['confirmation_token'] = confirmation_token

        return cleaned_data


class EditUserFormBase(forms.ModelForm):
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)

    class Meta:
        model = None
        fields = (
            'full_name',
            'email',
            'phone_number',
            'dundio_club_card',

            'delivery_address',
            'populated_place',
            'region',
            'postal_code',
        )

    def clean(self):
        cleaned_data = super().clean()
        _validate_email_uniqueness(self, cleaned_data, self.instance.pk)

        return cleaned_data


class EditPhysicalUserForm(EditUserFormBase):
    class Meta:
        model = PhysicalUser
        fields = RegisterUserFormBase.Meta.fields


class EditCompanyUserForm(EditUserFormBase):
    class Meta:
        model = CompanyUser
        fields = RegisterUserFormBase.Meta.fields + (
            'address',  # todo
            'dds',
            'mol',
            'eik',
            'contact_person',
        )


class EditPassForm(forms.Form):
    username = forms.CharField(required=True)
    old_password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
    re_password = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()

        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        re_password = cleaned_data.get('re_password')
        username = cleaned_data.get('username')

        user = BaseUser.objects.filter(username=username, is_active=True, is_confirmed=True).first()
        # if user:
        if not check_password(old_password, user.password):
            self.add_error('old_password', _('Грешна парола'))

        if new_password != re_password:
            self.add_error('re_password', _('Паролите не съвпадат'))
            return cleaned_data

        cleaned_data['new_password'] = make_password(new_password)

        return cleaned_data
