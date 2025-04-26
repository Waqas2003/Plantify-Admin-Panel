# dashboard/templatetags/custom_filters.py
from django import template

register = template.Library()  # Correct syntax (not <library())

@register.filter(name='divide')
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):  # Fixed typo in exception
        return 0

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0