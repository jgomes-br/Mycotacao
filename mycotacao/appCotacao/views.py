from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db import transaction
from django.conf import settings

import os

from collections import namedtuple
# from django.contrib.auth.models import  User

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Estrutura, Projeto, Fornecedor, Lance
from . formularios import CotacaoFormSet
from .core.cotacao import CotacaoCore
from .core.tabela_cotacao import TabelaCotacao
from .core.excel import ExportarExcel
# camada logica
from .opdb import gravar_resposta_form, gravar_resposta_admin, gravar_resposta

# Create your views here.

LanceParam = namedtuple('LanceParam', ['preco', 'etapa', 'estrutura', 'num_lances'])

@login_required(login_url='/accounts/login/')
def lista_cotacao(request):
    lista = Projeto.objects.all()
    pagina = 'appCotacao/lista-projetos-fornecedores.html'
    
    try:
        request.user.fornecedor
    except:
        return HttpResponseRedirect('/admin')
    return render(request, pagina, context={'projetos': lista})


def baixar_cotacao(request, cotacao_id):
    file_path = os.path.join(settings.MEDIA_ROOT, "temp_cotacao.xlsx")
    ExportarExcel(file_path)

    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response

# @login_required(login_url='/accounts/login/')
class GerenciarProjeto(DetailView):
    model = Projeto
    template_name = 'appCotacao/projeto_detail.html'
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        for chave, [custo] in filter(lambda x: x[0].startswith("proposta"), request.POST.lists()):
            cotacao_id = int(chave.replace("proposta-", ""))
            # print(cotacao_id, custo, request.user)
            if (custo != ""):
                gravar_resposta(request.user,cotacao_id, custo)
        return redirect(request.META['HTTP_REFERER'])
    
    def get_object(self):
        return get_object_or_404(Projeto, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs: Any):
        contexto =  super().get_context_data(**kwargs)
        contexto['tabela'] = TabelaCotacao(self.request.user, self.get_object())
        
        return contexto


class Cotacao(ListView):
    model = Estrutura
    template_name = 'appCotacao/cotacao.html'
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
        print(list(request.POST.lists()))
        for resposta, [custo] in filter(lambda x: x[0].startswith("input-resposta"), request.POST.lists()):
            gravar_resposta(request.user,int(resposta.replace("input-resposta-", "")), custo)
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs: Any):
        contexto =  super().get_context_data(**kwargs)
        cotacao = CotacaoCore(contexto['object_list'], self.request.user)

        context = {
            'dados': cotacao,
        }

        return context

def cotacao_nova(request):
    cotacao = CotacaoCore(3, 3, request.user)


    

    context = {
        'dados': cotacao,
    }

    return render(request, 'appCotacao/cotacao2.html', context)
        