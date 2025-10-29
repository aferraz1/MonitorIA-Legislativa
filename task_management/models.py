from django.db import models
from django.contrib.auth.models import User
from legislative_monitor.models import Proposicao


class Equipe(models.Model):
    """Modelo para representar uma equipe de trabalho"""
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    membros = models.ManyToManyField(User, related_name='equipes')
    coordenador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='equipes_coordenadas')
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipes"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Tarefa(models.Model):
    """Modelo para representar uma tarefa no workflow"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('EM_REVISAO', 'Em Revisão'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]
    
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='MEDIA')
    
    # Relacionamentos
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='tarefas')
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tarefas_responsaveis')
    criada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tarefas_criadas')
    proposicao = models.ForeignKey(Proposicao, on_delete=models.SET_NULL, null=True, blank=True, related_name='tarefas')
    
    # Prazos
    data_inicio = models.DateField(null=True, blank=True)
    data_fim_prevista = models.DateField(null=True, blank=True)
    data_conclusao = models.DateField(null=True, blank=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ['-prioridade', '-created_at']
    
    def __str__(self):
        return f"{self.titulo} - {self.status}"


class Comentario(models.Model):
    """Modelo para comentários em tarefas"""
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_tarefas')
    texto = models.TextField()
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.tarefa.titulo}"


class Anexo(models.Model):
    """Modelo para anexos em tarefas"""
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='tarefas/anexos/')
    nome_arquivo = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
        ordering = ['created_at']
    
    def __str__(self):
        return self.nome_arquivo

