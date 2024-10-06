from enum import IntEnum, Enum

ESTRUTURA_STATUS_START = '0'
ESTRUTURA_STATUS_COTANDO  = '1'
ESTRUTURA_STATUS_ACEITAR_RECUSAR = '4'
ESTRUTURA_STATUS_FINALIZADO_COM_ACORDO = '3'
ESTRUTURA_STATUS_FINALIDO_SEM_ACORDO = '5'

class EnumStatusEstrutura(Enum):
    START = '0'
    COTANDO  = '1'
    ACEITAR_RECUSAR = '2'
    FINALIZADO_COM_ACORDO = '3'
    FINALIDO_SEM_ACORDO = '5'


class EnumAcesso(IntEnum):
    podecotar = 1
    somentevalidar = 2
    inicio = 3
    naopodeeditar = 4

    def __str__(self) -> str:
        return self.name
    