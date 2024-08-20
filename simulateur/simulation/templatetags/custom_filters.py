from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_member_portfolio(portfolios, member):
    """
    Custom template filter to get the portfolio of a specific member.
    Usage: {{ portfolios|get_member_portfolio:member }}
    """
    return portfolios.filter(owner=member).first()

@register.filter
def get_item(dictionary, key):
    """
    Custom template filter to get a value from a dictionary.
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)

@register.filter
def get_attr(obj, attr_name):
    """
    Custom template filter to get an attribute of an object.
    Usage: {{ obj|get_attr:"attribute_name" }}
    """
    return getattr(obj, attr_name, None)

@register.filter
def currency(value):
    """
    Custom template filter to format a number as currency.
    Usage: {{ amount|currency }}
    """
    return "${:,.2f}".format(value)

@register.filter
def percentage(value):
    """
    Custom template filter to format a number as a percentage.
    Usage: {{ value|percentage }}
    """
    return "{:.2f}%".format(value)

@register.filter
def safe_html(value):
    """
    Custom template filter to mark a string as safe HTML.
    Usage: {{ html_string|safe_html }}
    """
    return mark_safe(value)