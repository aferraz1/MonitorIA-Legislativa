from django.db import models
from django.utils import timezone


class Deputado(models.Model):
    """Modelo para representar um deputado federal"""
    id_deputado = models.IntegerField(unique=True, help_text="ID do deputado na API da Câmara")
    nome = models.CharField(max_length=255)
    nome_civil = models.CharField(max_length=255, blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    
    # Sexo (relacionamento com modelo Sexo)
    sexo = models.ForeignKey(
        'Sexo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deputados',
        help_text="Sexo/gênero do deputado"
    )
    
    data_nascimento = models.DateField(null=True, blank=True)
    
    # Município de nascimento (relacionamento com modelo Municipio)
    municipio_nascimento = models.ForeignKey(
        'Municipio',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deputados_nascidos',
        help_text="Município de nascimento do deputado"
    )
    
    # UF de nascimento (relacionamento com modelo Estado)
    uf_nascimento = models.ForeignKey(
        'Estado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deputados_nascidos',
        help_text="Estado de nascimento do deputado"
    )
    
    # Dados políticos
    sigla_partido = models.CharField(max_length=20)
    
    # UF de representação (relacionamento com modelo Estado)
    uf_representacao = models.ForeignKey(
        'Estado',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='deputados_representantes',
        help_text="Estado de representação do deputado"
    )
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
        uf = self.uf_representacao.sigla if self.uf_representacao else ''
        return f"{self.nome} - {self.sigla_partido}/{uf}"


class Proposicao(models.Model):
    """Modelo para representar uma proposição legislativa"""
    SITUACAO_CHOICES = [
        ('EM_TRAMITACAO', 'Em Tramitação'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada'),
        ('ARQUIVADA', 'Arquivada'),
        ('RETIRADA', 'Retirada'),
    ]
    
    id_proposicao = models.IntegerField(unique=True, help_text="ID da proposição na API da Câmara")
    
    # Tipo de proposição (relacionamento com TipoProposicao)
    tipo = models.ForeignKey(
        'TipoProposicao',
        on_delete=models.PROTECT,
        related_name='proposicoes',
        null=True,
        blank=True,
        help_text='Tipo de proposição conforme API da Câmara'
    )
    
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
        tipo_str = self.tipo.sigla if self.tipo else ''
        return f"{tipo_str} {self.numero}/{self.ano}"


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


class Regiao(models.Model):
    """Modelo para representar uma região brasileira (dados do IBGE)"""
    id = models.PositiveIntegerField(primary_key=True, help_text="Código do IBGE da Região")
    sigla = models.CharField(max_length=2, unique=True, help_text="Sigla da Região")
    nome = models.CharField(max_length=100, help_text="Nome da Região")
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Região"
        verbose_name_plural = "Regiões"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Estado(models.Model):
    """Modelo para representar um estado brasileiro (dados do IBGE)"""
    id = models.PositiveIntegerField(primary_key=True, help_text="Código do IBGE do Estado")
    sigla = models.CharField(max_length=2, unique=True, help_text="Sigla do Estado")
    nome = models.CharField(max_length=100, help_text="Nome do Estado")
    regiao = models.ForeignKey(Regiao, on_delete=models.PROTECT, related_name='estados', help_text="Região do Estado")
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Municipio(models.Model):
    """Modelo para representar um município brasileiro (dados do IBGE)"""
    id = models.PositiveIntegerField(primary_key=True, help_text="Código do IBGE do Município")
    nome = models.CharField(max_length=100, help_text="Nome do Município")
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='municipios', help_text="Estado do Município")
    is_capital = models.BooleanField(default=False, help_text="Indica se o município é a capital do Estado")
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Município"
        verbose_name_plural = "Municípios"
        ordering = ['nome']
        # Garantir que cada Estado tem apenas uma capital
        constraints = [
            models.UniqueConstraint(
                fields=['estado'],
                condition=models.Q(is_capital=True),
                name='unique_capital_per_state'
            )
        ]
    
    def __str__(self):
        capital_marker = " (Capital)" if self.is_capital else ""
        return f"{self.nome}/{self.estado.sigla}{capital_marker}"


class TipoProposicao(models.Model):
    """Modelo para representar um tipo de proposição legislativa (dados da API da Câmara)"""
    cod = models.CharField(max_length=10, unique=True, help_text="Código do tipo de proposição na API da Câmara")
    sigla = models.CharField(max_length=20, db_index=True, help_text="Sigla do tipo de proposição")
    nome = models.CharField(max_length=255, help_text="Nome completo do tipo de proposição")
    descricao = models.TextField(blank=True, help_text="Descrição detalhada do tipo de proposição")
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tipo de Proposição"
        verbose_name_plural = "Tipos de Proposição"
        ordering = ['sigla', 'nome']
        indexes = [
            models.Index(fields=['sigla']),
            models.Index(fields=['cod']),
        ]
    
    def __str__(self):
        return f"{self.sigla} - {self.nome}"


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
        from django.utils.text import slugify
        
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
        import os
        from openai import OpenAI
        
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
