from django.core.exceptions import ObjectDoesNotExist
from ...models import Lance, CustomUser, Cotacao
from ..constantes import StatusLance, CotacaoStatus
from decimal import Decimal

class RespostaInterface:
    """
    Classe responsável por encapsular a lógica para responder à cotação.
    """
    def __init__(self, user_atual, cotacao: Cotacao, novo_custo: Decimal):
        self.user_atual = user_atual
        self.cotacao = cotacao
        self.novo_custo = novo_custo
        self.qtd_max_lances = cotacao.qtd_max_lances

        # Obter quantidade de lances e o último lance, se houver
        lances_qs = self.cotacao.lances_old.all()
        self.qtd_lances = lances_qs.count()
        try:
            self.ultimo_lance = lances_qs.last()
        except ObjectDoesNotExist:
            self.ultimo_lance = None

        # Determina se o usuário é fornecedor; supondo que 'dono.fornecedor' exista
        self.is_fornecedor = getattr(user_atual, 'fornecedor', False)

    def set_lance_pendente(self, novo_status: StatusLance):
        """
        Altera o status do lance pendente existente na estrutura.
        """
        try:
            self.cotacao.lances_old.filter(status='P').update(status=novo_status.value)
        except ObjectDoesNotExist:
            # Se não houver lance pendente, pode-se decidir criar um novo lance ou lançar exceção
            raise ObjectDoesNotExist("Não foi encontrado um lance pendente para alterar o status.")

    def aceitar_ultimo_lance(self):
        self.set_lance_pendente(StatusLance.ACEITO)

    def recusar_ultimo_lance(self):
        self.set_lance_pendente(StatusLance.RECUSADO)

    def criar_lance(self):
        """
        Cria um novo lance para a cotação com o novo custo informado.
        """
        num_lance = self.cotacao.lances_old.count() + 1

        novo_lance = Lance.objects.create(  # Usa `.create()` para criar e salvar em uma única linha
            dono=self.user_atual,
            sequencia=num_lance,
            preco=self.novo_custo,
            status=StatusLance.PENDENTE.value
        )

        self.cotacao.lances_old.add(novo_lance)  # Adiciona o lance à cotação

        # Atualiza a quantidade de lances de forma mais eficiente
        self.qtd_lances = self.cotacao.lances_old.count()

    def set_status_cotacao(self, status: CotacaoStatus):
        self.cotacao.status = status.value
        self.cotacao.save()

class AcoesLances:
    """
    Classe com métodos estáticos para executar as ações de lance.
    """
    @staticmethod
    def inicial(resposta: RespostaInterface):
        resposta.criar_lance()

    @staticmethod
    def aceito(resposta: RespostaInterface):
        resposta.aceitar_ultimo_lance()
        resposta.set_status_cotacao(CotacaoStatus.FINALIZADA_COM_ACORDO)

    @staticmethod
    def contra_proposta(resposta: RespostaInterface):
        resposta.recusar_ultimo_lance()
        resposta.criar_lance()
        if resposta.qtd_lances == resposta.qtd_max_lances:
            resposta.set_status_cotacao(CotacaoStatus.ACEITAR_RECUSAR)  
            # Ou use uma constante para esse status

    @staticmethod
    def declinar(resposta: RespostaInterface):
        resposta.recusar_ultimo_lance()
        resposta.set_status_cotacao(CotacaoStatus.FINALIZADO_SEM_ACORDO)


def gravar_resposta(user_atual: CustomUser, cotacao: Cotacao, novo_custo: Decimal):
    """
    Função que processa a resposta do usuário a uma cotação.
    Dependendo do valor de novo_custo e do lance atual, executa uma ação.
    """
    resposta = RespostaInterface(user_atual, cotacao, novo_custo)

    print(novo_custo)
    if cotacao.ja_finalizou:
        # nao fazer nada ja foi finalizado
        return

    if novo_custo == 999:
        AcoesLances.declinar(resposta)
    elif resposta.ultimo_lance is None:
        # Lance inicial
        AcoesLances.inicial(resposta)
    elif resposta.ultimo_lance.preco == resposta.novo_custo:
        # Aceita o novo custo
        AcoesLances.aceito(resposta)
    else:
        # Cadastra a nova contraproposta
        AcoesLances.contra_proposta(resposta)



