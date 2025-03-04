from ...models import Projeto, Cotacao
from ..constantes import EtapaCotacao


def criar_cotacoes(projeto: Projeto):
    """
    Cria as cotações para um projeto para cada combinação de produto e fornecedor, 
    se elas ainda não existirem, e remove cotações órfãs.
    """
    # Cria cotações para cada produto e fornecedor no projeto, se não existirem
    for produto in projeto.produtos.all():
        for fornecedor in projeto.fornecedores.all():
            if not Cotacao.objects.filter(projeto=projeto, produto=produto, fornecedor=fornecedor).exists():
                Cotacao.objects.create(
                    projeto=projeto,
                    produto=produto,
                    fornecedor=fornecedor,
                    status=EtapaCotacao.COTANDO  # '1'
                )
    # Remove cotações que não possuem fornecedor ou produto válidos
    try:
        projeto.estrutura_set.exclude(fornecedor__in=projeto.fornecedores.all()).delete()  # type: ignore
        projeto.estrutura_set.exclude(produto__in=projeto.produtos.all()).delete()  # type: ignore
    except Exception as e:
        # Registre o erro se necessário
        print("Erro ao limpar estruturas órfãs:", e)