from .models import Estrutura, Lance
from decimal import Decimal

from .models import Projeto, Estrutura

def gravar_resposta_form(dono, id_estrutura:int, resposta:str, valor: str):
    # precisamos gravar a reposta recbidas da pagina 
    # lista == []
    estrutura = Estrutura.objects.get(pk=id_estrutura)
    
    print(dono.groups.filter(name='fornecedor').exists())
    if dono.groups.filter(name='fornecedor').exists():
        status = '2'
    else:
        status = '1'

    if resposta == 'INICIAL':
        Lance(estrutura = estrutura, dono=dono, lance=1, 
                preco=Decimal(valor.replace(',', '.')), status='P').save()
        estrutura.status = status
    else:
        lance = estrutura.lance_set.get(status='P') # type: ignore
    
        if resposta == "ACEITO":
            lance.status = "A"
            estrutura.status = '3'
            
        elif resposta == "RECUSADO":
            lance.status = "R"
            Lance(estrutura = estrutura, dono=dono, lance=lance.lance+1, 
                preco=Decimal(valor.replace(',', '.')), status='P').save()
            estrutura.status = status
        elif resposta == "DECLINAR":
            lance.status = "R"
            estrutura.status = '5'
    lance.save()
    estrutura.save()


def create_strutura(projeto: Projeto):
    try:
        for produto in projeto.produto.all():
            for fornecedor in projeto.fornecedor.all():
                if not Estrutura.objects.filter(projeto=projeto, produto=produto, fornecedor=fornecedor).exists():
                    Estrutura.objects.create(projeto=projeto, produto=produto, fornecedor=fornecedor, status='0').save()
        projeto.estrutura_set.exclude(fornecedor__in=projeto.fornecedor.all()).delete() # type: ignore
        projeto.estrutura_set.exclude(produto__in=projeto.produto.all()).delete() # type: ignore
    except:
        pass


def gravar_resposta_admin(resposta: str, dono):
    # cod_estrutura é um numero positivo
    # resposta -> [status, preco, nova_proposta]
    # status -> [ACEITO, RECUSADO, DECLINADO]
    # preco numero ou None -> 
    # nova_proposta -> indicando se o fornecedor pode fazer uma nova proposta
    ################################################################
    resposta = resposta + ":::"
    param = resposta.split(':')
    status = param[1]
    if not status:
        return

    cod_estrutura = int(param[0].replace('proposta-',''))
    preco = Decimal(param[2].replace(',', '.')) if param[2] else Decimal('0')
    nova_proposta = param[3]=='true'
    print(cod_estrutura, status, preco, nova_proposta, param[3] )
    ################################################################

    estrutura = Estrutura.objects.get(pk=cod_estrutura)
    lance = estrutura.lance_set.get(status='P') # type: ignore

    if status == 'ACEITO':
        lance.status = "A"
        estrutura.status = '3'
    elif status == 'RECUSADO':
        if not nova_proposta:
            estrutura.status = '4'
        else:
            estrutura.status = '1'
        lance.status = "R"
        Lance(estrutura = estrutura, dono=dono, lance=lance.lance+1, 
                preco=preco, status='P').save()
    lance.save()
    estrutura.save()
            