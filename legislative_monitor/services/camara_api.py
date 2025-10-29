"""
Serviço para integração com a API de Dados Abertos da Câmara dos Deputados
"""
import requests
from datetime import datetime
from django.conf import settings


class CamaraAPIService:
    """Serviço para consumir a API da Câmara dos Deputados"""
    
    def __init__(self):
        self.base_url = settings.CAMARA_API_BASE_URL
    
    def _fazer_requisicao(self, endpoint, params=None):
        """Faz uma requisição à API da Câmara"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao fazer requisição: {e}")
            return None
    
    def listar_deputados(self, **kwargs):
        """
        Lista deputados com filtros opcionais
        Parâmetros: siglaPartido, siglaUf, dataInicio, dataFim, etc.
        """
        return self._fazer_requisicao('deputados', params=kwargs)
    
    def obter_deputado(self, id_deputado):
        """Obtém informações detalhadas de um deputado"""
        return self._fazer_requisicao(f'deputados/{id_deputado}')
    
    def listar_proposicoes(self, **kwargs):
        """
        Lista proposições com filtros opcionais
        Parâmetros: siglaTipo, numero, ano, dataInicio, dataFim, etc.
        """
        return self._fazer_requisicao('proposicoes', params=kwargs)
    
    def obter_proposicao(self, id_proposicao):
        """Obtém informações detalhadas de uma proposição"""
        return self._fazer_requisicao(f'proposicoes/{id_proposicao}')
    
    def listar_votacoes_proposicao(self, id_proposicao):
        """Lista votações de uma proposição"""
        return self._fazer_requisicao(f'proposicoes/{id_proposicao}/votacoes')
    
    def obter_votacao(self, id_votacao):
        """Obtém informações detalhadas de uma votação"""
        return self._fazer_requisicao(f'votacoes/{id_votacao}')
    
    def listar_votos_votacao(self, id_votacao):
        """Lista votos de deputados em uma votação"""
        return self._fazer_requisicao(f'votacoes/{id_votacao}/votos')
    
    def listar_discursos_deputado(self, id_deputado, **kwargs):
        """
        Lista discursos de um deputado
        Parâmetros: dataInicio, dataFim, etc.
        """
        return self._fazer_requisicao(f'deputados/{id_deputado}/discursos', params=kwargs)
    
    def obter_discurso(self, id_discurso):
        """Obtém informações detalhadas de um discurso"""
        return self._fazer_requisicao(f'discursos/{id_discurso}')
    
    def listar_eventos(self, **kwargs):
        """
        Lista eventos da Câmara
        Parâmetros: dataInicio, dataFim, etc.
        """
        return self._fazer_requisicao('eventos', params=kwargs)
    
    def listar_orgaos(self, **kwargs):
        """Lista órgãos da Câmara (comissões, etc.)"""
        return self._fazer_requisicao('orgaos', params=kwargs)
    
    def listar_tipos_proposicao(self):
        """Lista todos os tipos de proposição disponíveis"""
        return self._fazer_requisicao('referencias/proposicoes/siglaTipo')
