from django.core.management.base import BaseCommand
from legislative_monitor.models import Sexo


class Command(BaseCommand):
    help = 'Popula o modelo Sexo com dados iniciais (M, F, NB)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a recriação dos registros mesmo se já existirem',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        self.stdout.write('Iniciando população do modelo Sexo...\n')
        
        # Dados iniciais
        sexos_iniciais = [
            {
                'sigla': 'M',
                'nome': 'Masculino',
            },
            {
                'sigla': 'F',
                'nome': 'Feminino',
            },
            {
                'sigla': 'NB',
                'nome': 'Não Binário',
            },
        ]
        
        criados = 0
        atualizados = 0
        erros = 0
        
        for dados in sexos_iniciais:
            try:
                sigla = dados['sigla']
                nome = dados['nome']
                
                # Verificar se já existe
                sexo_existente = Sexo.objects.filter(sigla=sigla).first()
                
                if sexo_existente:
                    if force:
                        # Atualizar
                        sexo_existente.nome = nome
                        sexo_existente.save()  # save() vai gerar descrição por IA e slug
                        
                        atualizados += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Atualizado: {sigla} - {nome}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'⚠ Já existe: {sigla} - {nome} (use --force para atualizar)'
                            )
                        )
                else:
                    # Criar novo
                    sexo = Sexo.objects.create(
                        sigla=sigla,
                        nome=nome
                    )
                    # save() já foi chamado no create(), gerando descrição e slug
                    
                    criados += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Criado: {sigla} - {nome}'
                        )
                    )
                    self.stdout.write(
                        f'  Slug: {sexo.slug}'
                    )
                    if sexo.descricao:
                        self.stdout.write(
                            f'  Descrição: {sexo.descricao[:80]}...'
                        )
                
            except Exception as e:
                erros += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Erro ao processar {dados["sigla"]}: {str(e)}'
                    )
                )
        
        # Resumo
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('População concluída!'))
        self.stdout.write(f'  • Criados: {criados}')
        self.stdout.write(f'  • Atualizados: {atualizados}')
        
        if erros > 0:
            self.stdout.write(self.style.ERROR(f'  • Erros: {erros}'))
        
        # Estatísticas finais
        total_sexos = Sexo.objects.count()
        self.stdout.write(f'  • Total de sexos no banco: {total_sexos}')
        self.stdout.write('='*70)
        
        # Listar todos os sexos
        if total_sexos > 0:
            self.stdout.write('\nSexos cadastrados:')
            for sexo in Sexo.objects.all():
                self.stdout.write(
                    f'  • {sexo.sigla} - {sexo.nome} (slug: {sexo.slug})'
                )
