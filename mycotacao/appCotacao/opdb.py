from abc import ABC
from .models import Estrutura, Lance
from decimal import Decimal

from .models import Projeto, Estrutura

STATUS_INICIAL = 'INICIAL'
STATUS_ACEITO = 'ACEITO'
STATUS_RECUSADO = 'RECUSADO'
STATUS_DECLINAR = 'DECLINAR'

ETAPA_ESTRUTURA_COTANDO = '1'
ETAPA_ESTRUTURA_FINALIZADA = '3'
ETAPA_ESTRUTURA_NAO_PODE_LANCE = '4'
ETAPA_ESTRUTURA_FINALIZADO_SEM_ACORDO = '5'

def is_fornecedor(dono):
    return dono.groups.filter(name='fornecedor').exists()

class RespostaInterface:

    def __init__(self, dono, id_estrutura: int, valor: str) :
        self.dono = dono
        self.estrutura= Estrutura.objects.get(pk=id_estrutura)

        try:
            self.ultimo_lance =  self.estrutura.lances.all().latest('lance')
        except:
            self.ultimo_lance = None

        try:
            self.is_fornecedor = True if dono.fornecedor else False
        except:
            self.is_fornecedor = False

        if valor:
            self.novo_custo = Decimal(valor.replace(',', '.'))

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
                    preco=self.novo_custo, status='P')
        lance.save()
        self.estrutura.lances.add(lance)

    def set_status_estrutura(self, status):
        self.estrutura.status = status
        self.estrutura.save()

class AcoesLances:

    @staticmethod
    def incial(resposta:RespostaInterface):
        resposta.criar_lance()

    @staticmethod
    def aceito(resposta:RespostaInterface):
        resposta.aceitar_ultimo_lance()
        resposta.set_status_estrutura(ETAPA_ESTRUTURA_FINALIZADA)

    @staticmethod
    def contra_proposta(resposta:RespostaInterface):
        resposta.recusar_ultimo_lance()
        resposta.criar_lance()

    @staticmethod
    def declinar(resposta:RespostaInterface):
        resposta.recusar_ultimo_lance()
        resposta.set_status_estrutura(ETAPA_ESTRUTURA_FINALIZADO_SEM_ACORDO)


def gravar_resposta(dono, id_estrutura: int, novo_custo: str):
    # print(dono, id_estrutura, novo_custo)
    resp_i = RespostaInterface(dono, id_estrutura, novo_custo)
    if novo_custo == '999':
        AcoesLances.declinar(resp_i)
    elif resp_i.ultimo_lance is None:
        # lance inicial
        AcoesLances.incial(resp_i) 
    elif resp_i.ultimo_lance.preco == resp_i.novo_custo:
        # aceitando o novo custo
        AcoesLances.aceito(resp_i)
    elif resp_i.novo_custo == 0:
        # recusanDo o custo e não pode fazer um novo lance
        AcoesLances.declinar(resp_i)
    else:
        # cadastrar o novo custo
        AcoesLances.contra_proposta(resp_i)

def create_strutura(projeto: Projeto):
    try:
        for produto in projeto.produto.all():
            for fornecedor in projeto.fornecedor.all():
                if not Estrutura.objects.filter(projeto=projeto, produto=produto, fornecedor=fornecedor).exists():
                    Estrutura.objects.create(projeto=projeto, produto=produto, fornecedor=fornecedor, status='1').save()
        projeto.estrutura_set.exclude(fornecedor__in=projeto.fornecedor.all()).delete() # type: ignore
        projeto.estrutura_set.exclude(produto__in=projeto.produto.all()).delete() # type: ignore
    except:
        pass


