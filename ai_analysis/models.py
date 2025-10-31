from django.db import models
from legislative_monitor.models import Proposicao, Deputado, Discurso


class ResumoIA(models.Model):
    """Modelo para armazenar resumos gerados por IA"""
    proposicao = models.ForeignKey(Proposicao, on_delete=models.CASCADE, related_name='resumos_ia')
    
    resumo = models.TextField()
    resumo_executivo = models.TextField(blank=True)
    principais_pontos = models.JSONField(default=list)
    
    # Metadados
    modelo_ia = models.CharField(max_length=100, default='gpt-4o-mini')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Resumo IA"
        verbose_name_plural = "Resumos IA"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Resumo IA de {self.proposicao}"


class AnaliseImpacto(models.Model):
    """Modelo para análise de impacto de proposições"""
    NIVEL_IMPACTO_CHOICES = [
        ('BAIXO', 'Baixo'),
        ('MEDIO', 'Médio'),
        ('ALTO', 'Alto'),
        ('CRITICO', 'Crítico'),
    ]
    
    proposicao = models.ForeignKey(Proposicao, on_delete=models.CASCADE, related_name='analises_impacto')
    
    nivel_impacto = models.CharField(max_length=20, choices=NIVEL_IMPACTO_CHOICES)
    descricao_impacto = models.TextField()
    areas_afetadas = models.JSONField(default=list)
    stakeholders = models.JSONField(default=list)
    
    # Impactos específicos
    impacto_economico = models.TextField(blank=True)
    impacto_social = models.TextField(blank=True)
    impacto_ambiental = models.TextField(blank=True)
    impacto_juridico = models.TextField(blank=True)
    
    # Metadados
    modelo_ia = models.CharField(max_length=100, default='gpt-4o-mini')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Análise de Impacto"
        verbose_name_plural = "Análises de Impacto"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Análise de {self.proposicao} - Impacto {self.nivel_impacto}"


class BuscaSemantica(models.Model):
    """Modelo para armazenar embeddings para busca semântica"""
    proposicao = models.OneToOneField(Proposicao, on_delete=models.CASCADE, related_name='embedding_semantico')
    
    embedding = models.JSONField(help_text="Vetor de embedding para busca semântica")
    texto_indexado = models.TextField()
    
    # Metadados
    modelo_embedding = models.CharField(max_length=100, default='text-embedding-ada-002')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Busca Semântica"
        verbose_name_plural = "Buscas Semânticas"
    
    def __str__(self):
        return f"Embedding de {self.proposicao}"


class AnaliseDiscurso(models.Model):
    """Modelo para análise de discursos por IA"""
    discurso = models.ForeignKey(Discurso, on_delete=models.CASCADE, related_name='analises_ia')
    
    sentimento = models.CharField(max_length=50, blank=True)
    temas_principais = models.JSONField(default=list)
    entidades_mencionadas = models.JSONField(default=list)
    resumo = models.TextField(blank=True)
    
    # Metadados
    modelo_ia = models.CharField(max_length=100, default='gpt-4o-mini')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Análise de Discurso"
        verbose_name_plural = "Análises de Discursos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Análise de discurso - {self.discurso}"

