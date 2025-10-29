from django.db import models
from django.utils import timezone


class Deputado(models.Model):
    """Modelo para representar um deputado federal"""
    id_deputado = models.IntegerField(unique=True, help_text="ID do deputado na API da Câmara")
    nome = models.CharField(max_length=255)
    nome_civil = models.CharField(max_length=255, blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    sexo = models.CharField(max_length=1, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    municipio_nascimento = models.CharField(max_length=255, blank=True)
    uf_nascimento = models.CharField(max_length=2, blank=True)
    
    # Dados políticos
    sigla_partido = models.CharField(max_length=20)
    uf_representacao = models.CharField(max_length=2)
    situacao = models.CharField(max_length=50, blank=True)
    condicao_eleitoral = models.CharField(max_length=100, blank=True)
    
    # Contatos
    email = models.EmailField(blank=True)
    url_website = models.URLField(blank=True)
    url_foto = models.URLField(blank=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Deputado"
        verbose_name_plural = "Deputados"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.sigla_partido}/{self.uf_representacao}"


class Proposicao(models.Model):
    """Modelo para representar uma proposição legislativa"""
    TIPO_CHOICES = [
        ('PL', 'Projeto de Lei'),
        ('PLP', 'Projeto de Lei Complementar'),
        ('PEC', 'Proposta de Emenda à Constituição'),
        ('PDC', 'Projeto de Decreto Legislativo'),
        ('PRC', 'Projeto de Resolução'),
        ('MPV', 'Medida Provisória'),
    ]
    
    SITUACAO_CHOICES = [
        ('EM_TRAMITACAO', 'Em Tramitação'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada'),
        ('ARQUIVADA', 'Arquivada'),
        ('RETIRADA', 'Retirada'),
    ]
    
    id_proposicao = models.IntegerField(unique=True, help_text="ID da proposição na API da Câmara")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    numero = models.IntegerField()
    ano = models.IntegerField()
    ementa = models.TextField()
    ementa_detalhada = models.TextField(blank=True)
    
    data_apresentacao = models.DateField()
    situacao = models.CharField(max_length=50, choices=SITUACAO_CHOICES, default='EM_TRAMITACAO')
    status_proposicao = models.TextField(blank=True)
    
    # Autoria
    autor = models.ForeignKey(Deputado, on_delete=models.SET_NULL, null=True, blank=True, related_name='proposicoes')
    
    # URLs
    url_inteiro_teor = models.URLField(blank=True)
    url_tramitacao = models.URLField(blank=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Proposição"
        verbose_name_plural = "Proposições"
        ordering = ['-data_apresentacao']
    
    def __str__(self):
        return f"{self.tipo} {self.numero}/{self.ano}"


class Votacao(models.Model):
    """Modelo para representar uma votação"""
    id_votacao = models.CharField(max_length=100, unique=True)
    proposicao = models.ForeignKey(Proposicao, on_delete=models.CASCADE, related_name='votacoes')
    
    data = models.DateTimeField()
    descricao = models.TextField()
    tipo_votacao = models.CharField(max_length=100)
    
    aprovacao = models.BooleanField(null=True, blank=True)
    votos_sim = models.IntegerField(default=0)
    votos_nao = models.IntegerField(default=0)
    votos_abstencao = models.IntegerField(default=0)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Votação"
        verbose_name_plural = "Votações"
        ordering = ['-data']
    
    def __str__(self):
        return f"Votação {self.id_votacao} - {self.data.strftime('%d/%m/%Y')}"


class VotoDeputado(models.Model):
    """Modelo para representar o voto individual de um deputado"""
    VOTO_CHOICES = [
        ('SIM', 'Sim'),
        ('NAO', 'Não'),
        ('ABSTENCAO', 'Abstenção'),
        ('OBSTRUCAO', 'Obstrução'),
        ('AUSENTE', 'Ausente'),
    ]
    
    votacao = models.ForeignKey(Votacao, on_delete=models.CASCADE, related_name='votos')
    deputado = models.ForeignKey(Deputado, on_delete=models.CASCADE, related_name='votos')
    voto = models.CharField(max_length=20, choices=VOTO_CHOICES)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Voto do Deputado"
        verbose_name_plural = "Votos dos Deputados"
        unique_together = ['votacao', 'deputado']
    
    def __str__(self):
        return f"{self.deputado.nome} - {self.voto}"


class Discurso(models.Model):
    """Modelo para representar um discurso de deputado"""
    id_discurso = models.CharField(max_length=100, unique=True)
    deputado = models.ForeignKey(Deputado, on_delete=models.CASCADE, related_name='discursos')
    
    data = models.DateTimeField()
    tipo_discurso = models.CharField(max_length=100)
    transcricao = models.TextField()
    sumario = models.TextField(blank=True)
    
    # URLs
    url_audio = models.URLField(blank=True)
    url_video = models.URLField(blank=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Discurso"
        verbose_name_plural = "Discursos"
        ordering = ['-data']
    
    def __str__(self):
        return f"Discurso de {self.deputado.nome} em {self.data.strftime('%d/%m/%Y')}"

