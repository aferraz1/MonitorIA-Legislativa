from django.core.management.base import BaseCommand
from legislative_monitor.services.camara_api import CamaraAPIService
from legislative_monitor.models import TipoProposicao


class Command(BaseCommand):
    help = 'Sincroniza os tipos de proposição da API da Câmara dos Deputados'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando sincronização dos tipos de proposição...')
        
        api = CamaraAPIService()
        
        # Buscar dados da API
        response = api.listar_tipos_proposicao()
        
        if not response or 'dados' not in response:
            self.stdout.write(self.style.ERROR('Erro ao obter tipos de proposição da API'))
            return
        
        tipos_data = response['dados']
        self.stdout.write(f'Encontrados {len(tipos_data)} tipos de proposição na API')
        
        # Sincronizar dados
        criados = 0
        atualizados = 0
        erros = 0
        
        for tipo_data in tipos_data:
            try:
                tipo, created = TipoProposicao.objects.update_or_create(
                    cod=tipo_data['cod'],
                    defaults={
                        'sigla': tipo_data['sigla'],
                        'nome': tipo_data['nome'],
                        'descricao': tipo_data.get('descricao', ''),
                    }
                )
                
                if created:
                    criados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Criado: {tipo.sigla} - {tipo.nome}')
                    )
                else:
                    atualizados += 1
                    self.stdout.write(f'  Atualizado: {tipo.sigla} - {tipo.nome}')
                    
            except Exception as e:
                erros += 1
                self.stdout.write(
                    self.style.ERROR(f'✗ Erro ao processar tipo {tipo_data.get("sigla", "?")} (cod: {tipo_data.get("cod", "?")}): {str(e)}')
                )
        
        # Resumo
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Sincronização concluída!'))
        self.stdout.write(f'  • Tipos criados: {criados}')
        self.stdout.write(f'  • Tipos atualizados: {atualizados}')
        if erros > 0:
            self.stdout.write(self.style.WARNING(f'  • Erros: {erros}'))
        self.stdout.write(f'  • Total processado: {criados + atualizados}')
        self.stdout.write('='*60)
