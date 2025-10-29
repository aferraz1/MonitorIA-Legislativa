from django.core.management.base import BaseCommand
from django.db.models import Q
from legislative_monitor.models import Proposicao, TipoProposicao


class Command(BaseCommand):
    help = 'Migra os tipos de proposição do campo legado "tipo" para o novo campo "tipo_proposicao"'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula a migração sem salvar alterações',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN: Nenhuma alteração será salva\n'))
        
        self.stdout.write('Iniciando migração dos tipos de proposição...\n')
        
        # Buscar proposições sem tipo_proposicao definido
        proposicoes = Proposicao.objects.filter(
            Q(tipo_proposicao__isnull=True) & ~Q(tipo='')
        )
        
        total = proposicoes.count()
        self.stdout.write(f'Encontradas {total} proposições para migrar\n')
        
        if total == 0:
            self.stdout.write(self.style.SUCCESS('Nenhuma proposição precisa ser migrada!'))
            return
        
        migradas = 0
        nao_encontrados = 0
        erros = 0
        tipos_nao_encontrados = set()
        
        for proposicao in proposicoes:
            try:
                # Buscar tipo correspondente pela sigla
                # Primeiro tenta buscar o tipo mais comum (menor código)
                tipo_obj = TipoProposicao.objects.filter(
                    sigla=proposicao.tipo
                ).order_by('cod').first()
                
                if tipo_obj:
                    if not dry_run:
                        proposicao.tipo_proposicao = tipo_obj
                        proposicao.save()
                    
                    migradas += 1
                    
                    if migradas <= 10 or migradas % 100 == 0:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Migrada: {proposicao.tipo} {proposicao.numero}/{proposicao.ano} '
                                f'→ {tipo_obj.sigla} (cod: {tipo_obj.cod})'
                            )
                        )
                else:
                    nao_encontrados += 1
                    tipos_nao_encontrados.add(proposicao.tipo)
                    
                    if nao_encontrados <= 10:
                        self.stdout.write(
                            self.style.WARNING(
                                f'⚠ Tipo não encontrado: {proposicao.tipo} '
                                f'(Proposição {proposicao.id}: {proposicao.numero}/{proposicao.ano})'
                            )
                        )
                    
            except Exception as e:
                erros += 1
                if erros <= 10:
                    self.stdout.write(
                        self.style.ERROR(
                            f'✗ Erro ao migrar proposição {proposicao.id}: {str(e)}'
                        )
                    )
        
        # Resumo
        self.stdout.write('\n' + '='*70)
        
        if dry_run:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN - Nenhuma alteração foi salva'))
        else:
            self.stdout.write(self.style.SUCCESS('Migração concluída!'))
        
        self.stdout.write(f'  • Proposições migradas: {migradas}')
        
        if nao_encontrados > 0:
            self.stdout.write(
                self.style.WARNING(f'  • Tipos não encontrados: {nao_encontrados}')
            )
            self.stdout.write(f'    Siglas não encontradas: {", ".join(sorted(tipos_nao_encontrados))}')
        
        if erros > 0:
            self.stdout.write(self.style.ERROR(f'  • Erros: {erros}'))
        
        self.stdout.write(f'  • Total processado: {migradas + nao_encontrados + erros}')
        self.stdout.write('='*70)
        
        # Estatísticas adicionais
        if not dry_run and migradas > 0:
            self.stdout.write('\n' + 'Estatísticas após migração:')
            
            total_proposicoes = Proposicao.objects.count()
            com_tipo_proposicao = Proposicao.objects.filter(tipo_proposicao__isnull=False).count()
            sem_tipo_proposicao = Proposicao.objects.filter(tipo_proposicao__isnull=True).count()
            
            self.stdout.write(f'  • Total de proposições: {total_proposicoes}')
            self.stdout.write(f'  • Com tipo_proposicao: {com_tipo_proposicao} ({com_tipo_proposicao/total_proposicoes*100:.1f}%)')
            self.stdout.write(f'  • Sem tipo_proposicao: {sem_tipo_proposicao} ({sem_tipo_proposicao/total_proposicoes*100:.1f}%)')
