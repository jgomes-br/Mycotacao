# from enum import IntEnum
# from typing import List, NamedTuple, Dict
# from decimal import Decimal
# from ..models import Projeto, CustomUser
# from .apoio import EnumStatusEstrutura

# class EnumStatus(IntEnum):
#     RECUSADO = 0
#     PENDENTE = 1
#     ACEITO = 2
#     COTAR = 3
    
#     def __str__(self) -> str:
#         return self.name

# class LanceForm(NamedTuple):
#     status: EnumStatus
#     qtdlances: int
#     custo: Decimal

# class Cotacao(NamedTuple):
#     fornecedor: str
#     cod_cotacao: int
#     status: EnumStatus
#     qtd_max_lances: int
#     lances: Dict[str, LanceForm]

# class Produto(NamedTuple):
#     produto: str
#     cotacoes: List[Cotacao]

# class TabelaCotacao:
#     def __init__(self, user: CustomUser, projeto: Projeto) -> None:
#         """
#         Inicializa a tabela de cotações para um projeto específico.
        
#         Args:
#             user (CustomUser): O usuário atual.
#             projeto (Projeto): O projeto para o qual as cotações são geradas.
#         """
#         self.user = user
#         self.fornecedores = list(projeto.fornecedor.all())
#         self.produtos = list(projeto.produto.all())
#         self.total_forn = len(self.fornecedores)
#         self.projeto = projeto
#         self.lista_produtos_cotados = {}

#         self.processar_cotacoes()

#     def processar_cotacoes(self) -> None:
#         """
#         Processa todas as cotações do projeto e as armazena na estrutura temporária.
#         """
#         for produto in self.produtos:
#             lista_cotacoes = {}
#             for cotacao in self.projeto.estrutura_set.filter(produto=produto.id):
#                 fornecedor = cotacao.fornecedor
#                 todos_lances = list(cotacao.lances.all())
#                 utimos_lances = self.obter_lances(todos_lances)
#                 status = self.get_status(cotacao.status, cotacao.lances.last())
#                 lista_cotacoes[fornecedor.id] = Cotacao(
#                     fornecedor.nome_fornecedor, cotacao.id, status, cotacao.total_lances, utimos_lances
#                 )._asdict()
#             self.lista_produtos_cotados[produto.id] = Produto(produto.descricao, lista_cotacoes)._asdict()  

#     def conv_status(self, status: str) -> int:
#         """
#         Converte o status de uma cotação.

#         Args:
#             status (str): Status da cotação.

#         Returns:
#             EnumStatus: Status da cotação.
#         """
#         if status == "R":
#             return EnumStatus.RECUSADO.value
#         elif status == "A":
#             return EnumStatus.ACEITO.value
#         return EnumStatus.PENDENTE.value

#     def obter_lances(self, todos_lances: List) -> Dict[str, LanceForm]:
#         """
#         Obtém os lances de um produto.

#         Args:
#             todos_lances (List): Lista de todos os lances de um produto.

#         Returns:
#             Dict[str, LanceForm]: Dicionário com os lances do fornecedor e do administrador.
#         """
#         if len(todos_lances) == 0:
#             return None
#         elif len(todos_lances) % 2 == 0:
#             ultimo_lance = todos_lances[-1]
#             penultimo_lance = todos_lances[-2]
#             lances = {
#                 "forn": LanceForm(
#                     self.conv_status(penultimo_lance.status), penultimo_lance.lance, penultimo_lance.preco
#                 )._asdict(),
#                 "adm": LanceForm(
#                     self.conv_status(ultimo_lance.status), ultimo_lance.lance, ultimo_lance.preco
#                 )._asdict()
#             }
#         else:
#             ultimo_lance = todos_lances[-1]
#             lances = {
#                 "forn": LanceForm(
#                     self.conv_status(ultimo_lance.status), ultimo_lance.lance, ultimo_lance.preco
#                 )._asdict(),
#                 "adm": LanceForm(EnumStatus.COTAR.value, 0, Decimal("0"))._asdict()
#             }
#             if ultimo_lance.status == "A":
#                 del lances["adm"]
#         return lances

#     def get_status(self, cotacao_status, ultimo_lance) -> int:
#         """
#         Obtém o status de uma cotação.

#         Args:
#             cotacao_status (EnumStatusEstrutura): Status da estrutura da cotação.
#             ultimo_lance: Último lance realizado.

#         Returns:
#             EnumStatus: Status da cotação.
#         """
#         status = EnumStatus.PENDENTE.value
#         if cotacao_status == EnumStatusEstrutura.COTANDO.value:
#             if ultimo_lance is not None and ultimo_lance.dono != self.user:
#                 status = EnumStatus.COTAR.value
#         elif cotacao_status == EnumStatusEstrutura.FINALIZADO_COM_ACORDO.value:
#             status = EnumStatus.ACEITO.value
#         elif cotacao_status == EnumStatusEstrutura.FINALIDO_SEM_ACORDO.value:
#             status = EnumStatus.ACEITO.value
#         return status

#     def get_cotacoes(self) -> Dict[Produto, List[Cotacao]]:
#         """
#         Retorna as cotações processadas.

#         Returns:
#             Dict[Produto, List[Cotacao]]: Dicionário com as cotações processadas.
#         """
#         produtos = self._get_produtos()
#         fornecedores = self._get_fornecedores()
#         return {
#             'projeto': {'nome': self.projeto.nome, 'id': self.projeto.id},
#             'produtos': produtos,
#             'fornecedores': fornecedores,
#             'cotacoes': self.lista_produtos_cotados
#         }

#     def _get_produtos(self) -> List[Dict]:
#         """
#         Retorna a lista de produtos.

#         Returns:
#             List[Dict]: Lista de produtos.
#         """
#         produtos = []
#         for prod in self.produtos:
#             produtos.append({'id': prod.id, 'descricao': prod.descricao})
#         return produtos

#     def _get_fornecedores(self) -> List[Dict]:
#         """
#         Retorna a lista de fornecedores.

#         Returns:
#             List[Dict]: Lista de fornecedores.
#         """
#         fornecedores = []
#         for forn in self.fornecedores:
#             fornecedores.append({'id': forn.id, 'nome_fornecedor': forn.nome_fornecedor})
#         return fornecedores