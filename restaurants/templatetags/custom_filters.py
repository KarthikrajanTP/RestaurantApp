from django import template

register = template.Library()

@register.filter
def is_filtered(query_dict):
    return any(
        value.strip() for key, value in query_dict.items()
        if key != 'page' and value.strip()
    )
