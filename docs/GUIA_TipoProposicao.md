# Guia de Uso - Modelo TipoProposicao

## Visão Geral

O modelo **TipoProposicao** armazena informações sobre os tipos de proposições legislativas disponíveis na Câmara dos Deputados, obtidos através da API de Dados Abertos.

## Instalação e Configuração

### 1. Aplicar Migrations

Primeiro, aplique a migration para criar a tabela no banco de dados:

```bash
python manage.py migrate legislative_monitor
```

### 2. Sincronizar Dados

Execute o comando de sincronização para popular a tabela com os dados da API:

```bash
python manage.py sync_tipos_proposicao
```

**Saída esperada:**
```
Iniciando sincronização dos tipos de proposição...
Encontrados 542 tipos de proposição na API
✓ Criado: OF - Ofício do Congresso Nacional
✓ Criado: CON - Consulta
✓ Criado: EMC - Emenda na Comissão
...
============================================================
Sincronização concluída!
  • Tipos criados: 542
  • Tipos atualizados: 0
  • Total processado: 542
============================================================
```

## Uso no Django Admin

Após a sincronização, você pode gerenciar os tipos de proposição através do Django Admin:

1. Acesse `/admin/legislative_monitor/tipoproposicao/`
2. Visualize, pesquise e filtre os tipos de proposição
3. Os campos `created_at` e `updated_at` são somente leitura

## Uso Programático

### Consultar Tipos de Proposição

```python
from legislative_monitor.models import TipoProposicao

# Listar todos os tipos
tipos = TipoProposicao.objects.all()

# Buscar por sigla
pl = TipoProposicao.objects.filter(sigla='PL')

# Buscar por código
tipo = TipoProposicao.objects.get(cod='139')

# Buscar por nome (case-insensitive)
pec = TipoProposicao.objects.filter(nome__icontains='emenda')
```

### Exemplos de Tipos Comuns

```python
# Projeto de Lei
pl = TipoProposicao.objects.get(cod='139')
print(pl)  # Output: PL - Projeto de Lei

# Proposta de Emenda à Constituição
pec = TipoProposicao.objects.get(cod='136')
print(pec)  # Output: PEC - Proposta de Emenda à Constituição

# Projeto de Decreto Legislativo
pdc = TipoProposicao.objects.get(cod='135')
print(pdc)  # Output: PDC - Projeto de Decreto Legislativo

# Medida Provisória
mpv = TipoProposicao.objects.get(cod='146')
print(mpv)  # Output: MPV - Medida Provisória
```

### Integração com o Modelo Proposicao

**Opção 1: Consulta por sigla (atual)**

```python
from legislative_monitor.models import Proposicao, TipoProposicao

# Buscar proposições de um tipo específico
tipo_pl = TipoProposicao.objects.get(sigla='PL')
proposicoes_pl = Proposicao.objects.filter(tipo='PL')
```

**Opção 2: Adicionar ForeignKey (recomendado para futuro)**

Modificar o modelo `Proposicao` para usar ForeignKey:

```python
class Proposicao(models.Model):
    # ... outros campos ...
    tipo_proposicao = models.ForeignKey(
        TipoProposicao, 
        on_delete=models.PROTECT, 
        related_name='proposicoes'
    )
```

Isso permitiria consultas mais eficientes:

```python
# Buscar proposições de um tipo
tipo = TipoProposicao.objects.get(sigla='PL')
proposicoes = tipo.proposicoes.all()

# Acessar informações do tipo a partir da proposição
proposicao = Proposicao.objects.first()
print(proposicao.tipo_proposicao.nome)
print(proposicao.tipo_proposicao.descricao)
```

## API REST (se disponível)

Se o projeto tiver Django REST Framework configurado, você pode criar um endpoint:

