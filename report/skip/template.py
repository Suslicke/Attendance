from django import template

register = template.Library()

@register.filter
def all_or_not(value):
    ready = value[-1]
    return ready