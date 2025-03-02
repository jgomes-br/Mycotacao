import json
from typing import Any
from django.db.models.query import QuerySet
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db import transaction
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

import os

from collections import namedtuple
# from django.contrib.auth.models import  User

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Projeto, CustomUser, Lance
from .core.cotacao import CotacaoCore
from .core.tabela_cotacao import TabelaCotacao
from .core.excel import ExportarExcel

from .opdb import gravar_resposta

# Create your views here.

LanceParam = namedtuple('LanceParam', ['preco', 'etapa', 'estrutura', 'num_lances'])

@login_required(login_url='/accounts/login/')
def lista_cotacao(request):
    lista = Projeto.objects.all()
    pagina = 'appCotacao/lista-projetos-fornecedores.html'
    if (request.user.is_superuser):
        return HttpResponseRedirect('/admin')
    return render(request, pagina, context={'projetos': lista})


def baixar_cotacao(request, cotacao_id):
    saida = os.path.join(settings.MEDIA_ROOT, "relatorio.xlsx")
    ExportarExcel(saida, request.user, Projeto.objects.get(id=cotacao_id))

    with open(saida, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(saida)
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
        contexto['dados'] = TabelaCotacao(self.request.user, self.get_object()).get_cotacoes()
        
        return contexto

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        # Define os cabeçalhos para não cachear a página
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class Cotacao(ListView):
    model = Lance
    template_name = 'appCotacao/cotacao.html'
    def get_queryset(self) -> QuerySet[Any]:
        qr = super().get_queryset()
        projeto_id = self.kwargs['projeto_id']

        if (self.request.user.is_staff):
            self.fornecedor = CustomUser.objects.get(pk=self.kwargs['fornecedor_id'])
        else:
            self.fornecedor = self.request.user

        # print(fornecedor.id, fornecedor.is_staff,  projeto_id)
        return qr.filter(fornecedor=self.fornecedor, projeto_id=projeto_id)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        resposta = json.loads(request.body)
        print(resposta)
        for r in resposta:
            if r['contraproposta'] != "":
                gravar_resposta(request.user, r['id'], r['contraproposta'])
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs: Any):
        contexto =  super().get_context_data(**kwargs)
        cotacao = CotacaoCore(contexto['object_list'], self.request.user)
        context = {
            'dados': cotacao.obter_dados_angular(),
            'fornecedor': self.fornecedor
        }
        
        return context
