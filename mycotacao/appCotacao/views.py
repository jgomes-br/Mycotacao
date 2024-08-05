from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db import transaction

from collections import namedtuple
# from django.contrib.auth.models import  User

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Estrutura, Projeto, Fornecedor, Lance
# camada logica
from .opdb import gravar_resposta_form, gravar_resposta_admin

# Create your views here.

LanceParam = namedtuple('LanceParam', ['preco', 'etapa', 'estrutura', 'num_lances'])

@login_required(login_url='/accounts/login/')
def lista_cotacao(request):
    lista = Projeto.objects.all()
    pagina = 'appCotacao/lista-projetos-fornecedores.html'
    return render(request, pagina, context={'projetos': lista})


# @login_required(login_url='/accounts/login/')
class GerenciarProjeto(DetailView):
    model = Projeto
    template_name = 'appCotacao/projeto_detail.html'

    def tabela(self):
        # temp = {
        #     'colunas':('2:fornecedor1', '1:forncedor2', '3:fornecedor3'),
        #     'linhas':(
        #         ['produto1', [('preco1', 'dono'), 'preco2', 'preco3']],
        #         ['produto2', ['preco1', 'preco2', 'preco3']],
        #         ['produto3', ['preco1', 'preco2', 'preco3']],
        #         )
        # }
        temp = {'colunas':[], 'linhas':[]}
        proj = self.get_object()

        for forn in proj.fornecedor.all(): # type: ignore
            temp['colunas'].append(forn)

        for prod in proj.produto.all(): # type: ignore
            lista_p = []
            for forn in temp['colunas']:
                est = proj.estrutura_set.get(fornecedor__pk=forn,  # type: ignore
                                             produto__descricao=prod.descricao)
                lance =  est.lances.last() 
                # print(est.lances.all().count())
                lista_p.append(LanceParam(lance.preco if lance else 0, int(est.status), est.id, est.lances.all().count()))

            temp['linhas'].append([prod.descricao, lista_p])


        return temp
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        for chave, [resposta] in filter(lambda x: x[0].startswith("proposta"), request.POST.lists()):
            gravar_resposta_admin(chave+":"+resposta, request.user)

        return redirect(request.META['HTTP_REFERER'])
    
    def get_object(self):
        return get_object_or_404(Projeto, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        contexto =  super().get_context_data(**kwargs)
        contexto['tabela'] = self.tabela()
        
        return contexto


class Cotacao(ListView):
    model = Estrutura

    def get_queryset(self) -> QuerySet[Any]:
        qr = super().get_queryset()
        projeto_id = self.kwargs['projeto_id']
        try:
            fornecedor = Fornecedor.objects.get(pk=self.kwargs['fornecedor_id'])
        except KeyError:
            fornecedor = self.request.user.fornecedor # type: ignore

        return qr.filter(fornecedor=fornecedor, projeto_id=projeto_id)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        for chave, [resposta, custo] in filter(lambda x: x[0].startswith("resposta"), request.POST.lists()):
            gravar_resposta_form(request.user, int(chave.replace("resposta-", "")), resposta, custo)
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        contexto =  super().get_context_data(**kwargs)
        return contexto


# def cotacao(request, cod_cotacao, forn_id=None):

#     if request.method == "POST":
#         # print(request.user)
#         for chave, [resposta, custo] in filter(lambda x: x[0].startswith("resposta"), request.POST.lists()):
#             gravar_resposta_form(request.user, int(chave.replace("resposta-", "")), resposta, custo)
#         return HttpResponseRedirect('/')
    
#     pr = get_object_or_404(Projeto, pk=cod_cotacao)
#     if not forn_id:
#         forn = Fornecedor.objects.get(responsavel=request.user)
#         perfil = 'FORNECEDOR'
#     else:
#         forn = Fornecedor.objects.get(pk=forn_id)
#         perfil = 'ADMIM'


#     estrutura =  pr.estrutura_set.filter(fornecedor__nomeempresa=forn.nomeempresa) # type: ignore
#     lances = Lance.objects.filter(estrutura__projeto__id=pr.id, estrutura__fornecedor__id=forn.id) # type: ignore

#     return render(request, 'appCotacao/cotacao.html', context={'estrutura':estrutura , 
#                                                                 'lances':lances, 'projeto': pr, 
#                                                                 "eu":request.user, 'forn':forn, 'perfil':perfil
#                                                                 })

