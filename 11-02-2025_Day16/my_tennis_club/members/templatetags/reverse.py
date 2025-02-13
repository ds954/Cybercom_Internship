from django import template

register=template.Library()

@register.filter()
def reverse_word(value):
    return ' '.join(value.split()[::-1])
