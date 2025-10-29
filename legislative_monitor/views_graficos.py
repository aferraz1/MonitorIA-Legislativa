"""
Views para gráficos e visualizações de dados
"""
from django.shortcuts import render
from django.db.models import Count
from .models import Deputado, Partido, Proposicao
import json


def graficos_partidos(request):
    """Exibe gráficos de distribuição partidária"""
    
    # Distribuição de deputados por partido
    deputados_por_partido = Partido.objects.annotate(
        total=Count('deputados')
    ).filter(total__gt=0).order_by('-total')
    
    # Dados para gráfico de pizza/barras
    partidos_labels = [p.sigla for p in deputados_por_partido]
    partidos_data = [p.total for p in deputados_por_partido]
    partidos_cores = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
        '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384',
        '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
        '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384', '#36A2EB'
    ]
    
    # Distribuição de proposições por partido
    proposicoes_por_partido = Partido.objects.annotate(
        total_proposicoes=Count('deputados__proposicoes')
    ).filter(total_proposicoes__gt=0).order_by('-total_proposicoes')[:10]
    
    proposicoes_labels = [p.sigla for p in proposicoes_por_partido]
    proposicoes_data = [p.total_proposicoes for p in proposicoes_por_partido]
    
    # Distribuição geográfica (deputados por partido e UF)
    from .models import Estado
    distribuicao_geografica = []
    
    for partido in deputados_por_partido[:10]:  # Top 10 partidos
        deputados_uf = Deputado.objects.filter(
            sigla_partido=partido
        ).values('uf_representacao__sigla').annotate(
            total=Count('id')
        ).order_by('-total')[:5]  # Top 5 UFs por partido
        
        distribuicao_geografica.append({
            'partido': partido.sigla,
            'ufs': [
                {'uf': d['uf_representacao__sigla'] or 'N/D', 'total': d['total']}
                for d in deputados_uf
            ]
        })
    
    # Estatísticas gerais
    total_deputados = Deputado.objects.count()
    total_partidos = Partido.objects.count()
    partidos_com_deputados = deputados_por_partido.count()
    
    # Maior e menor partido
    maior_partido = deputados_por_partido.first()
    menor_partido = deputados_por_partido.last()
    
    context = {
        # Dados para gráficos
        'partidos_labels': json.dumps(partidos_labels),
        'partidos_data': json.dumps(partidos_data),
        'partidos_cores': json.dumps(partidos_cores[:len(partidos_labels)]),
        
        'proposicoes_labels': json.dumps(proposicoes_labels),
        'proposicoes_data': json.dumps(proposicoes_data),
        
        'distribuicao_geografica': distribuicao_geografica,
        
        # Estatísticas
        'total_deputados': total_deputados,
        'total_partidos': total_partidos,
        'partidos_com_deputados': partidos_com_deputados,
        'maior_partido': maior_partido,
        'menor_partido': menor_partido,
        
        # Dados tabulares
        'deputados_por_partido': deputados_por_partido,
        'proposicoes_por_partido': proposicoes_por_partido,
    }
    
    return render(request, 'legislative_monitor/graficos_partidos.html', context)
