from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django import forms
from apps.cards.models import ClubCard
from apps.promo_codes.choices import PromoCodeStatuses
from apps.promo_codes.models import PromoCode

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class ApplyDiscountsForm(forms.Form):
    use_club_card = forms.BooleanField(required=False)
    card_number_or_code = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        use_club_card = cleaned_data.get('use_club_card')
        card_number_or_code = cleaned_data.get('card_number_or_code')

        dundio_club_card, promo_code = None, None
        if use_club_card:
            dundio_club_card = ClubCard.objects.filter(number=card_number_or_code).first()
            if not dundio_club_card:
                self.add_error('card_number_or_code', _('Няма такава карта!'))
        else:
            promo_code: PromoCode = PromoCode.objects.filter(title=card_number_or_code).first()
            if not promo_code:
                self.add_error('card_number_or_code', _('Няма такъв промо код!'))
            if promo_code and (
                    promo_code.status == PromoCodeStatuses.used or promo_code.valid_to_date < timezone.now()
            ):
                self.add_error('card_number_or_code', _('Този промо код вече е използван или е изтекал!'))

        cleaned_data['dundio_club_card'] = dundio_club_card
        cleaned_data['promo_code'] = promo_code
        return cleaned_data
