# https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
from django import template

register = template.Library()

@register.filter
def get_obj_attr(obj, attr):
    return getattr(obj, attr)