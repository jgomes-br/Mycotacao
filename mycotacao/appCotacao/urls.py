from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_cotacao, name="index"),
    path('gerenciar/<int:pk>', views.GerenciarProjeto.as_view(), name="gerenciar_projeto"),
    path('cotacao/<int:projeto_id>', views.Cotacao.as_view(), name="cotacao"),
    path('cotacaoadm/<int:projeto_id>/<int:fornecedor_id>', views.Cotacao.as_view(), name="cotacaoadm"),
    path('baixar/<int:cotacao_id>', views.baixar_cotacao, name="baixar"),

]
