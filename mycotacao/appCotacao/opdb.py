from abc import ABC
from .models import Estrutura, Lance
from decimal import Decimal

from .models import Projeto, Estrutura

STATUS_INICIAL = 'INICIAL'
STATUS_ACEITO = 'ACEITO'
STATUS_RECUSADO = 'RECUSADO'
STATUS_DECLINAR = 'DECLINAR'

ETAPA_ESTRUTURA_FORNECEDOR = '1'
ETAPA_ESTRUTURA_ADMINISTRADOR = '2'
ETAPA_ESTRUTURA_FINALIZADA = '3'
ETAPA_ESTRUTURA_NAO_PODE_LANCE = '4'
ETAPA_ESTRUTURA_FINALIZADO_SEM_ACORDO = '5'


def is_fornecedor(dono):
    return dono.groups.filter(name='fornecedor').exists()

class RespostaInterface:

    def __init__(self, dono, id_estrutura: int, resposta: str, valor: str|None, pode_proposta: bool) :
        self.dono = dono
        self.pode_proposta = pode_proposta
        self.estrutura= Estrutura.objects.get(pk=id_estrutura)
        self.resposta = resposta
        # self.is_fornecedor = dono.groups.filter(name='fornecedor').exists()
        try:
            self.is_fornecedor = True if dono.fornecedor else False
        except:
            self.is_fornecedor = False

        if valor:
            self.valor = Decimal(valor.replace(',', '.'))

    def set_lance_pendente(self, status):
        lance = self.estrutura.lances.get(status='P') # type: ignore
        lance.status = status
        lance.save()

    def aceitar_ultimo_lance(self):
        self.set_lance_pendente('A')

    def recusar_ultimo_lance(self):
        self.set_lance_pendente('R')

    def criar_lance(self):
        num_lance = self.estrutura.lances.all().count() +1 # type: ignore
        lance = Lance(dono=self.dono, lance=num_lance, 
                    preco=self.valor, status='P')
        lance.save()
        self.estrutura.lances.add(lance)

    def set_status_estrutura(self, status):
        self.estrutura.status = status
        self.estrutura.save()

class AcoesLances:

    @staticmethod
    def incial(resposta:RespostaInterface):
        resposta.criar_lance()
        resposta.set_status_estrutura(ETAPA_ESTRUTURA_ADMINISTRADOR)

    @staticmethod
    def aceito(resposta:RespostaInterface):
        resposta.aceitar_ultimo_lance()
        resposta.set_status_estrutura(ETAPA_ESTRUTURA_FINALIZADA)

    @staticmethod
    def recusado(resposta:RespostaInterface):
        resposta.recusar_ultimo_lance()
        resposta.criar_lance()
        if resposta.is_fornecedor:
            resposta.set_status_estrutura(ETAPA_ESTRUTURA_ADMINISTRADOR)
        elif not resposta.pode_proposta:
            resposta.set_status_estrutura(ETAPA_ESTRUTURA_NAO_PODE_LANCE)
        else:
            resposta.set_status_estrutura(ETAPA_ESTRUTURA_FORNECEDOR)

    @staticmethod
    def declinar(resposta:RespostaInterface):
        resposta.recusar_ultimo_lance()
        resposta.set_status_estrutura(ETAPA_ESTRUTURA_FINALIZADO_SEM_ACORDO)


def gravar_resposta_form(dono, id_estrutura:int, resposta:str, valor: str, pode_nova_proposta=True):
    # precisamos gravar a reposta recbidas da pagina 
    resp_i = RespostaInterface(dono, id_estrutura, resposta, valor, pode_nova_proposta)
    if resposta == STATUS_INICIAL:
        AcoesLances.incial(resp_i)
    elif resposta == STATUS_ACEITO:
        AcoesLances.aceito(resp_i)
    elif resposta == STATUS_RECUSADO:
        AcoesLances.recusado(resp_i)
    elif resposta == STATUS_DECLINAR:
        AcoesLances.declinar(resp_i)

def create_strutura(projeto: Projeto):
    try:
        for produto in projeto.produto.all():
            for fornecedor in projeto.fornecedor.all():
                if not Estrutura.objects.filter(projeto=projeto, produto=produto, fornecedor=fornecedor).exists():
                    Estrutura.objects.create(projeto=projeto, produto=produto, fornecedor=fornecedor, status='0').save()
        projeto.estrutura_set.exclude(fornecedor__in=projeto.fornecedor.all()).delete() # type: ignore
        projeto.estrutura_set.exclude(produto__in=projeto.produto.all()).delete() # type: ignore
    except:
        pass


def gravar_resposta_admin(resposta: str, dono):
    # cod_estrutura é um numero positivo
    # resposta -> [status, preco, nova_proposta]
    # status -> [ACEITO, RECUSADO, DECLINADO]
    # preco numero ou None -> 
    # nova_proposta -> indicando se o fornecedor pode fazer uma nova proposta
    ################################################################
    resposta = resposta + ":::"
    param = resposta.split(':')
    status = param[1]
    if not status:
        return

    cod_estrutura = int(param[0].replace('proposta-',''))
    preco = param[2]
    nova_proposta = param[3]=='true'
    gravar_resposta_form(dono, cod_estrutura, status, preco, nova_proposta)
            