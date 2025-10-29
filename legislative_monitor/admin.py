from django.contrib import admin
from .models import Deputado, Proposicao, Votacao, VotoDeputado, Discurso, Regiao, Estado, Municipio, TipoProposicao


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


@admin.register(Regiao)
class RegiaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'sigla']
    search_fields = ['nome', 'sigla']
    ordering = ['id']


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'sigla', 'regiao']
    list_filter = ['regiao']
    search_fields = ['nome', 'sigla']
    ordering = ['nome']


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'estado', 'is_capital']
    list_filter = ['estado', 'is_capital']
    search_fields = ['nome']
    ordering = ['nome']



@admin.register(TipoProposicao)
class TipoProposicaoAdmin(admin.ModelAdmin):
    list_display = ['cod', 'sigla', 'nome', 'created_at']
    list_filter = ['sigla']
    search_fields = ['cod', 'sigla', 'nome', 'descricao']
    ordering = ['sigla', 'nome']
    readonly_fields = ['created_at', 'updated_at']
