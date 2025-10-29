from django.urls import path
from . import views

app_name = 'news_portal'

urlpatterns = [
    path('', views.index, name='index'),
    path('noticias/', views.listar_noticias, name='noticias_list'),
    path('noticia/<slug:slug>/', views.detalhe_noticia, name='noticia_detail'),
    path('categoria/<slug:slug>/', views.noticias_por_categoria, name='categoria'),
]
