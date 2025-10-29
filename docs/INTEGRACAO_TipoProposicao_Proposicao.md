# Integração TipoProposicao com Proposicao

## Situação Atual

O modelo `Proposicao` atualmente utiliza um campo `CharField` com choices hardcoded para armazenar o tipo de proposição:

```python
class Proposicao(models.Model):
    TIPO_CHOICES = [
        ('PL', 'Projeto de Lei'),
        ('PLP', 'Projeto de Lei Complementar'),
        ('PEC', 'Proposta de Emenda à Constituição'),
        ('PDC', 'Projeto de Decreto Legislativo'),
        ('PRC', 'Projeto de Resolução'),
        ('MPV', 'Medida Provisória'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
```

**Limitações desta abordagem:**
- Apenas 6 tipos suportados (API tem 542 tipos)
- Manutenção manual necessária para adicionar novos tipos
- Sem acesso a informações detalhadas (código, descrição)
- Não reflete mudanças na API da Câmara automaticamente

## Proposta de Integração

### Opção 1: Adicionar ForeignKey (Recomendado)

Adicionar um novo campo `tipo_proposicao` como ForeignKey para `TipoProposicao`, mantendo o campo `tipo` existente para compatibilidade retroativa.

**Vantagens:**
- Não quebra código existente
- Permite migração gradual
- Acesso a todas as informações do tipo
- Sincronização automática com a API

**Implementação:**

```python
class Proposicao(models.Model):
    # ... campos existentes ...
    
    # Campo legado (manter por compatibilidade)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, blank=True)
    
    # Novo campo (recomendado)
    tipo_proposicao = models.ForeignKey(
        TipoProposicao,
        on_delete=models.PROTECT,
        related_name='proposicoes',
        null=True,
        blank=True,
        help_text="Tipo de proposição conforme API da Câmara"
    )
    
    def save(self, *args, **kwargs):
        # Sincronizar tipo legado com tipo_proposicao
        if self.tipo_proposicao and not self.tipo:
            self.tipo = self.tipo_proposicao.sigla
        super().save(*args, **kwargs)
```

**Migration necessária:**

```python
# legislative_monitor/migrations/0004_add_tipo_proposicao_fk.py
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legislative_monitor', '0003_tipoproposicao'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposicao',
            name='tipo_proposicao',
            field=models.ForeignKey(
                blank=True,
                help_text='Tipo de proposição conforme API da Câmara',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='proposicoes',
                to='legislative_monitor.tipoproposicao'
            ),
        ),
        migrations.AlterField(
            model_name='proposicao',
            name='tipo',
            field=models.CharField(blank=True, choices=[...], max_length=10),
        ),
    ]
```

**Script de migração de dados:**

```python
# legislative_monitor/management/commands/migrate_tipos_proposicao.py
from django.core.management.base import BaseCommand
from legislative_monitor.models import Proposicao, TipoProposicao


class Command(BaseCommand):
    help = 'Migra os tipos de proposição do campo legado para o novo campo ForeignKey'

    def handle(self, *args, **options):
        proposicoes = Proposicao.objects.filter(tipo_proposicao__isnull=True)
        total = proposicoes.count()
        
        self.stdout.write(f'Migrando {total} proposições...')
        
        migradas = 0
        erros = 0
        
        for proposicao in proposicoes:
            try:
                # Buscar tipo correspondente pela sigla
                tipo_obj = TipoProposicao.objects.filter(
                    sigla=proposicao.tipo
                ).first()
                
                if tipo_obj:
                    proposicao.tipo_proposicao = tipo_obj
                    proposicao.save()
                    migradas += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Tipo não encontrado: {proposicao.tipo} '
                            f'(Proposição {proposicao.id})'
                        )
                    )
                    erros += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Erro ao migrar proposição {proposicao.id}: {str(e)}'
                    )
                )
                erros += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\nMigração concluída!\n'
            f'  • Migradas: {migradas}\n'
            f'  • Erros: {erros}'
        ))
```

### Opção 2: Substituir Completamente (Não Recomendado)

Remover o campo `tipo` e usar apenas `tipo_proposicao`.

**Desvantagens:**
- Quebra código existente
- Requer refatoração de views, templates, etc.
- Migração de dados obrigatória

## Uso Após Integração

### Criar nova proposição

```python
from legislative_monitor.models import Proposicao, TipoProposicao

# Buscar o tipo
tipo_pl = TipoProposicao.objects.get(cod='139')  # PL

# Criar proposição
proposicao = Proposicao.objects.create(
    id_proposicao=123456,
    tipo_proposicao=tipo_pl,
    numero=1234,
    ano=2025,
    ementa="Dispõe sobre...",
    data_apresentacao="2025-01-15"
)
```

