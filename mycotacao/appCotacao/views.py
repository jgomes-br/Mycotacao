from typing import Any
from django.db.models.query import QuerySet
from django.forms import formset_factory
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

from .models import Cotacao, Projeto, CustomUser
from .core.tabela_cotacao import TabelaCotacao
from .core.excel import ExportarExcel
from .formularios import FormRespostaCotacao
from .core.constantes import CotacaoStatus
# camada logica
from .core.db.gravar_lances import gravar_resposta

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
        contexto['tabela'] = TabelaCotacao(self.request.user, self.get_object())
        
        return contexto


class CotacaoView(ListView):
    model = Cotacao
    template_name = 'appCotacao/cotacao.html'
    context_object_name = 'cotacoes'
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
        ResponderCotacaoFormSet = formset_factory(FormRespostaCotacao, extra=0)
        formset = ResponderCotacaoFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                cotacao_id = form.cleaned_data.get("cotacao_id")
                novo_custo = form.cleaned_data.get("novo_custo")
                if not novo_custo is None:
                    gravar_resposta(request.user, form.cotacao, novo_custo)
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        ResponderCotacaoFormSet = formset_factory(FormRespostaCotacao, extra=0)
        # Cria os dados iniciais para cada cotação, baseado na queryset atual
        initial_data = [{'cotacao_id': cotacao.id, 'cotacao': cotacao} for cotacao in self.get_queryset()]
        context['formset'] = ResponderCotacaoFormSet(initial=initial_data)
        
        # alguma_cotacao_aberta = any([cotacao.status in (0, 1, 2, 3) for cotacao in self.get_queryset()])
        # eu_posso_enviar_resosta = any([getattr(cotacao.lances_old.last(), "dono", None) != self.request.user for cotacao in self.get_queryset()])
        context['tem_cotacao_aberta'] = any([cotacao.status in range(3) for cotacao in self.get_queryset()])
        return context
