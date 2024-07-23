from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_cotacao, name="index"),
    path('cotacao/<int:cod_cotacao>', views.cotacao, name="cotacao"),
    path('teste/', views.teste, name='teste'),
    path('novoprojeto/', views.criando_projeto, name='criandoprojeto'),
    path('editando/<int:cod_projeto>', views.criando_projeto, name='editando'),
]
