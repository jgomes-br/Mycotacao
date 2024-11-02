
from enum import IntEnum
from typing import List, NamedTuple
from collections import defaultdict

from decimal import Decimal
from ..models import Projeto, CustomUser
from .apoio import EnumStatusEstrutura

class EnumStatus(IntEnum):
    AGUARDANDO= 0
    FAZER_OU_ACEITAR= 1
    FINALIZADO_SUCESSO= 2
    FINALIZDO_SEM_SUCESSO= 3
    
    def __str__(self) -> str:
        return self.name
    


class Cotacao(NamedTuple):
    codigo: int
    fornecedor: CustomUser
    preco: Decimal
    status: EnumStatus
    num_lances: int

class Produto:
    decricao: str
    cotacoes: List[Cotacao]    

class TabelaCotacao:
    def __init__(self, user, projeto: Projeto) -> None:
        temp = defaultdict(list)

        for cotacao in projeto.estrutura_set.all():
            lance = cotacao.lances.last()
            qtd_lances = len(cotacao.lances.all())

            status = EnumStatus.AGUARDANDO

            if cotacao.status == EnumStatusEstrutura.COTANDO.value:
                if ((lance is not None) and(lance.dono != user)):
                    status = EnumStatus.FAZER_OU_ACEITAR
            elif cotacao.status == EnumStatusEstrutura.FINALIZADO_COM_ACORDO.value:
                status = EnumStatus.FINALIZADO_SUCESSO
            elif cotacao.status == EnumStatusEstrutura.FINALIDO_SEM_ACORDO.value:
                status = EnumStatus.FINALIZDO_SEM_SUCESSO

            preco = Decimal("0") if lance is None else lance.preco
            temp[cotacao.produto].append(Cotacao(cotacao.id ,cotacao.fornecedor, preco, status, qtd_lances))

        self.cotacoes = dict(temp)