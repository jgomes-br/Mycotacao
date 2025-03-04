from django import template
from ..core.constantes import CotacaoStatus, StatusLance
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def removespaces(value):
    return value.replace(" ","_")

@register.filter
def exibir_proposta_contraproposta(status, user):
    cotando = status >= 0 and status <= 2
    primeiro_lance = status == 0
    usuario_carrefour = user.is_staff
    return cotando and (not(primeiro_lance and usuario_carrefour))

