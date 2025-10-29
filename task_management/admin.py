from django.contrib import admin
from .models import Equipe, Tarefa, Comentario, Anexo


@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'coordenador', 'created_at']
    search_fields = ['nome', 'descricao']
    filter_horizontal = ['membros']
    ordering = ['nome']


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'equipe', 'responsavel', 'status', 'prioridade', 'data_fim_prevista']
    list_filter = ['status', 'prioridade', 'equipe']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['tarefa', 'autor', 'created_at']
    search_fields = ['texto', 'tarefa__titulo']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ['nome_arquivo', 'tarefa', 'uploaded_by', 'created_at']
    search_fields = ['nome_arquivo', 'tarefa__titulo']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

