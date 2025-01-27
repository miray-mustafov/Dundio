from django import forms
from django.utils.translation import gettext_lazy as _


class BaseForm(forms.ModelForm):
    """Handling title slug uniqueness validation"""

    def clean_title(self):
        cur_instance_id = self.instance.id if self.instance else None
        title = self.cleaned_data.get('title')
        existing_obj = self.Meta.model.objects.filter(title=title).exclude(id=cur_instance_id).exists()
        if existing_obj:
            self.add_error('title', _(f'Обект с такова заглавие вече съществува'))
        return title

    def clean_slug(self):
        cur_instance_id = self.instance.id if self.instance else None
        slug = self.cleaned_data.get('slug')
        existing_obj = self.Meta.model.objects.filter(slug=slug).exclude(id=cur_instance_id).exists()
        if existing_obj:
            self.add_error('slug', _(f'Обект с такъв слъг вече съществува'))
        return slug
