import os

from django import template

register = template.Library()


@register.filter
def get_active_subcategories(category):
    return category.get_children().filter(is_active=True)


@register.simple_tag(takes_context=True)
def get_link_with_translation(context, cur_link):
    request = context['request']
    if cur_link.startswith('/'):
        cur_link = '/' + request.LANGUAGE_CODE + cur_link
    return cur_link


@register.filter
def takename(value):
    res = os.path.basename(value)
    return res
