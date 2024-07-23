from .models import Estrutura, Lance
from decimal import Decimal

from .models import Projeto
from .formularios import ProjetoForm

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

def gravar_projeto(form:ProjetoForm, cod):

    if cod > -1:
        proj = Projeto.objects.get(pk = cod)
        proj.nome=form.cleaned_data['titulo']
        proj.start = form.cleaned_data['inicio']
        proj.produtos = form.cleaned_data['produto']
        proj.fornecedores = form.cleaned_data['fornecedor']
    else:
        proj = Projeto(nome=form.cleaned_data['titulo'], start = form.cleaned_data['inicio'])
    proj.save()
    return proj.id
    # Projeto(nome=form)