```python
# serializers.py
from rest_framework import serializers
from .models import TipoProposicao

class TipoProposicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProposicao
        fields = ['id', 'cod', 'sigla', 'nome', 'descricao', 'created_at', 'updated_at']

# views.py
from rest_framework import viewsets
from .models import TipoProposicao
from .serializers import TipoProposicaoSerializer

class TipoProposicaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoProposicao.objects.all()
    serializer_class = TipoProposicaoSerializer
    filterset_fields = ['sigla', 'cod']
    search_fields = ['sigla', 'nome', 'descricao']

# urls.py
from rest_framework.routers import DefaultRouter
from .views import TipoProposicaoViewSet

router = DefaultRouter()
router.register(r'tipos-proposicao', TipoProposicaoViewSet)
```

## Sincronização Automática

Para manter os dados atualizados, você pode agendar a sincronização usando Celery Beat:

```python
# tasks.py
from celery import shared_task
from django.core.management import call_command

@shared_task
def sync_tipos_proposicao():
    """Tarefa Celery para sincronizar tipos de proposição"""
    call_command('sync_tipos_proposicao')

# celery.py (configuração do beat)
from celery.schedules import crontab

app.conf.beat_schedule = {
    'sync-tipos-proposicao-semanal': {
        'task': 'legislative_monitor.tasks.sync_tipos_proposicao',
        'schedule': crontab(day_of_week=1, hour=3, minute=0),  # Toda segunda-feira às 3h
    },
}
```

## Templates HTML

Exemplo de template para listar tipos de proposição:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h1>Tipos de Proposição</h1>
    
    <div class="row">
        {% for tipo in tipos %}
        <div class="col-md-4 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">
                        <span class="badge bg-primary">{{ tipo.sigla }}</span>
                    </h5>
                    <p class="card-text">{{ tipo.nome }}</p>
                    {% if tipo.descricao %}
                    <small class="text-muted">{{ tipo.descricao }}</small>
                    {% endif %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

## Consultas Úteis

### Contar tipos por sigla

```python
from django.db.models import Count

tipos_count = TipoProposicao.objects.values('sigla').annotate(
    total=Count('id')
).order_by('-total')

for item in tipos_count:
    print(f"{item['sigla']}: {item['total']} tipo(s)")
```

### Buscar tipos sem descrição

```python
tipos_sem_descricao = TipoProposicao.objects.filter(descricao='')
print(f"Total de tipos sem descrição: {tipos_sem_descricao.count()}")
```

### Tipos mais recentemente atualizados

```python
tipos_recentes = TipoProposicao.objects.order_by('-updated_at')[:10]
for tipo in tipos_recentes:
    print(f"{tipo.sigla} - Atualizado em: {tipo.updated_at}")
```

## Troubleshooting

### Erro ao sincronizar

Se houver erro na sincronização, verifique:

1. **Conexão com a API:**
   ```bash
   curl https://dadosabertos.camara.leg.br/api/v2/referencias/proposicoes/siglaTipo
   ```

2. **Configuração da URL base:**
   Verifique em `settings.py`:
   ```python
   CAMARA_API_BASE_URL = 'https://dadosabertos.camara.leg.br/api/v2'
   ```

3. **Logs de erro:**
   O comando exibe erros específicos para cada tipo que falhar

### Tipos duplicados

Alguns tipos podem ter a mesma sigla mas códigos diferentes. Isso é esperado e reflete a estrutura da API da Câmara. Use o campo `cod` como identificador único.

### Performance

Para melhorar a performance em consultas frequentes:

```python
# Use select_related ou prefetch_related quando apropriado
# Use índices (já configurados nos campos sigla e cod)
# Considere cache para listas que não mudam frequentemente

from django.core.cache import cache

def get_tipos_proposicao():
    tipos = cache.get('tipos_proposicao')
    if tipos is None:
        tipos = list(TipoProposicao.objects.all())
        cache.set('tipos_proposicao', tipos, 60*60*24)  # Cache por 24h
    return tipos
```

## Referências

- [API de Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br/swagger/api.html)
- [Documentação Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Management Commands](https://docs.djangoproject.com/en/stable/howto/custom-management-commands/)

---

**Última atualização:** 29/10/2025
