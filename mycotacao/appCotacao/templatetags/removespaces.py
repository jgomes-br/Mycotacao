from django import template

register = template.Library()

@register.filter
def removespaces(value):
    return value.replace(" ","_")