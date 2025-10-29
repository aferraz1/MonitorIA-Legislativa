from django.db import models
from legislative_monitor.models import Deputado, Proposicao, Votacao, Discurso


class PerfilParlamentar(models.Model):
    """Modelo para perfil analítico de parlamentar"""
    deputado = models.OneToOneField(Deputado, on_delete=models.CASCADE, related_name='perfil')
    
    # Estatísticas de votação
    total_votacoes = models.IntegerField(default=0)
    presenca_votacoes = models.FloatField(default=0.0, help_text="Percentual de presença")
    votos_sim = models.IntegerField(default=0)
    votos_nao = models.IntegerField(default=0)
    votos_abstencao = models.IntegerField(default=0)
    
    # Estatísticas de proposições
    total_proposicoes = models.IntegerField(default=0)
    proposicoes_aprovadas = models.IntegerField(default=0)
    proposicoes_em_tramitacao = models.IntegerField(default=0)
    
    # Estatísticas de discursos
    total_discursos = models.IntegerField(default=0)
    tempo_total_discurso = models.IntegerField(default=0, help_text="Tempo em minutos")
    
    # Análise de atuação
    areas_atuacao = models.JSONField(default=list, help_text="Áreas temáticas de atuação")
    temas_frequentes = models.JSONField(default=list, help_text="Temas mais abordados")
    
    # Metadados
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Perfil Parlamentar"
        verbose_name_plural = "Perfis Parlamentares"
    
    def __str__(self):
        return f"Perfil de {self.deputado.nome}"


class RelatorioAtividade(models.Model):
    """Modelo para relatórios periódicos de atividade parlamentar"""
    PERIODO_CHOICES = [
        ('SEMANAL', 'Semanal'),
        ('MENSAL', 'Mensal'),
        ('TRIMESTRAL', 'Trimestral'),
        ('ANUAL', 'Anual'),
    ]
    
    deputado = models.ForeignKey(Deputado, on_delete=models.CASCADE, related_name='relatorios')
    periodo = models.CharField(max_length=20, choices=PERIODO_CHOICES)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    
    # Atividades no período
    proposicoes_apresentadas = models.IntegerField(default=0)
    votacoes_participadas = models.IntegerField(default=0)
    discursos_realizados = models.IntegerField(default=0)
    
    # Análise
    principais_atuacoes = models.JSONField(default=list)
    destaque_periodo = models.TextField(blank=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Relatório de Atividade"
        verbose_name_plural = "Relatórios de Atividades"
        ordering = ['-data_fim']
    
    def __str__(self):
        return f"{self.deputado.nome} - {self.periodo} ({self.data_inicio} a {self.data_fim})"


class ComparativoDeputados(models.Model):
    """Modelo para comparações entre deputados"""
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    deputados = models.ManyToManyField(Deputado, related_name='comparativos')
    
    # Critérios de comparação
    criterios = models.JSONField(default=list)
    resultados = models.JSONField(default=dict)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comparativo de Deputados"
        verbose_name_plural = "Comparativos de Deputados"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nome

