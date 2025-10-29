# Changelog - Implementação do Modelo TipoProposicao

## Data: 29 de outubro de 2025

## Resumo

Foi implementado o modelo **TipoProposicao** no aplicativo `legislative_monitor` do projeto MonitorIA-Legislativa, permitindo o armazenamento e gerenciamento dos tipos de proposições legislativas disponíveis na API da Câmara dos Deputados.

## Alterações Realizadas

### 1. Modelo de Dados (`models.py`)

Foi criado o modelo `TipoProposicao` com os seguintes campos:

- **cod** (CharField): Código único do tipo de proposição na API da Câmara
- **sigla** (CharField): Sigla do tipo de proposição (ex: PL, PEC, PDC)
- **nome** (CharField): Nome completo do tipo de proposição
- **descricao** (TextField): Descrição detalhada do tipo de proposição
- **created_at** (DateTimeField): Data de criação do registro
- **updated_at** (DateTimeField): Data da última atualização

**Características:**
- Índices criados nos campos `sigla` e `cod` para otimização de consultas
- Ordenação padrão por sigla e nome
- Método `__str__()` retorna formato "SIGLA - Nome"

### 2. Interface Administrativa (`admin.py`)

Foi criada a classe `TipoProposicaoAdmin` com as seguintes configurações:

- **list_display**: Exibe cod, sigla, nome e data de criação
- **list_filter**: Permite filtrar por sigla
- **search_fields**: Busca por cod, sigla, nome e descrição
- **ordering**: Ordenação por sigla e nome
- **readonly_fields**: Campos created_at e updated_at como somente leitura

### 3. Migration (`0003_tipoproposicao.py`)

Foi gerada a migration que cria a tabela do modelo TipoProposicao no banco de dados com todos os campos, índices e constraints necessários.

### 4. Serviço de API (`camara_api.py`)

Foi adicionado o método `listar_tipos_proposicao()` na classe `CamaraAPIService` para consumir o endpoint da API da Câmara:

```
GET https://dadosabertos.camara.leg.br/api/v2/referencias/proposicoes/siglaTipo
```

### 5. Comando de Sincronização (`sync_tipos_proposicao.py`)

Foi criado o comando de gerenciamento Django `sync_tipos_proposicao` que:

- Consulta a API da Câmara dos Deputados
- Sincroniza todos os tipos de proposição disponíveis
- Cria novos registros ou atualiza existentes
- Exibe relatório detalhado da sincronização com estatísticas

**Uso:**
```bash
python manage.py sync_tipos_proposicao
```

## Estrutura de Dados da API

A API retorna os tipos de proposição no seguinte formato JSON:

```json
{
  "dados": [
    {
      "cod": "139",
      "sigla": "PL",
      "nome": "Projeto de Lei",
      "descricao": "Projeto de Lei"
    },
    {
      "cod": "136",
      "sigla": "PEC",
      "nome": "Proposta de Emenda à Constituição",
      "descricao": "Proposta de Emenda à Constituição (Art. 60 CF c/c art. 201 a 203, RICD)"
    }
  ]
}
```

**Total de tipos disponíveis na API:** 542

## Arquivos Modificados

1. `/legislative_monitor/models.py` - Adicionado modelo TipoProposicao
2. `/legislative_monitor/admin.py` - Adicionado TipoProposicaoAdmin
3. `/legislative_monitor/services/camara_api.py` - Adicionado método listar_tipos_proposicao()
4. `/legislative_monitor/migrations/0003_tipoproposicao.py` - Nova migration criada

## Arquivos Criados

1. `/legislative_monitor/management/commands/sync_tipos_proposicao.py` - Comando de sincronização

## Próximos Passos Recomendados

1. **Executar a migration:**
   ```bash
   python manage.py migrate legislative_monitor
   ```

2. **Sincronizar os tipos de proposição:**
   ```bash
   python manage.py sync_tipos_proposicao
   ```

3. **Relacionar com o modelo Proposicao:**
   Considerar adicionar uma ForeignKey no modelo `Proposicao` para referenciar `TipoProposicao`, substituindo o campo `tipo` atual (CharField com choices) por uma relação com a tabela de tipos.

4. **Criar views e templates:**
   Implementar views para listar e visualizar os tipos de proposição no frontend.

5. **Adicionar testes:**
   Criar testes unitários para o modelo e o comando de sincronização.

6. **Documentação da API:**
   Se houver uma API REST no projeto, adicionar endpoints para consulta dos tipos de proposição.

## Benefícios da Implementação

1. **Dados sempre atualizados:** Sincronização automática com a fonte oficial da Câmara
2. **Facilidade de manutenção:** Não é necessário manter lista hardcoded de tipos
3. **Flexibilidade:** Suporte a todos os 542 tipos de proposição existentes
4. **Integridade:** Uso de chave única (cod) garante consistência dos dados
5. **Performance:** Índices otimizam consultas por sigla e código
6. **Rastreabilidade:** Campos de auditoria (created_at, updated_at)

## Observações

- O modelo foi projetado para ser compatível com a estrutura atual do projeto
- A sincronização pode ser agendada usando Celery Beat para manter os dados atualizados
- O campo `descricao` pode estar vazio para alguns tipos de proposição na API
- Existem tipos de proposição com a mesma sigla mas códigos diferentes (ex: múltiplos tipos com sigla "REQ")

## Autor

**ALEXANDRE FERRAZ**  
Assessor Técnico Legislativo  
Alexandre.ferraz@camara.leg.br

---

**Brasília-DF, 29/10/2025**
