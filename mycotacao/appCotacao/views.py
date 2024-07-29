from typing import Any
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
# from django.contrib.auth.models import  User

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Projeto, Fornecedor, Lance
# camada logica
from .opdb import gravar_resposta_form

# Create your views here.

@login_required(login_url='/accounts/login/')
def lista_cotacao(request):
    lista = Projeto.objects.all()
    pagina = 'appCotacao/lista-projetos-fornecedores.html'
    return render(request, pagina, context={'projetos': lista, "eu":request.user})


# @login_required(login_url='/accounts/login/')

class GerenciarProjeto(DetailView):
    model = Projeto

    def colunas(self):
        return ('fornecedor1', 'fornecedor2', 'fornecedor3')

    def tabela(self):
        temp = {
            'colunas':('2:fornecedor1', '1:forncedor2', '3:fornecedor3'),
            'linhas':(
                ['produto1', [('preco1', 'dono'), 'preco2', 'preco3']],
                ['produto2', ['preco1', 'preco2', 'preco3']],
                ['produto3', ['preco1', 'preco2', 'preco3']],
                )
        }
        temp = {'colunas':[], 'linhas':[]}
        proj = self.get_object()

        for forn in proj.fornecedor.all(): # type: ignore
            temp['colunas'].append(forn)

        for prod in proj.produto.all(): # type: ignore
            lista_p = []
            for forn in temp['colunas']:
                est = proj.estrutura_set.get(fornecedor__pk=forn.id,  # type: ignore
                                             produto__descricao=prod.descricao)
                lance =  est.lance_set.last()
                lista_p.append((lance.preco, int(est.status), est.id))

            temp['linhas'].append([prod.descricao, lista_p])


        return temp
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        contexto =  super().get_context_data(**kwargs)
        contexto['tabela'] = self.tabela()
        contexto['eu'] = self.request.user
        
        return contexto

# def gerenciar(request, projeto_id):
#     pagina = 'appCotacao/gerenciar-cotacao.html'
#     projeto = Projeto.objects.get(pk=projeto_id)
#     return render(request, pagina, context={"eu":request.user, 
#                                             'projeto':projeto})



def cotacao(request, cod_cotacao, forn_id=None):

    if request.method == "POST":
        # print(request.user)
        for chave, [resposta, custo] in filter(lambda x: x[0].startswith("resposta"), request.POST.lists()):
            gravar_resposta_form(request.user, int(chave.replace("resposta-", "")), resposta, custo)
        return HttpResponseRedirect('/')
    
    pr = get_object_or_404(Projeto, pk=cod_cotacao)
    if not forn_id:
        forn = Fornecedor.objects.get(responsavel=request.user)
        perfil = 'FORNECEDOR'
    else:
        forn = Fornecedor.objects.get(pk=forn_id)
        perfil = 'ADMIM'


    estrutura =  pr.estrutura_set.filter(fornecedor__nomeempresa=forn.nomeempresa) # type: ignore
    lances = Lance.objects.filter(estrutura__projeto__id=pr.id, estrutura__fornecedor__id=forn.id) # type: ignore

    return render(request, 'appCotacao/cotacao.html', context={'estrutura':estrutura , 
                                                                'lances':lances, 'projeto': pr, 
                                                                "eu":request.user, 'forn':forn, 'perfil':perfil
                                                                })

