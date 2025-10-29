from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from legislative_monitor.models import Proposicao, Discurso
from .models import ResumoIA, AnaliseImpacto, AnaliseDiscurso


def index(request):
    """Dashboard de análises IA"""
    resumos_recentes = ResumoIA.objects.all()[:10]
    analises_recentes = AnaliseImpacto.objects.all()[:10]
    
    context = {
        'resumos_recentes': resumos_recentes,
        'analises_recentes': analises_recentes,
    }
    return render(request, 'ai_analysis/index.html', context)


def resumos(request):
    """Lista resumos gerados por IA"""
    resumos = ResumoIA.objects.all()
    
    paginator = Paginator(resumos, 20)
    page = request.GET.get('page')
    resumos_page = paginator.get_page(page)
    
    context = {
        'resumos': resumos_page,
    }
    return render(request, 'ai_analysis/resumos_list.html', context)


def detalhe_resumo(request, pk):
    """Exibe detalhes de um resumo"""
    resumo = get_object_or_404(ResumoIA, pk=pk)
    
    context = {
        'resumo': resumo,
    }
    return render(request, 'ai_analysis/resumo_detail.html', context)


def analises_impacto(request):
    """Lista análises de impacto"""
    analises = AnaliseImpacto.objects.all()
    
    # Filtros
    nivel = request.GET.get('nivel')
    if nivel:
        analises = analises.filter(nivel_impacto=nivel)
    
    paginator = Paginator(analises, 20)
    page = request.GET.get('page')
    analises_page = paginator.get_page(page)
    
    context = {
        'analises': analises_page,
    }
    return render(request, 'ai_analysis/analises_impacto_list.html', context)


def detalhe_analise_impacto(request, pk):
    """Exibe detalhes de uma análise de impacto"""
    analise = get_object_or_404(AnaliseImpacto, pk=pk)
    
    context = {
        'analise': analise,
    }
    return render(request, 'ai_analysis/analise_impacto_detail.html', context)


def busca_semantica(request):
    """Interface de busca semântica"""
    query = request.GET.get('q', '')
    resultados = []
    
    if query:
        # Aqui implementaríamos a busca semântica real
        # Por enquanto, fazemos uma busca simples
        resultados = Proposicao.objects.filter(ementa__icontains=query)[:20]
    
    context = {
        'query': query,
        'resultados': resultados,
    }
    return render(request, 'ai_analysis/busca_semantica.html', context)

