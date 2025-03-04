from enum import Enum

# Constantes de status e etapas

class StatusLance(Enum):
    PENDENTE = 'P'
    ACEITO = 'A'
    RECUSADO = 'R'

class EtapaCotacao(Enum):
    COTANDO = 1
    ACEITAR_RECUSAR = 2
    FINALIZADA_COM_ACORDO = 3
    FINALIZADO_SEM_ACORDO = 5