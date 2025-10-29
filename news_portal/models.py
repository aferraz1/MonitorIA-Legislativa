from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from legislative_monitor.models import Proposicao, Deputado


class Categoria(models.Model):
    """Modelo para categorias de notícias"""
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    descricao = models.TextField(blank=True)
    cor = models.CharField(max_length=7, default='#007bff', help_text="Cor em formato hexadecimal")
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome


class Noticia(models.Model):
    """Modelo para notícias do portal"""
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('PUBLICADA', 'Publicada'),
        ('ARQUIVADA', 'Arquivada'),
    ]
    
    titulo = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    subtitulo = models.CharField(max_length=255, blank=True)
    conteudo = models.TextField()
    resumo = models.TextField(blank=True)
    
    # Relacionamentos
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='noticias')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='noticias')
    proposicoes = models.ManyToManyField(Proposicao, blank=True, related_name='noticias')
    deputados = models.ManyToManyField(Deputado, blank=True, related_name='noticias')
    
    # Mídia
    imagem_destaque = models.ImageField(upload_to='noticias/imagens/', blank=True, null=True)
    credito_imagem = models.CharField(max_length=255, blank=True)
    
    # Status e destaque
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RASCUNHO')
    destaque = models.BooleanField(default=False)
    
    # SEO
    meta_descricao = models.TextField(blank=True, max_length=160)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Estatísticas
    visualizacoes = models.IntegerField(default=0)
    
    # Datas
    data_publicacao = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-data_publicacao', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.titulo


class Tag(models.Model):
    """Modelo para tags de notícias"""
    nome = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    noticias = models.ManyToManyField(Noticia, related_name='tags', blank=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['nome']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome


class Comentario(models.Model):
    """Modelo para comentários em notícias"""
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_noticias')
    texto = models.TextField()
    aprovado = models.BooleanField(default=False)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.noticia.titulo}"

