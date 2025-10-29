from django.contrib import admin
from .models import Categoria, Noticia, Tag, Comentario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'cor']
    search_fields = ['nome', 'descricao']
    prepopulated_fields = {'slug': ('nome',)}
    ordering = ['nome']


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'autor', 'status', 'destaque', 'data_publicacao', 'visualizacoes']
    list_filter = ['status', 'destaque', 'categoria', 'data_publicacao']
    search_fields = ['titulo', 'conteudo', 'resumo']
    prepopulated_fields = {'slug': ('titulo',)}
    filter_horizontal = ['proposicoes', 'deputados']
    date_hierarchy = 'data_publicacao'
    ordering = ['-data_publicacao']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    search_fields = ['nome']
    prepopulated_fields = {'slug': ('nome',)}
    ordering = ['nome']


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['noticia', 'autor', 'aprovado', 'created_at']
    list_filter = ['aprovado']
    search_fields = ['texto', 'noticia__titulo']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

