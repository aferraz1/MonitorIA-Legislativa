# MonitorIA Legislativa

Portal do Sistema de Análise e Acompanhamento do Processo Legislativo

## Descrição

MonitorIA Legislativa é um sistema completo de monitoramento e análise do processo legislativo brasileiro, com foco na Câmara dos Deputados. O sistema utiliza inteligência artificial para análise de proposições, discursos e votações, fornecendo insights valiosos sobre a atividade parlamentar.

## Funcionalidades

1. **Monitoramento Automático de Dados Legislativos**
   - Integração com API de Dados Abertos da Câmara dos Deputados
   - Sincronização automática de proposições, votações e discursos
   - Atualização em tempo real de informações parlamentares

2. **Análise com Inteligência Artificial**
   - Resumos automáticos de proposições legislativas
   - Análise de impacto de proposições
   - Busca semântica inteligente
   - Análise de sentimento em discursos
   - Extração de temas e entidades

3. **Dashboard de Perfil Parlamentar**
   - Estatísticas de votação e presença
   - Histórico de proposições apresentadas
   - Análise de discursos e posicionamentos
   - Comparação entre deputados
   - Relatórios de atividade periódicos

4. **Gestão de Tarefas e Workflow**
   - Criação e atribuição de tarefas
   - Gerenciamento de equipes
   - Comentários e anexos em tarefas
   - Diferentes níveis de prioridade
   - Acompanhamento de status

5. **Portal de Notícias Categorizado**
   - Publicação de notícias sobre o processo legislativo
   - Sistema de categorias e tags
   - Relacionamento com proposições e deputados
   - Destaque de notícias principais
   - Sistema de comentários

## Stack Tecnológico

### Backend

- **Django 4.2**: Framework web Python
- **PostgreSQL**: Banco de dados relacional (com fallback para SQLite em desenvolvimento)
- **Django REST Framework**: API REST
- **OpenAI API**: Integração com modelos de linguagem (GPT-3.5/GPT-4)
- **Celery**: Processamento assíncrono de tarefas
- **Redis**: Cache e broker para Celery

### Frontend

- **HTML5**: Estrutura das páginas
- **CSS3**: Estilização
- **Bootstrap 5**: Framework CSS responsivo
- **JavaScript**: Interatividade
- **jQuery**: Manipulação do DOM e AJAX
- **Chart.js**: Visualização de dados (opcional)

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL (opcional, pode usar SQLite em desenvolvimento)
- Redis (opcional, para Celery)

### Passo a Passo

1. Clone o repositório:

```bash
git clone https://github.com/aferraz1/MonitorIA-Legislativa.git
cd MonitorIA-Legislativa
```

1. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

1. Configure as variáveis de ambiente:

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

1. Execute as migrações:

```bash
python manage.py migrate
```

1. Crie um superusuário:

```bash
python manage.py createsuperuser
```

1. Colete arquivos estáticos:

```bash
python manage.py collectstatic --noinput
```

1. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

1. Acesse o sistema em: <http://localhost:8000>

## Configuração

### Variáveis de Ambiente

Edite o arquivo `.env` com as seguintes configurações:

```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=*

# Database (PostgreSQL)
DB_NAME=monitoria_legislativa
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Use SQLite em desenvolvimento
USE_SQLITE=True

# OpenAI API (opcional, para funcionalidades de IA)
OPENAI_API_KEY=sua-chave-api-openai

# Celery (opcional, para processamento assíncrono)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### API da Câmara dos Deputados

O sistema está configurado para consumir a API de Dados Abertos da Câmara dos Deputados:

- Base URL: <https://dadosabertos.camara.leg.br/api/v2>
- Documentação: <https://dadosabertos.camara.leg.br/swagger/api.html>

## Estrutura do Projeto

```
MonitorIA-Legislativa/
├── monitoria_legislativa/       # Configurações do projeto Django
├── legislative_monitor/         # App de monitoramento legislativo
│   ├── models.py               # Modelos: Deputado, Proposição, Votação, etc.
│   ├── views.py                # Views para listagem e detalhes
│   ├── services/               # Serviços de integração com API
│   └── admin.py                # Interface administrativa
├── ai_analysis/                 # App de análise com IA
│   ├── models.py               # Modelos: ResumoIA, AnaliseImpacto, etc.
│   ├── services/               # Serviços de IA (OpenAI)
│   └── views.py                # Views para análises
├── parliamentary_dashboard/     # App de dashboard parlamentar
│   ├── models.py               # Modelos: PerfilParlamentar, Relatórios
│   └── views.py                # Views para dashboards
├── task_management/             # App de gestão de tarefas
│   ├── models.py               # Modelos: Equipe, Tarefa, Comentário
│   └── views.py                # Views para tarefas
├── news_portal/                 # App de portal de notícias
│   ├── models.py               # Modelos: Notícia, Categoria, Tag
│   └── views.py                # Views para notícias
├── templates/                   # Templates HTML
│   ├── base.html               # Template base
│   ├── news_portal/            # Templates do portal
│   ├── legislative_monitor/    # Templates de monitoramento
│   └── ...
└── static/                      # Arquivos estáticos
    ├── css/                    # Estilos CSS
    ├── js/                     # Scripts JavaScript
    └── img/                    # Imagens
