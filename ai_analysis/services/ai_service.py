"""
Serviço para análise de texto utilizando LLMs (OpenAI)
"""
from django.conf import settings
from openai import OpenAI


class AIAnalysisService:
    """Serviço para análise de texto usando IA"""
    
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"
    
    def gerar_resumo(self, texto, max_tokens=500):
        """Gera um resumo de um texto usando IA"""
        if not self.client:
            return "API Key não configurada"
        
        try:
            prompt = f"""Gere um resumo conciso e informativo do seguinte texto legislativo:

{texto}

Resumo:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise legislativa."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erro ao gerar resumo: {e}")
            return None
    
    def analisar_impacto(self, texto):
        """Analisa o impacto de uma proposição legislativa"""
        if not self.client:
            return None
        
        try:
            prompt = f"""Analise o impacto da seguinte proposição legislativa:

{texto}

Forneça uma análise estruturada considerando:
1. Nível de impacto (Baixo/Médio/Alto/Crítico)
2. Áreas afetadas
3. Impacto econômico
4. Impacto social
5. Impacto ambiental
6. Stakeholders principais"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de impacto legislativo."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erro ao analisar impacto: {e}")
            return None
    
    def extrair_principais_pontos(self, texto):
        """Extrai os principais pontos de um texto legislativo"""
        if not self.client:
            return []
        
        try:
            prompt = f"""Liste os principais pontos da seguinte proposição legislativa:

{texto}

Forneça uma lista numerada com os pontos mais importantes."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise legislativa."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            pontos_texto = response.choices[0].message.content.strip()
            # Converte o texto em lista
            pontos = [p.strip() for p in pontos_texto.split('\n') if p.strip()]
            return pontos
        except Exception as e:
            print(f"Erro ao extrair pontos: {e}")
            return []
    
    def analisar_sentimento_discurso(self, texto):
        """Analisa o sentimento de um discurso"""
        if not self.client:
            return None
        
        try:
            prompt = f"""Analise o sentimento do seguinte discurso parlamentar:

{texto}

Classifique como: Positivo, Negativo, Neutro ou Misto"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de sentimento."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erro ao analisar sentimento: {e}")
            return None
    
    def extrair_temas(self, texto):
        """Extrai temas principais de um discurso"""
        if not self.client:
            return []
        
        try:
            prompt = f"""Identifique os principais temas abordados no seguinte discurso:

{texto}

Liste os temas em ordem de relevância."""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de conteúdo."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            temas_texto = response.choices[0].message.content.strip()
            temas = [t.strip() for t in temas_texto.split('\n') if t.strip()]
            return temas
        except Exception as e:
            print(f"Erro ao extrair temas: {e}")
            return []
    
    def gerar_embedding(self, texto):
        """Gera embedding vetorial para busca semântica"""
        if not self.client:
            return None
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=texto
            )
            
            return response.data[0].embedding
        except Exception as e:
            print(f"Erro ao gerar embedding: {e}")
            return None
