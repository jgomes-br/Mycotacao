from .models import Estrutura, Lance
from decimal import Decimal

from .models import Projeto, Estrutura

def gravar_resposta_form(dono, id_estrutura:int, resposta:str, valor: str):
    # precisamos gravar a reposta recbidas da pagina 
    # lista == []
    estrutura = Estrutura.objects.get(pk=id_estrutura)
    lance = estrutura.lance_set.get(status='P') # type: ignore
    print(resposta)
    
    if resposta == "ACEITO":
        lance.status = "A"
        estrutura.status = '3'
        
    elif resposta == "RECUSADO":
        lance.status = "R"
        lance.save()
        Lance(estrutura = estrutura, dono=dono, lance=lance.lance+1, 
              preco=Decimal(valor.replace(',', '.')), status='P').save()
        estrutura.status = '2'
    lance.save()
    estrutura.save()


def create_strutura(projeto: Projeto):
    for produto in projeto.produto.all():
        for fornecedor in projeto.fornecedor.all():
            if not Estrutura.objects.filter(projeto=projeto, produto=produto, fornecedor=fornecedor).exists():
                Estrutura.objects.create(projeto=projeto, produto=produto, fornecedor=fornecedor).save()

    projeto.estrutura_set.exclude(fornecedor__in=projeto.fornecedor.all()).delete() # type: ignore
    projeto.estrutura_set.exclude(produto__in=projeto.produto.all()).delete() # type: ignore