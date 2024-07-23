from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
# from django.contrib.auth.models import  User

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Projeto, Fornecedor, Lance, Produto
from .formularios import TesteForm, ProjetoForm

# camada logica
from .banco_dados import gravar_resposta_form, gravar_projeto

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

def cotacao(request, cod_cotacao):

    if request.method == "POST":
        # print(request.user)
        for chave, [resposta, custo] in filter(lambda x: x[0].startswith("resposta"), request.POST.lists()):
            gravar_resposta_form(request.user, int(chave.replace("resposta-", "")), resposta, custo)
        return HttpResponseRedirect('/')
    
    pr = get_object_or_404(Projeto, pk=cod_cotacao)
        
    estrutura =  pr.estrutura_set.filter(fornecedor__nome=forn.nome) # type: ignore
    lances = Lance.objects.filter(estrutura__projeto__id=pr.id, estrutura__fornecedor__id=forn.id) # type: ignore

    return render(request, 'appCotacao/cotacao.html', context={'estrutura':estrutura , 
                                                                'lances':lances, 'projeto': pr, 
                                                                "eu":request.user,
                                                                })

def criando_projeto(request, cod_projeto=-1):
    
    if request.method == 'POST':
        print('post')
        form = ProjetoForm(request.POST)
        if form.is_valid():
            try:
                gravar_projeto(form, cod_projeto)
            except IntegrityError:
                print('Não foi possivel')
    elif cod_projeto > -1:
        # editando
        pr = Projeto.objects.get(pk=cod_projeto)
        data = {'titulo':pr.nome, 'inicio':pr.start, 'fim':pr.fim, 'cod':cod_projeto,
                'fornecedor':pr.fornecedores, 'produto':pr.produtos}
        form = ProjetoForm(initial=data)
        
    else:
        # novo
        form = ProjetoForm()

    fonecedores = Fornecedor.objects.all()
    produtos = Produto.objects.all()
    contexto = {'form': form,  'fornecedores': fonecedores, 'produtos': produtos}
    return render(request, 'appCotacao/novoprojeto.html', context=contexto)


def teste(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TesteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data['subject'])
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse("/teste")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TesteForm()
        
    return render(request, 'appCotacao/teste.html', context={"formulario": form})