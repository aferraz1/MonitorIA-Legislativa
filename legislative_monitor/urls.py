from django.urls import path
from . import views

app_name = 'legislative_monitor'

urlpatterns = [
    path('deputados/', views.listar_deputados, name='deputados_list'),
    path('deputados/<int:id_deputado>/', views.detalhe_deputado, name='deputado_detail'),
    path('proposicoes/', views.listar_proposicoes, name='proposicoes_list'),
    path('proposicoes/<int:id_proposicao>/', views.detalhe_proposicao, name='proposicao_detail'),
    path('votacoes/', views.listar_votacoes, name='votacoes_list'),
    path('votacoes/<str:id_votacao>/', views.detalhe_votacao, name='votacao_detail'),
]
