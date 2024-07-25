from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
# from django.contrib.auth.models import  User

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Projeto, Fornecedor, Lance, Produto
from .formularios import TesteForm

# camada logica
from .opdb import gravar_resposta_form

# Create your views here.

@login_required(login_url='/accounts/login/')
def lista_cotacao(request):
    # user_id = request.user
    # fornecedor = Fornecedor.objects.get(dono=user_id)
    lista = Projeto.objects.all()
    pagina = 'appCotacao/lista-projetos-fornecedores.html'
    if request.user.is_superuser:
        pagina = 'appCotacao/lista-projetos-manager.html' 
    
    return render(request, pagina, context={'projetos': lista})

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

