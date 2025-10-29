from django.db import models
from django.utils.text import slugify
import os
from openai import OpenAI


class Sexo(models.Model):
    """Modelo para representar o sexo/gênero com descrição gerada por IA"""
    sigla = models.CharField(
        max_length=2,
        unique=True,
        help_text="Sigla do sexo (ex: M, F, NB)"
    )
    nome = models.CharField(
        max_length=100,
        help_text="Nome completo do sexo/gênero"
    )
    descricao = models.TextField(
        max_length=500,
        blank=True,
        help_text="Descrição gerada automaticamente por IA"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Slug gerado automaticamente a partir do nome"
    )
    
    # Campo auxiliar para detectar mudanças significativas no nome
    _nome_anterior = models.CharField(
        max_length=100,
        blank=True,
        editable=False,
        help_text="Nome anterior para detectar mudanças"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Sexo"
        verbose_name_plural = "Sexos"
        ordering = ['sigla']
    
    def __str__(self):
        return f"{self.sigla} - {self.nome}"
    
    def _gerar_slug(self):
        """Gera slug a partir do nome usando slugify"""
        if not self.slug or self.nome != self._nome_anterior:
            base_slug = slugify(self.nome, allow_unicode=False)
            slug = base_slug
            counter = 1
            
            # Garantir que o slug seja único
            while Sexo.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
    
    def _nome_mudou_significativamente(self):
        """
        Verifica se o nome mudou significativamente.
        Considera mudança significativa se:
        - Nome anterior está vazio (primeiro save)
        - Diferença de mais de 30% nas palavras
        - Mudança nas palavras-chave principais
        """
        if not self._nome_anterior:
            return True
        
        # Normalizar e comparar
        nome_atual = self.nome.lower().strip()
        nome_anterior = self._nome_anterior.lower().strip()
        
        if nome_atual == nome_anterior:
            return False
        
        # Dividir em palavras
        palavras_atual = set(nome_atual.split())
        palavras_anterior = set(nome_anterior.split())
        
        # Calcular diferença (Jaccard distance)
        if not palavras_anterior:
            return True
        
        intersecao = palavras_atual & palavras_anterior
        uniao = palavras_atual | palavras_anterior
        
        similaridade = len(intersecao) / len(uniao) if uniao else 0
        
        # Se similaridade for menor que 70%, considera mudança significativa
        return similaridade < 0.7
    
    def _gerar_descricao_ia(self):
        """
        Gera descrição usando IA (OpenAI GPT).
        Só é chamado se o nome mudou significativamente.
        """
        try:
            # Verificar se a API key está disponível
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                self.descricao = f"Descrição de {self.nome} (API key não configurada)"
                return
            
            # Criar cliente OpenAI
            client = OpenAI()
            
            # Prompt para gerar descrição
            prompt = f"""Escreva uma definição técnica e objetiva sobre o conceito de "{self.nome}" 
no contexto de identificação de gênero/sexo em registros oficiais e sistemas de informação.

A definição deve:
- Ter no máximo 500 caracteres
- Ser formal e técnica
- Ser adequada para uso em sistemas governamentais
- Evitar linguagem discriminatória
- Focar no aspecto de identificação e classificação

Responda apenas com a definição, sem introduções ou explicações adicionais."""
            
            # Chamar API
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Você é um especialista em terminologia técnica para sistemas de informação governamentais."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            # Extrair descrição
            descricao = response.choices[0].message.content.strip()
            
            # Garantir que não exceda 500 caracteres
            if len(descricao) > 500:
                descricao = descricao[:497] + "..."
            
            self.descricao = descricao
            
        except Exception as e:
            # Em caso de erro, usar descrição padrão
            self.descricao = f"Classificação de sexo/gênero: {self.nome}. (Erro ao gerar descrição: {str(e)[:100]})"
    
    def save(self, *args, **kwargs):
        """
        Override do método save para:
        1. Gerar slug automaticamente
        2. Gerar descrição por IA se necessário
        3. Atualizar nome anterior
        """
        # Gerar slug
        self._gerar_slug()
        
        # Gerar descrição por IA se nome mudou significativamente
        if self._nome_mudou_significativamente():
            self._gerar_descricao_ia()
        
        # Salvar
        super().save(*args, **kwargs)
        
        # Atualizar nome anterior para próxima comparação
        if self.nome != self._nome_anterior:
            Sexo.objects.filter(pk=self.pk).update(_nome_anterior=self.nome)
