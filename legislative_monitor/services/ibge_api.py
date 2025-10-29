"""
Serviço para integração com a API de Localidades do IBGE
"""
import requests


class IBGELocalizacoesService:
    """Serviço para consumir a API de Localidades do IBGE"""
    
    def __init__(self):
        self.base_url = 'https://servicodados.ibge.gov.br/api/v1/localidades'
    
    def _fazer_requisicao(self, endpoint):
        """Faz uma requisição à API do IBGE"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao fazer requisição: {e}")
            return None
    
    def listar_regioes(self):
        """
        Lista todas as regiões do Brasil
        Retorna: Lista com dados das regiões
        Exemplo de retorno:
        [
            {
                "id": 1,
                "sigla": "N",
                "nome": "Norte"
            },
            ...
        ]
        """
        return self._fazer_requisicao('regioes')
    
    def listar_estados(self):
        """
        Lista todos os estados do Brasil
        Retorna: Lista com dados dos estados
        Exemplo de retorno:
        [
            {
                "id": 11,
                "sigla": "RO",
                "nome": "Rondônia",
                "regiao": {
                    "id": 1,
                    "sigla": "N",
                    "nome": "Norte"
                }
            },
            ...
        ]
        """
        return self._fazer_requisicao('estados')
    
    def obter_estado(self, id_estado):
        """
        Obtém informações de um estado específico
        Parâmetros:
            id_estado: Código do IBGE do estado
        """
        return self._fazer_requisicao(f'estados/{id_estado}')
    
    def listar_municipios_por_estado(self, id_estado):
        """
        Lista todos os municípios de um estado
        Parâmetros:
            id_estado: Código do IBGE do estado
        Retorna: Lista com dados dos municípios
        """
        return self._fazer_requisicao(f'estados/{id_estado}/municipios')
    
    def listar_todos_municipios(self):
        """
        Lista todos os municípios do Brasil
        Retorna: Lista com dados dos municípios
        Exemplo de retorno:
        [
            {
                "id": 1100015,
                "nome": "Alta Floresta D'Oeste",
                "microrregiao": {...},
                "regiao-imediata": {...}
            },
            ...
        ]
        """
        return self._fazer_requisicao('municipios')
    
    def obter_municipio(self, id_municipio):
        """
        Obtém informações de um município específico
        Parâmetros:
            id_municipio: Código do IBGE do município
        """
        return self._fazer_requisicao(f'municipios/{id_municipio}')
