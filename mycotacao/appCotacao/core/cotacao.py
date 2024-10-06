from decimal import Decimal

from django import forms
from ..models import Estrutura, Projeto
from typing import NamedTuple
from enum import IntEnum, auto

ESTRUTURA_STATUS_START = '0'
ESTRUTURA_STATUS_COTANDO  = '1'
ESTRUTURA_STATUS_ACEITAR_RECUSAR = '4'
ESTRUTURA_STATUS_FINALIZADO_COM_ACORDO = '3'
ESTRUTURA_STATUS_FINALIDO_SEM_ACORDO = '5'

class Acesso(IntEnum):
    podecotar = 1
    somentevalidar = 2
    inicio = 3
    naopodeeditar = 4

    def __str__(self) -> str:
        return self.name
    
class Lances(NamedTuple):
    lance: int
    user: str
    preco: Decimal
    status: str
    

class Cotacao(NamedTuple):
    id: int
    produto: str
    status: str
    lances: Lances
    acesso: Acesso
    ultimo_lance: str

class CotacaoCore:

    # def __init__(self, id_projeto, id_fornecedor, user_atual) -> None:
    def __init__(self, estrutura: Estrutura, user_atual) -> None:
        # estrutura = Estrutura.objects.filter(projeto_id=id_projeto, fornecedor_id=id_fornecedor)
        try:
            self.projeto = estrutura[0].projeto
        except: 
            pass
        # self.projeto = Projeto.objects.get(id=id_projeto)

        self.cotacoes: list[Cotacao] = []

        for dado in estrutura:
            qtd_max_lance = 4
            temp_lances = []
            ultimo_lance = None
            for lance in dado.lances.all():
                lance.podeeditar = 'sim'
                user_lance = 'Eu' if lance.dono == user_atual else lance.dono.first_name
                temp_lances.append(Lances(lance.lance, user_lance, lance.preco, lance.get_status_display ))
                ultimo_lance = user_lance
            # print(len(temp_lances), len(temp_lances) == qtd_max_lance)
            if len(temp_lances)==0:
                acesso = Acesso.inicio
            elif (len(temp_lances) == qtd_max_lance and ultimo_lance != 'Eu'):
                print("Nao pode cotar somente validar")
                acesso = Acesso.somentevalidar
            elif (dado.status == ESTRUTURA_STATUS_COTANDO and ultimo_lance != 'Eu'):
                acesso = Acesso.podecotar
            else:
                acesso = Acesso.naopodeeditar

            self.cotacoes.append(Cotacao(dado.id, dado.produto.descricao,
                                         dado.get_status_display ,temp_lances, acesso ,ultimo_lance))

        self.testeform  = forms.CharField(label="Produto", max_length=100)
