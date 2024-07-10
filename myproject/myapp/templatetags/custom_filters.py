from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='get_field_value')
def get_field_value(instance, field_name):
    """Retrieves the value of a model instance field dynamically."""
    return getattr(instance, field_name, '')


register = template.Library()

@register.filter(is_safe=True)  # Ensure your filter is marked as safe if it returns safe HTML/text
def intdot(value):
    try:
        # Handle value if it's a float
        if isinstance(value, float):
            value = round(value)  # You can also use int(value) if you're sure you won't need rounding
    except (ValueError, TypeError):
        return value  # If conversion fails, return original value
    value_with_comma = intcomma(value)
    return value_with_comma.replace(',', '.')



@register.filter(name='get_field_value')
def get_field_value(item, field_name):
    return getattr(item, field_name, "N/A")


@register.filter
def get_attribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    return getattr(value, arg, "")



@register.filter
def get_related_attribute(value, args):
    related_field, sub_field = args.split(',')
    try:
        related_obj = getattr(value, related_field)
        return getattr(related_obj, sub_field, 'N/A')
    except AttributeError:
        return 'N/A'
    
@register.filter(name='replace')
def replace(value, arg):
    """Custom template filter to replace strings in Django templates."""
    # arg should be in "find_this|replace_with_this" format
    try:
        original, new = arg.split('|')
        return value.replace(original, new)
    except ValueError:
        return value
    


@register.filter(name='get_attr')
def get_attr(obj, attr):
    """Recursively get an attribute."""
    try:
        for a in attr.split('__'):
            obj = getattr(obj, a)
        return obj
    except AttributeError:
        return ""
    
@register.filter(name='replace_underscores')
def replace_underscores(value):
    """Replaces double underscores in a string with spaces."""
    return value.replace("__", " ")


def convert_german_characters(value):
    replacements = {
        'ae': 'ä', 'oe': 'ö', 'ue': 'ü',
        'Ae': 'Ä', 'Oe': 'Ö', 'Ue': 'Ü'
    }
    for key, val in replacements.items():
        value = value.replace(key, val)
    return value

register.filter('convert_german', convert_german_characters)

@register.filter
def to_int(value):
    """Converts a float to an integer if possible."""
    try:
        # Check if the value is a float and convert to int
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
    except (ValueError, TypeError):
        return value