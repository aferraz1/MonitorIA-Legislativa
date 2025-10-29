from django.urls import path
from . import views

app_name = 'task_management'

urlpatterns = [
    path('', views.index, name='index'),
    path('tarefas/', views.listar_tarefas, name='tarefas_list'),
    path('tarefas/<int:pk>/', views.detalhe_tarefa, name='tarefa_detail'),
    path('equipes/', views.minhas_equipes, name='minhas_equipes'),
    path('equipes/<int:pk>/', views.detalhe_equipe, name='equipe_detail'),
]
