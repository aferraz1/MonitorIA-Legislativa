from django.urls import path
from . import views
from .views import TipoProposicaoListView, TipoProposicaoDetailView
from .views_graficos import graficos_partidos

app_name = 'legislative_monitor'

urlpatterns = [
    path('deputados/', views.listar_deputados, name='deputados_list'),
    path('deputados/<int:id_deputado>/', views.detalhe_deputado, name='deputado_detail'),
    path('proposicoes/', views.listar_proposicoes, name='proposicoes_list'),
    path('proposicoes/<int:id_proposicao>/', views.detalhe_proposicao, name='proposicao_detail'),
    path('votacoes/', views.listar_votacoes, name='votacoes_list'),
    path('votacoes/<str:id_votacao>/', views.detalhe_votacao, name='votacao_detail'),
    
    # Tipos de Proposição
    path('tipos-proposicao/', TipoProposicaoListView.as_view(), name='tipos_proposicao_list'),
    path('tipos-proposicao/<int:pk>/', TipoProposicaoDetailView.as_view(), name='tipo_proposicao_detail'),
    
    # Partidos
    path('partidos/', views.listar_partidos, name='partidos_list'),
    path('partidos/<str:sigla>/', views.detalhe_partido, name='partido_detail'),
    
    # Gráficos
    path('graficos/partidos/', graficos_partidos, name='graficos_partidos'),
]
