from django.core.management.base import BaseCommand
from legislative_monitor.models import Partido
from legislative_monitor.services.camara_api import CamaraAPIService
from datetime import datetime


class Command(BaseCommand):
    help = 'Sincroniza partidos políticos da API da Câmara dos Deputados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detalhes',
            action='store_true',
            help='Busca detalhes completos de cada partido (mais lento)',
        )

    def handle(self, *args, **options):
        buscar_detalhes = options['detalhes']
        
        self.stdout.write('Iniciando sincronização de partidos...\n')
        
        # Criar serviço da API
        api = CamaraAPIService()
        
        # Buscar lista de partidos
        self.stdout.write('Buscando lista de partidos da API...')
        response = api.listar_partidos(itens=100)
        
        if not response or 'dados' not in response:
            self.stdout.write(self.style.ERROR('Erro ao buscar partidos da API'))
            return
        
        partidos_api = response['dados']
        total = len(partidos_api)
        
        self.stdout.write(self.style.SUCCESS(f'✓ {total} partidos encontrados\n'))
        
        # Estatísticas
        criados = 0
        atualizados = 0
        erros = 0
        
        for idx, partido_data in enumerate(partidos_api, 1):
            try:
                id_partido = partido_data['id']
                sigla = partido_data['sigla']
                nome = partido_data['nome']
                uri = partido_data.get('uri', '')
                
                self.stdout.write(f'[{idx}/{total}] Processando {sigla}...', ending='')
                
                # Buscar detalhes se solicitado
                dados_completos = {}
                if buscar_detalhes:
                    detalhes = api.obter_partido(id_partido)
                    if detalhes and 'dados' in detalhes:
                        dados_detalhes = detalhes['dados']
                        
                        # Extrair dados de status
                        status = dados_detalhes.get('status', {})
                        if status:
                            dados_completos['status_data'] = self._parse_datetime(status.get('data'))
                            dados_completos['status_situacao'] = status.get('situacao', '')
                            dados_completos['status_total_posse'] = status.get('totalPosse')
                            dados_completos['status_total_membros'] = status.get('totalMembros')
                            dados_completos['status_id_legislatura'] = status.get('idLegislatura')
                        
                        # Extrair dados adicionais
                        dados_completos['numero_eleitoral'] = dados_detalhes.get('numeroEleitoral')
                        dados_completos['url_logo'] = dados_detalhes.get('urlLogo', '')
                        dados_completos['url_website'] = dados_detalhes.get('urlWebSite', '')
                        dados_completos['url_facebook'] = dados_detalhes.get('urlFacebook', '')
                
                # Criar ou atualizar partido
                partido, created = Partido.objects.update_or_create(
                    id_partido=id_partido,
                    defaults={
                        'sigla': sigla,
                        'nome': nome,
                        'uri': uri,
                        **dados_completos
                    }
                )
                
                if created:
                    criados += 1
                    self.stdout.write(self.style.SUCCESS(' ✓ Criado'))
                else:
                    atualizados += 1
                    self.stdout.write(self.style.WARNING(' ↻ Atualizado'))
                
            except Exception as e:
                erros += 1
                self.stdout.write(self.style.ERROR(f' ✗ Erro: {str(e)}'))
        
        # Relatório final
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('SINCRONIZAÇÃO CONCLUÍDA'))
        self.stdout.write('='*60)
        self.stdout.write(f'Total processado: {total}')
        self.stdout.write(self.style.SUCCESS(f'  • Criados: {criados}'))
        self.stdout.write(self.style.WARNING(f'  • Atualizados: {atualizados}'))
        if erros > 0:
            self.stdout.write(self.style.ERROR(f'  • Erros: {erros}'))
        
        # Estatísticas do banco
        self.stdout.write('\nEstatísticas do banco de dados:')
        total_partidos = Partido.objects.count()
        self.stdout.write(f'  • Total de partidos: {total_partidos}')
        
        # Top 5 partidos por número de deputados
        self.stdout.write('\nPartidos cadastrados:')
        for partido in Partido.objects.all()[:10]:
            self.stdout.write(f'  • {partido.sigla} - {partido.nome}')
    
    def _parse_datetime(self, data_str):
        """Converte string de data da API para datetime"""
        if not data_str:
            return None
        
        try:
            # Formato: "2025-04-08T14:44"
            return datetime.strptime(data_str, "%Y-%m-%dT%H:%M")
        except:
            return None
