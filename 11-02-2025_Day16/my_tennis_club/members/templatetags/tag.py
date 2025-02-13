from django import template

register = template.Library()

@register.simple_tag
def calculate_total(price, quantity):
    """Returns total price for given quantity"""
    return price * quantity

