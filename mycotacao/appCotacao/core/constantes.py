from enum import Enum

# Constantes de status e etapas

class StatusLance(Enum):
    PENDENTE = 'P'
    ACEITO = 'A'
    RECUSADO = 'R'

class CotacaoStatus(Enum):
    FORN_N_TRABALHA = -1
    INICIO = 0
    CUSTO_CRF = 1
    CUSTO_FOR = 2
    CUSTO_FOR_CHECK = 3
    CUSTO_ACEITO_AGUARDANDO_VOLUME_CRF = 10
    CUSTO_CANCELADO = 13

    VOLUME_FORN = 21
    VOLUME_CRF = 22
    VOLUME_CHECK = 23
    VOLUME_CANCELADO = 24

    COTACAO_FINALIZADA = 1000