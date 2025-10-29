from django.core.management.base import BaseCommand
from news_portal.models import Categoria, Noticia
from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):
    help = 'Cria categorias e notícias de exemplo'

    def handle(self, *args, **options):
        self.stdout.write('Criando categorias...')
        
        categorias_data = [
            {'nome': 'Política', 'cor': '#0d6efd', 'descricao': 'Notícias sobre política brasileira'},
            {'nome': 'Economia', 'cor': '#198754', 'descricao': 'Notícias sobre economia'},
            {'nome': 'Legislação', 'cor': '#dc3545', 'descricao': 'Novas leis e proposições'},
            {'nome': 'Comissões', 'cor': '#ffc107', 'descricao': 'Atividades das comissões'},
            {'nome': 'Plenário', 'cor': '#0dcaf0', 'descricao': 'Votações e debates no plenário'},
        ]
        
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoria "{categoria.nome}" criada'))
        
        # Get or create admin user
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        
        self.stdout.write('Criando notícias de exemplo...')
        
        noticias_data = [
            {
                'titulo': 'Câmara aprova projeto de lei sobre educação digital',
                'subtitulo': 'Proposta inclui tecnologia no currículo escolar',
                'resumo': 'A Câmara dos Deputados aprovou hoje o projeto de lei que inclui educação digital como disciplina obrigatória no ensino básico.',
                'conteudo': '''A Câmara dos Deputados aprovou nesta terça-feira o projeto de lei que torna obrigatória a inclusão de educação digital no currículo do ensino básico. A proposta segue agora para o Senado Federal.

O texto aprovado estabelece que escolas públicas e privadas deverão oferecer conteúdos relacionados ao uso responsável e seguro da internet, programação básica e pensamento computacional.

Segundo o relator da proposta, a medida visa preparar os estudantes para os desafios do século XXI e promover a inclusão digital no país.''',
                'categoria': 'Legislação',
                'destaque': True,
            },
            {
                'titulo': 'Deputados debatem reforma tributária em audiência pública',
                'subtitulo': 'Especialistas apresentam propostas para simplificação',
                'resumo': 'Comissão especial realiza audiência pública para discutir os impactos da reforma tributária na economia brasileira.',
                'conteudo': '''A Comissão Especial da Reforma Tributária realizou hoje uma audiência pública com especialistas em tributação para debater as mudanças propostas no sistema tributário brasileiro.

Entre os pontos discutidos estão a unificação de impostos, a criação do IVA (Imposto sobre Valor Agregado) e os impactos sobre diferentes setores da economia.

Representantes do setor produtivo, acadêmicos e membros do governo participaram do debate, apresentando diferentes perspectivas sobre a reforma.''',
                'categoria': 'Comissões',
                'destaque': True,
            },
            {
                'titulo': 'Nova lei de proteção de dados pessoais entra em vigor',
                'subtitulo': 'Empresas têm prazo para se adequar às novas regras',
                'resumo': 'Lei que estabelece regras para tratamento de dados pessoais entra em vigor e traz mudanças importantes para empresas e cidadãos.',
                'conteudo': '''Entrou em vigor hoje a nova lei de proteção de dados pessoais, que estabelece regras mais rígidas para coleta, armazenamento e uso de informações pessoais por empresas e órgãos públicos.

A legislação cria uma série de direitos para os titulares de dados, incluindo o direito de saber quais informações são coletadas, como são usadas e a possibilidade de solicitar a exclusão dos dados.

Empresas que descumprirem as novas regras poderão ser multadas em até 2% do faturamento, limitado a R$ 50 milhões por infração.''',
                'categoria': 'Legislação',
                'destaque': False,
            },
            {
                'titulo': 'Plenário vota projeto sobre energia renovável',
                'subtitulo': 'Proposta incentiva investimentos em energia solar e eólica',
                'resumo': 'Deputados votam hoje projeto que cria incentivos fiscais para investimentos em fontes de energia renovável.',
                'conteudo': '''O Plenário da Câmara dos Deputados vota hoje o projeto de lei que cria incentivos fiscais para empresas que investirem em energia renovável, especialmente solar e eólica.

A proposta prevê redução de impostos e linhas de crédito facilitadas para projetos de geração de energia limpa. O objetivo é aumentar a participação de fontes renováveis na matriz energética brasileira.

Ambientalistas elogiam a iniciativa, mas cobram medidas mais abrangentes para combater as mudanças climáticas.''',
                'categoria': 'Plenário',
                'destaque': True,
            },
            {
                'titulo': 'Comissão de Economia debate impactos da inflação',
                'subtitulo': 'Parlamentares ouvem especialistas sobre controle de preços',
                'resumo': 'Comissão realiza reunião para discutir medidas de controle da inflação e seus impactos na economia.',
                'conteudo': '''A Comissão de Economia da Câmara dos Deputados realizou hoje uma reunião técnica para debater os impactos da inflação na economia brasileira e possíveis medidas para seu controle.

Economistas apresentaram análises sobre a alta de preços de alimentos, combustíveis e outros itens básicos, além de avaliar as políticas monetárias adotadas pelo Banco Central.

Os deputados questionaram sobre alternativas para proteger o poder de compra da população, especialmente dos mais vulneráveis.''',
                'categoria': 'Economia',
                'destaque': False,
            },
        ]
        
        for noticia_data in noticias_data:
            categoria = Categoria.objects.get(nome=noticia_data.pop('categoria'))
            
            noticia, created = Noticia.objects.get_or_create(
                titulo=noticia_data['titulo'],
                defaults={
                    **noticia_data,
                    'categoria': categoria,
                    'autor': user,
                    'status': 'PUBLICADA',
                    'data_publicacao': timezone.now(),
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Notícia "{noticia.titulo}" criada'))
        
        self.stdout.write(self.style.SUCCESS('Dados de exemplo criados com sucesso!'))
