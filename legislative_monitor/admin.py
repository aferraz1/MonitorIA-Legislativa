from django.contrib import admin
from .models import Deputado, Proposicao, Votacao, VotoDeputado, Discurso


@admin.register(Deputado)
class DeputadoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sigla_partido', 'uf_representacao', 'situacao']
    list_filter = ['sigla_partido', 'uf_representacao', 'situacao', 'sexo']
    search_fields = ['nome', 'nome_civil', 'email']
    ordering = ['nome']


@admin.register(Proposicao)
class ProposicaoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'numero', 'ano', 'autor', 'data_apresentacao', 'situacao']
    list_filter = ['tipo', 'situacao', 'ano']
    search_fields = ['ementa', 'numero']
    date_hierarchy = 'data_apresentacao'
    ordering = ['-data_apresentacao']


@admin.register(Votacao)
class VotacaoAdmin(admin.ModelAdmin):
    list_display = ['id_votacao', 'proposicao', 'data', 'aprovacao', 'votos_sim', 'votos_nao']
    list_filter = ['aprovacao', 'tipo_votacao']
    search_fields = ['descricao', 'id_votacao']
    date_hierarchy = 'data'
    ordering = ['-data']


@admin.register(VotoDeputado)
class VotoDeputadoAdmin(admin.ModelAdmin):
    list_display = ['deputado', 'votacao', 'voto', 'created_at']
    list_filter = ['voto']
    search_fields = ['deputado__nome']
    ordering = ['-created_at']


@admin.register(Discurso)
class DiscursoAdmin(admin.ModelAdmin):
    list_display = ['deputado', 'data', 'tipo_discurso']
    list_filter = ['tipo_discurso']
    search_fields = ['deputado__nome', 'transcricao', 'sumario']
    date_hierarchy = 'data'
    ordering = ['-data']

