from django.contrib import admin
from .models import ResumoIA, AnaliseImpacto, BuscaSemantica, AnaliseDiscurso


@admin.register(ResumoIA)
class ResumoIAAdmin(admin.ModelAdmin):
    list_display = ['proposicao', 'modelo_ia', 'created_at']
    list_filter = ['modelo_ia']
    search_fields = ['proposicao__ementa', 'resumo']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(AnaliseImpacto)
class AnaliseImpactoAdmin(admin.ModelAdmin):
    list_display = ['proposicao', 'nivel_impacto', 'modelo_ia', 'created_at']
    list_filter = ['nivel_impacto', 'modelo_ia']
    search_fields = ['proposicao__ementa', 'descricao_impacto']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(BuscaSemantica)
class BuscaSemanticaAdmin(admin.ModelAdmin):
    list_display = ['proposicao', 'modelo_embedding', 'created_at']
    list_filter = ['modelo_embedding']
    search_fields = ['proposicao__ementa', 'texto_indexado']
    ordering = ['-created_at']


@admin.register(AnaliseDiscurso)
class AnaliseDiscursoAdmin(admin.ModelAdmin):
    list_display = ['discurso', 'sentimento', 'modelo_ia', 'created_at']
    list_filter = ['sentimento', 'modelo_ia']
    search_fields = ['discurso__deputado__nome', 'resumo']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

