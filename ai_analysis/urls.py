from django.urls import path
from . import views

app_name = 'ai_analysis'

urlpatterns = [
    path('', views.index, name='index'),
    path('resumos/', views.resumos, name='resumos_list'),
    path('resumos/<int:pk>/', views.detalhe_resumo, name='resumo_detail'),
    path('analises-impacto/', views.analises_impacto, name='analises_impacto_list'),
    path('analises-impacto/<int:pk>/', views.detalhe_analise_impacto, name='analise_impacto_detail'),
    path('busca-semantica/', views.busca_semantica, name='busca_semantica'),
]
