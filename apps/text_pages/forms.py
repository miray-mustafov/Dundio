from django import forms

from apps.common.forms import BaseForm
from apps.text_pages.models import TextPage


class TextPageForm(BaseForm):
    class Meta:
        model = TextPage
        fields = (
            'title',
            'slug',
            'short_description',
            'description',
            'main_image',
            'youtube_link',
            'is_active',
            'meta_title',
            'meta_description',
            'meta_key_words',
        )
