from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_cotacao, name="index"),
    path('cotacao/<int:cod_cotacao>', views.cotacao, name="cotacao"),
    path('gerenciar/<int:pk>', views.GerenciarProjeto.as_view(), name="gerenciar_projeto"),
    path('cotacaoadm/<int:cod_cotacao>/<int:forn_id>', views.cotacao, name="cotacaoadm"),
]
