from decimal import Decimal

from django import forms
from ..models import Estrutura
from typing import NamedTuple
from .apoio import EnumAcesso, EnumStatusEstrutura

class Lances(NamedTuple):
    lance: int
    user: str
    preco: Decimal
    status: str
    

class Cotacao(NamedTuple):
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
    def __init__(self, estrutura: Estrutura, user_atual) -> None:
        # estrutura = Estrutura.objects.filter(projeto_id=id_projeto, fornecedor_id=id_fornecedor)
        try:
            self.projeto = estrutura[0].projeto
        except: 
            pass
        # self.projeto = Projeto.objects.get(id=id_projeto)

        self.cotacoes: list[Cotacao] = []

        for dado in estrutura:
            qtd_max_lance = dado.total_lances
            temp_lances = []
            ultimo_lance = None
            for lance in dado.lances.all():
                lance.podeeditar = 'sim'
                user_lance = 'Eu' if lance.dono == user_atual else lance.dono.first_name
                temp_lances.append(Lances(lance.lance, user_lance, lance.preco, lance.get_status_display ))
                ultimo_lance = user_lance

            if len(temp_lances)==0:
                acesso = EnumAcesso.inicio
            elif (len(temp_lances) == qtd_max_lance and ultimo_lance != 'Eu' and 
                  dado.status == EnumStatusEstrutura.ACEITAR_RECUSAR.value):
                acesso = EnumAcesso.somentevalidar
            elif (dado.status == EnumStatusEstrutura.COTANDO.value and ultimo_lance != 'Eu'):
                acesso = EnumAcesso.podecotar
            else:
                acesso = EnumAcesso.naopodeeditar

            self.cotacoes.append(Cotacao(dado.id, dado.produto.descricao,
                                         dado.get_status_display,qtd_max_lance, len(temp_lances) ,temp_lances, acesso ,ultimo_lance))

        self.testeform  = forms.CharField(label="Produto", max_length=100)
