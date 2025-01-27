from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product, Producer, MeasureUnit


@register(Category)
class CategoryTranslations(TranslationOptions):
    fields = ('title', 'slug',)


@register(Producer)
class ProducerTranslations(TranslationOptions):
    fields = ('title',)


@register(MeasureUnit)
class MeasureUnitTranslations(TranslationOptions):
    fields = ('title',)


@register(Product)
class ProductTranslations(TranslationOptions):
    fields = ('title', 'slug', 'short_description', 'meta_title', 'meta_description', 'meta_key_words',)
