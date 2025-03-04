from django import template
from ..core.constantes import EtapaCotacao, StatusLance
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def removespaces(value):
    return value.replace(" ","_")

@register.filter
def index(value, arg):
    """Retorna o elemento na posição 'arg' da lista 'value'."""
    try:
        return value[int(arg)]
    except (IndexError, ValueError, TypeError):
        return None
    

@register.filter
def minha_vez(cotacao, user):
    eu_fiz_ultimo_lance = getattr(cotacao.lances_old.last(), "dono", None) == user
    cotacao_aberta = cotacao.status <= EtapaCotacao.ACEITAR_RECUSAR.value
    primeiro_lance = cotacao.lances_old.all().count() == 0
    sou_fornecedor = not user.is_staff
    return ((not eu_fiz_ultimo_lance)and (cotacao_aberta))

@register.filter
def posso_fazer_contraproposta(cotacao, user):
    eu_fiz_ultimo_lance = getattr(cotacao.lances_old.last(), "dono", None) == user
    cotacao_aberta = cotacao.status == EtapaCotacao.COTANDO.value
    return ((not eu_fiz_ultimo_lance)and (cotacao_aberta))

# configuracao do template cores e icones
@register.filter
def primeiro_lance(cotacao, user):
    primeiro_lance = cotacao.lances_old.all().count() == 0
    sou_fornecedor = not user.is_staff
    return ((primeiro_lance)and (sou_fornecedor))
lista_pendentes = (StatusLance.PENDENTE.value, 
                   EtapaCotacao.COTANDO.value, 
                   EtapaCotacao.ACEITAR_RECUSAR.value)
lista_aceitos = (StatusLance.ACEITO.value, 
                 EtapaCotacao.FINALIZADA_COM_ACORDO.value)
lista_recusados = (StatusLance.RECUSADO.value, 
                   EtapaCotacao.FINALIZADO_SEM_ACORDO.value)
@register.filter
def getcolorstatus(value):
    if value in lista_pendentes:
        part = 'warning text-dark'
    elif value in lista_aceitos:
        part = 'success'
    elif value in lista_recusados:
        part = 'danger'
    else:
        part = 'light'

    return "badge bg-" + part

@register.filter
def icone_status(status):
    icone = ''
    if status in lista_recusados:
        icone = "bi bi-x-circle"
    elif status in lista_aceitos:
        icone = 'bi bi-check-circle'
    elif status in lista_pendentes:
        icone = 'bi bi-exclamation-triangle'
    if icone:
        return mark_safe(f'<i class="{icone}"></i>')
    else:
        return ''
    
@register.filter
def color_background(status):
    if status in lista_recusados:
        return "bg-danger text-white"
    elif status in lista_aceitos:
        return "bg-success text-white"
    elif status in lista_pendentes:
        return "bg-warning"