```

## Uso

### Interface Web

1. **Portal de Notícias**: Página inicial com notícias sobre o processo legislativo
2. **Proposições**: Lista e detalhes de proposições legislativas
3. **Deputados**: Perfis parlamentares com estatísticas
4. **Dashboard**: Análises e visualizações de dados
5. **Busca IA**: Busca semântica inteligente
6. **Tarefas**: Gestão de tarefas e workflow (requer login)
7. **Admin**: Interface administrativa Django (requer login admin)

### Admin

Acesse `/admin/` com suas credenciais de superusuário para:

- Gerenciar deputados, proposições e votações
- Criar e editar notícias
- Gerenciar equipes e tarefas
- Configurar categorias e tags
- Visualizar análises de IA

### API REST

O sistema utiliza Django REST Framework. Endpoints disponíveis:

- Deputados, proposições, votações (via views)
- Análises de IA
- Notícias e categorias

## Integração com API da Câmara

Para sincronizar dados da Câmara dos Deputados, utilize o serviço `CamaraAPIService`:

```python
from legislative_monitor.services.camara_api import CamaraAPIService

api = CamaraAPIService()

# Listar deputados
deputados = api.listar_deputados()

# Obter proposições
proposicoes = api.listar_proposicoes(ano=2024)

# Detalhes de uma votação
votacao = api.obter_votacao(id_votacao)
```

## Integração com API do IBGE (Localidades)

O sistema inclui modelos e integração com a API de Localidades do IBGE para gerenciar dados geográficos brasileiros:

### Modelos de Localidades

- **Regiao**: Representa as 5 regiões brasileiras (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)
- **Estado**: Representa os 26 estados e o Distrito Federal
- **Municipio**: Representa os municípios brasileiros, com indicador de capital

### Sincronização de Dados do IBGE

Para sincronizar os dados de localidades do IBGE:

```bash
# Sincronizar todas as localidades (regiões, estados e municípios)
python manage.py sync_ibge_localidades

# Sincronizar apenas regiões
python manage.py sync_ibge_localidades --apenas-regioes

# Sincronizar apenas estados
python manage.py sync_ibge_localidades --apenas-estados

# Sincronizar apenas municípios
python manage.py sync_ibge_localidades --apenas-municipios
```

### Uso Programático

```python
from legislative_monitor.services.ibge_api import IBGELocalizacoesService
from legislative_monitor.models import Regiao, Estado, Municipio

# API do IBGE
api = IBGELocalizacoesService()

# Listar regiões
regioes = api.listar_regioes()

# Listar estados
estados = api.listar_estados()

# Listar municípios de um estado
municipios_sp = api.listar_municipios_por_estado(35)  # São Paulo

# Consultar modelos
regiao_sudeste = Regiao.objects.get(sigla='SE')
estado_sp = Estado.objects.get(sigla='SP')
capital_sp = Municipio.objects.get(estado=estado_sp, is_capital=True)

print(f"{capital_sp.nome} é a capital de {estado_sp.nome}")
```

**Características dos Modelos:**

- Constraint único garante que cada estado tem apenas uma capital
- Relacionamentos: `Regiao` → `Estado` → `Municipio`
- IDs são os códigos oficiais do IBGE
- Sincronização automática via comando de management

## Funcionalidades de IA

Para utilizar as funcionalidades de IA, configure a chave da OpenAI no arquivo `.env`:

```python
from ai_analysis.services.ai_service import AIAnalysisService

ai = AIAnalysisService()

# Gerar resumo
resumo = ai.gerar_resumo(texto_proposicao)

# Analisar impacto
analise = ai.analisar_impacto(texto_proposicao)

# Busca semântica
embedding = ai.gerar_embedding(texto)
```

## Desenvolvimento

### Executar Testes

```bash
python manage.py test
```

### Criar Nova Migração

```bash
python manage.py makemigrations
python manage.py migrate
```

### Iniciar Celery (para tarefas assíncronas)

```bash
celery -A monitoria_legislativa worker -l info
celery -A monitoria_legislativa beat -l info
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

## Contato

Para mais informações, entre em contato através do GitHub.

## Recursos Adicionais

- [Documentação Django](https://docs.djangoproject.com/)
- [API Dados Abertos Câmara](https://dadosabertos.camara.leg.br/)
- [Bootstrap 5](https://getbootstrap.com/)
- [OpenAI API](https://platform.openai.com/docs/)
