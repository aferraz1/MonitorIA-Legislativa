from django.core.management.base import BaseCommand
from legislative_monitor.services.ibge_api import IBGELocalizacoesService
from legislative_monitor.models import Regiao, Estado, Municipio


class Command(BaseCommand):
    help = 'Sincroniza dados de localidades (regiões, estados e municípios) da API do IBGE'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apenas-regioes',
            action='store_true',
            help='Sincroniza apenas as regiões',
        )
        parser.add_argument(
            '--apenas-estados',
            action='store_true',
            help='Sincroniza apenas os estados',
        )
        parser.add_argument(
            '--apenas-municipios',
            action='store_true',
            help='Sincroniza apenas os municípios',
        )

    def handle(self, *args, **options):
        api = IBGELocalizacoesService()
        
        apenas_regioes = options.get('apenas_regioes')
        apenas_estados = options.get('apenas_estados')
        apenas_municipios = options.get('apenas_municipios')
        
        # Se nenhuma opção específica foi escolhida, sincroniza tudo
        sincronizar_tudo = not (apenas_regioes or apenas_estados or apenas_municipios)
        
        if sincronizar_tudo or apenas_regioes:
            self.sincronizar_regioes(api)
        
        if sincronizar_tudo or apenas_estados:
            self.sincronizar_estados(api)
        
        if sincronizar_tudo or apenas_municipios:
            self.sincronizar_municipios(api)
        
        self.stdout.write(self.style.SUCCESS('Sincronização concluída com sucesso!'))

    def sincronizar_regioes(self, api):
        """Sincroniza as regiões do Brasil"""
        self.stdout.write('Sincronizando regiões...')
        
        regioes_data = api.listar_regioes()
        if not regioes_data:
            self.stdout.write(self.style.ERROR('Erro ao obter regiões da API do IBGE'))
            return
        
        for regiao_data in regioes_data:
            regiao, created = Regiao.objects.update_or_create(
                id=regiao_data['id'],
                defaults={
                    'sigla': regiao_data['sigla'],
                    'nome': regiao_data['nome'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Região "{regiao.nome}" criada'))
            else:
                self.stdout.write(f'Região "{regiao.nome}" atualizada')
        
        self.stdout.write(self.style.SUCCESS(f'Total de regiões sincronizadas: {len(regioes_data)}'))

    def sincronizar_estados(self, api):
        """Sincroniza os estados do Brasil"""
        self.stdout.write('Sincronizando estados...')
        
        estados_data = api.listar_estados()
        if not estados_data:
            self.stdout.write(self.style.ERROR('Erro ao obter estados da API do IBGE'))
            return
        
        for estado_data in estados_data:
            try:
                regiao = Regiao.objects.get(id=estado_data['regiao']['id'])
                
                estado, created = Estado.objects.update_or_create(
                    id=estado_data['id'],
                    defaults={
                        'sigla': estado_data['sigla'],
                        'nome': estado_data['nome'],
                        'regiao': regiao,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Estado "{estado.nome}" criado'))
                else:
                    self.stdout.write(f'Estado "{estado.nome}" atualizado')
            except Regiao.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'Região {estado_data["regiao"]["id"]} não encontrada para o estado {estado_data["nome"]}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS(f'Total de estados sincronizados: {len(estados_data)}'))

    def sincronizar_municipios(self, api):
        """Sincroniza os municípios do Brasil"""
        self.stdout.write('Sincronizando municípios...')
        self.stdout.write(self.style.WARNING('Atenção: Este processo pode demorar alguns minutos...'))
        
        municipios_data = api.listar_todos_municipios()
        if not municipios_data:
            self.stdout.write(self.style.ERROR('Erro ao obter municípios da API do IBGE'))
            return
        
        # Lista de capitais brasileiras (código IBGE)
        capitais = {
            1100205,  # Porto Velho - RO
            1200401,  # Rio Branco - AC
            1302603,  # Manaus - AM
            1400100,  # Boa Vista - RR
            1501402,  # Belém - PA
            1600303,  # Macapá - AP
            1721000,  # Palmas - TO
            2111300,  # São Luís - MA
            2211001,  # Teresina - PI
            2304400,  # Fortaleza - CE
            2408102,  # Natal - RN
            2507507,  # João Pessoa - PB
            2611606,  # Recife - PE
            2704302,  # Maceió - AL
            2800308,  # Aracaju - SE
            2927408,  # Salvador - BA
            3106200,  # Belo Horizonte - MG
            3170206,  # Vitória - ES
            3304557,  # Rio de Janeiro - RJ
            3550308,  # São Paulo - SP
            4106902,  # Curitiba - PR
            4205407,  # Florianópolis - SC
            4314902,  # Porto Alegre - RS
            5002704,  # Campo Grande - MS
            5103403,  # Cuiabá - MT
            5208707,  # Goiânia - GO
            5300108,  # Brasília - DF
        }
        
        contador = 0
        for municipio_data in municipios_data:
            try:
                # Extrair código do estado dos primeiros 2 dígitos do código do município
                codigo_estado = int(str(municipio_data['id'])[:2])
                estado = Estado.objects.get(id=codigo_estado)
                
                is_capital = municipio_data['id'] in capitais
                
                municipio, created = Municipio.objects.update_or_create(
                    id=municipio_data['id'],
                    defaults={
                        'nome': municipio_data['nome'],
                        'estado': estado,
                        'is_capital': is_capital,
                    }
                )
                
                contador += 1
                if contador % 500 == 0:
                    self.stdout.write(f'Sincronizados {contador} municípios...')
                
            except Estado.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f'Estado {codigo_estado} não encontrado para o município {municipio_data["nome"]}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS(f'Total de municípios sincronizados: {contador}'))
