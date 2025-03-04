from ...models import Projeto, Cotacao

def criar_cotacoes(projeto: Projeto):
    """
    Cria as cotações para um projeto para cada combinação de produto e fornecedor, 
    se elas ainda não existirem, e remove cotações órfãs.
    """
    produtos = projeto.produtos.all()
    fornecedores = projeto.fornecedores.all()

    # Recupera todas as cotações existentes para este projeto
    cotacoes_existentes = Cotacao.objects.filter(projeto=projeto).values_list("produto_id", "fornecedor_id")

    # Criar uma lista de cotações que ainda não existem
    novas_cotacoes = [
        Cotacao(projeto=projeto, produto=produto, fornecedor=fornecedor)
        for produto in produtos
        for fornecedor in fornecedores
        if (produto.id, fornecedor.id) not in cotacoes_existentes
    ]

    # Inserção eficiente no banco de dados
    if novas_cotacoes:
        Cotacao.objects.bulk_create(novas_cotacoes)

    # Remover cotações órfãs (onde produto ou fornecedor foram removidos do projeto)
    try:
        projeto.cotacao_set.filter(fornecedor__isnull=True).delete()
        projeto.cotacao_set.filter(produto__isnull=True).delete()
        projeto.cotacao_set.exclude(fornecedor__in=fornecedores).delete()
        projeto.cotacao_set.exclude(produto__in=produtos).delete()
    except Exception as e:
        print(f"Erro ao limpar estruturas órfãs: {e}")
