from django.contrib import admin
from .models import PerfilParlamentar, RelatorioAtividade, ComparativoDeputados


@admin.register(PerfilParlamentar)
class PerfilParlamentarAdmin(admin.ModelAdmin):
    list_display = ['deputado', 'total_votacoes', 'presenca_votacoes', 'total_proposicoes', 'total_discursos']
    search_fields = ['deputado__nome']
    ordering = ['deputado__nome']


@admin.register(RelatorioAtividade)
class RelatorioAtividadeAdmin(admin.ModelAdmin):
    list_display = ['deputado', 'periodo', 'data_inicio', 'data_fim', 'proposicoes_apresentadas']
    list_filter = ['periodo']
    search_fields = ['deputado__nome']
    date_hierarchy = 'data_fim'
    ordering = ['-data_fim']


@admin.register(ComparativoDeputados)
class ComparativoDeputadosAdmin(admin.ModelAdmin):
    list_display = ['nome', 'created_at']
    search_fields = ['nome', 'descricao']
    filter_horizontal = ['deputados']
    ordering = ['-created_at']

