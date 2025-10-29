from django.urls import path
from . import views

app_name = 'parliamentary_dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/<int:id_deputado>/', views.perfil_parlamentar, name='perfil_parlamentar'),
    path('comparar/', views.comparar_deputados, name='comparar_deputados'),
    path('relatorios/', views.relatorios, name='relatorios'),
]
