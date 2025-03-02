from decimal import Decimal

from typing import NamedTuple
from ..models import Lance, CustomUser, Projeto

class Lances(NamedTuple):
    lance: int
    user: str
    preco: Decimal
    status: str
    
class CotacaoProdutos(NamedTuple):
    id: int
    produto: str
    status: str
    qtd_max_lances: int
    qtd_lances: int
    lances: Lances

class CotacaoCore:
    """
    Classe que agrega as informações de cotação para um projeto/fornecedor com base
    na 'estrutura' fornecida. Para cada item na estrutura, são processados os lances e
    definidos os parâmetros de acesso para edição e envio.
    """
    
    def __init__(self,projeto: Projeto, user_atual) -> None:
        # Obtém o nome do projeto a partir do primeiro item da estrutura, se disponível.
        
        self.projeto_name = projeto.nome
        
        # Lista que armazenará os produtos cotados em formato de dicionário.
        self.produtos_cotados = []  
        
        # Indica se o botão de envio deve ser habilitado.
        self.botao_enviar = False
        
        # Quantidade máxima de lances permitidos para cada produto.
        self.qtd_max_lance = 4

        self.user_atual = {'id': user_atual.id, 'nome': user_atual.first_name, 'is_staff': user_atual.is_staff}
        # Processa cada item (dado) da estrutura.
        self.processar_lances(projeto, user_atual)


    def processar_lances(self, projeto:Projeto, user_atual:CustomUser) -> None:
        """
        Processa um lances da lances:
          - Processa os lances associados;
          - Determina o nível de acesso baseado nas regras definidas;
          - Adiciona o produto cotado (como dicionário) à lista de produtos cotados.
        """


        # Itera sobre os lances associados ao dado.
        for produto in projeto.produto.all():
            temp_lances = []   # Lista para armazenar os lances deste item.
            for lance in Lance.objects.filter(projeto=projeto, produto=produto, fornecedor=user_atual):
                # Permite que o lance seja editado.
                lance.podeeditar = 'sim'
                
                # Verifica se o lance foi feito pelo usuário atual.
                user_lance = 'Eu' if lance.dono == user_atual else lance.dono.first_name
                
                # Cria um dicionário a partir do lance (supondo que Lances._asdict() converta para dict).
                lance_dict = Lances(lance.numero, user_lance, lance.preco, lance.get_status_display())._asdict()
                temp_lances.append(lance_dict)


            qtd_lances = len(temp_lances)
            ultimo_lance = temp_lances[-1]
            # Cria o objeto de CotacaoProdutos e o converte para dict.
            produto_cotado = CotacaoProdutos(
                produto.id,
                produto.descricao,
                {"cod": int(ultimo_lance.status), "desc": ultimo_lance.get_status_display()},
                self.qtd_max_lance,
                qtd_lances,
                temp_lances
            )._asdict()

        self.produtos_cotados.append(produto_cotado)

    def obter_dados_angular(self):
        return self.__dict__