### Consultar proposições por tipo

```python
# Buscar todas as PECs
tipo_pec = TipoProposicao.objects.get(cod='136')
pecs = tipo_pec.proposicoes.all()

# Ou usando filter
pecs = Proposicao.objects.filter(tipo_proposicao__sigla='PEC')

# Acessar informações do tipo
for proposicao in pecs:
    print(f"{proposicao.tipo_proposicao.sigla} {proposicao.numero}/{proposicao.ano}")
    print(f"Descrição: {proposicao.tipo_proposicao.descricao}")
```

### Atualizar views

```python
# views.py
from django.views.generic import ListView
from .models import Proposicao, TipoProposicao

class ProposicaoListView(ListView):
    model = Proposicao
    template_name = 'legislative_monitor/proposicoes_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar tipos disponíveis para filtro
        context['tipos_disponiveis'] = TipoProposicao.objects.all()
        return context
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Filtrar por tipo se fornecido
        tipo_cod = self.request.GET.get('tipo')
        if tipo_cod:
            qs = qs.filter(tipo_proposicao__cod=tipo_cod)
        
        return qs.select_related('tipo_proposicao', 'autor')
```

### Atualizar templates

```html
<!-- proposicoes_list.html -->
<div class="filters">
    <label>Filtrar por tipo:</label>
    <select name="tipo" onchange="this.form.submit()">
        <option value="">Todos</option>
        {% for tipo in tipos_disponiveis %}
        <option value="{{ tipo.cod }}" {% if request.GET.tipo == tipo.cod %}selected{% endif %}>
            {{ tipo.sigla }} - {{ tipo.nome }}
        </option>
        {% endfor %}
    </select>
</div>

<table>
    <thead>
        <tr>
            <th>Tipo</th>
            <th>Número/Ano</th>
            <th>Ementa</th>
            <th>Autor</th>
        </tr>
    </thead>
    <tbody>
        {% for proposicao in object_list %}
        <tr>
            <td>
                <span class="badge" title="{{ proposicao.tipo_proposicao.descricao }}">
                    {{ proposicao.tipo_proposicao.sigla }}
                </span>
            </td>
            <td>{{ proposicao.numero }}/{{ proposicao.ano }}</td>
            <td>{{ proposicao.ementa|truncatewords:20 }}</td>
            <td>{{ proposicao.autor.nome }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

## Sincronização com API

Ao buscar proposições da API da Câmara, relacionar com TipoProposicao:

```python
# services/camara_api.py (atualizar método)
def buscar_proposicao(self, id_proposicao):
    """Busca uma proposição específica"""
    response = self._fazer_requisicao(f'proposicoes/{id_proposicao}')
    
    if response and 'dados' in response:
        dados = response['dados']
        
        # Buscar ou criar o tipo de proposição
        tipo_sigla = dados.get('siglaTipo', '')
        tipo_obj = None
        
        if tipo_sigla:
            tipo_obj = TipoProposicao.objects.filter(sigla=tipo_sigla).first()
        
        # Criar/atualizar proposição
        proposicao, created = Proposicao.objects.update_or_create(
            id_proposicao=dados['id'],
            defaults={
                'tipo_proposicao': tipo_obj,
                'tipo': tipo_sigla,  # Manter campo legado
                'numero': dados.get('numero'),
                'ano': dados.get('ano'),
                'ementa': dados.get('ementa', ''),
                # ... outros campos
            }
        )
        
        return proposicao
    
    return None
```

## Benefícios da Integração

1. **Flexibilidade:** Suporte a todos os 542 tipos da API
2. **Manutenção:** Sincronização automática, sem hardcoding
3. **Informação:** Acesso a código, nome completo e descrição
4. **Consultas:** Queries mais eficientes com select_related
5. **Filtros:** Filtros dinâmicos baseados em tipos reais
6. **Compatibilidade:** Mantém código legado funcionando

## Cronograma de Implementação

1. **Fase 1:** Adicionar campo `tipo_proposicao` (ForeignKey)
2. **Fase 2:** Criar migration e aplicar ao banco
3. **Fase 3:** Executar script de migração de dados
4. **Fase 4:** Atualizar views para usar novo campo
5. **Fase 5:** Atualizar templates com novos filtros
6. **Fase 6:** Atualizar serviços de API
7. **Fase 7:** (Futuro) Deprecar campo `tipo` legado

## Considerações

- Usar `on_delete=models.PROTECT` para evitar exclusão acidental de tipos em uso
- Manter campo `tipo` por um período de transição
- Documentar mudanças para outros desenvolvedores
- Criar testes para garantir compatibilidade

---

**Data:** 29/10/2025  
**Autor:** Alexandre Ferraz
