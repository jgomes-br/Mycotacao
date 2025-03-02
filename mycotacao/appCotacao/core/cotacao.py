from decimal import Decimal

from django import forms
from ..models import Cotacao
from typing import NamedTuple
from .apoio import EnumAcesso, EnumStatusEstrutura

class Lances(NamedTuple):
    lance: int
    user: str
    preco: Decimal
    status: str
    

class CotacaoReposta(NamedTuple):
    id: int
    produto: str
    status: str
    qtd_max_lances: int
    qtd_lances: int
    lances: Lances
    acesso: EnumAcesso
    ultimo_lance: str

class CotacaoCore:

    # def __init__(self, id_projeto, id_fornecedor, user_atual) -> None:
    def __init__(self, estrutura: Cotacao, user_atual) -> None:
        # estrutura = Estrutura.objects.filter(projeto_id=id_projeto, fornecedor_id=id_fornecedor)
        try:
            self.projeto = estrutura[0].projeto
        except: 
            pass
        self.cotacoes: list[CotacaoReposta] = []

        self.botao_enviar = False
        qtd_max_lance = 4
        for dado in estrutura:
            temp_lances = []
            ultimo_lance = None
            for lance in dado.lances.all():
                lance.podeeditar = 'sim'
                user_lance = 'Eu' if lance.dono == user_atual else lance.dono.first_name
                temp_lances.append(Lances(lance.sequencia, user_lance, lance.preco, lance.get_status_display ))
                ultimo_lance = user_lance
            qtd_lances = len(temp_lances)
            if qtd_lances==0:
                acesso = EnumAcesso.inicio
                self.botao_enviar = True
            elif (qtd_lances == qtd_max_lance and ultimo_lance != 'Eu'):
                acesso = EnumAcesso.somentevalidar
                self.botao_enviar = True
            elif (dado.status == EnumStatusEstrutura.COTANDO.value and ultimo_lance != 'Eu'):
                acesso = EnumAcesso.podecotar
                self.botao_enviar = True
            else:
                acesso = EnumAcesso.naopodeeditar

            self.cotacoes.append(CotacaoReposta(dado.id, dado.produto.descricao,
                                         dado.get_status_display,qtd_max_lance, qtd_lances ,temp_lances, acesso ,ultimo_lance))

        self.testeform  = forms.CharField(label="Produto", max_length=100)
