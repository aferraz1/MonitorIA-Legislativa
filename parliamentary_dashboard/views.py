from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from legislative_monitor.models import Deputado, VotoDeputado
from .models import PerfilParlamentar, RelatorioAtividade, ComparativoDeputados


def index(request):
    """Dashboard principal"""
    deputados_destaque = Deputado.objects.all()[:10]
    
    context = {
        'deputados_destaque': deputados_destaque,
    }
    return render(request, 'parliamentary_dashboard/index.html', context)


def perfil_parlamentar(request, id_deputado):
    """Exibe dashboard completo de um parlamentar"""
    deputado = get_object_or_404(Deputado, id_deputado=id_deputado)
    
    # Obtém ou cria perfil
    perfil, created = PerfilParlamentar.objects.get_or_create(deputado=deputado)
    
    # Estatísticas de votação
    votos = VotoDeputado.objects.filter(deputado=deputado)
    total_votos = votos.count()
    votos_sim = votos.filter(voto='SIM').count()
    votos_nao = votos.filter(voto='NAO').count()
    votos_abstencao = votos.filter(voto='ABSTENCAO').count()
    
    # Proposições
    proposicoes = deputado.proposicoes.all()[:10]
    
    # Discursos recentes
    discursos = deputado.discursos.all()[:10]
    
    # Relatórios
    relatorios = RelatorioAtividade.objects.filter(deputado=deputado)[:5]
    
    context = {
        'deputado': deputado,
        'perfil': perfil,
        'total_votos': total_votos,
        'votos_sim': votos_sim,
        'votos_nao': votos_nao,
        'votos_abstencao': votos_abstencao,
        'proposicoes': proposicoes,
        'discursos': discursos,
        'relatorios': relatorios,
    }
    return render(request, 'parliamentary_dashboard/perfil_parlamentar.html', context)


def comparar_deputados(request):
    """Permite comparar deputados"""
    deputados = Deputado.objects.all()
    comparativos = ComparativoDeputados.objects.all()[:10]
    
    context = {
        'deputados': deputados,
        'comparativos': comparativos,
    }
    return render(request, 'parliamentary_dashboard/comparar_deputados.html', context)


def relatorios(request):
    """Lista relatórios de atividade"""
    relatorios = RelatorioAtividade.objects.all()[:50]
    
    context = {
        'relatorios': relatorios,
    }
    return render(request, 'parliamentary_dashboard/relatorios.html', context)

