from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Deputado, Proposicao, Votacao, Discurso


def listar_deputados(request):
    """Lista todos os deputados"""
    deputados = Deputado.objects.all()
    
    # Filtros
    partido = request.GET.get('partido')
    uf = request.GET.get('uf')
    
    if partido:
        deputados = deputados.filter(sigla_partido=partido)
    if uf:
        deputados = deputados.filter(uf_representacao=uf)
    
    paginator = Paginator(deputados, 20)
    page = request.GET.get('page')
    deputados_page = paginator.get_page(page)
    
    context = {
        'deputados': deputados_page,
        'partidos': Deputado.objects.values_list('sigla_partido', flat=True).distinct(),
        'ufs': Deputado.objects.values_list('uf_representacao', flat=True).distinct(),
    }
    return render(request, 'legislative_monitor/deputados_list.html', context)


def detalhe_deputado(request, id_deputado):
    """Exibe detalhes de um deputado"""
    deputado = get_object_or_404(Deputado, id_deputado=id_deputado)
    proposicoes = deputado.proposicoes.all()[:10]
    discursos = deputado.discursos.all()[:10]
    
    context = {
        'deputado': deputado,
        'proposicoes': proposicoes,
        'discursos': discursos,
    }
    return render(request, 'legislative_monitor/deputado_detail.html', context)


def listar_proposicoes(request):
    """Lista todas as proposições"""
    proposicoes = Proposicao.objects.all()
    
    # Filtros
    tipo = request.GET.get('tipo')
    situacao = request.GET.get('situacao')
    ano = request.GET.get('ano')
    
    if tipo:
        proposicoes = proposicoes.filter(tipo=tipo)
    if situacao:
        proposicoes = proposicoes.filter(situacao=situacao)
    if ano:
        proposicoes = proposicoes.filter(ano=ano)
    
    paginator = Paginator(proposicoes, 20)
    page = request.GET.get('page')
    proposicoes_page = paginator.get_page(page)
    
    context = {
        'proposicoes': proposicoes_page,
        'tipos': Proposicao.TIPO_CHOICES,
        'situacoes': Proposicao.SITUACAO_CHOICES,
    }
    return render(request, 'legislative_monitor/proposicoes_list.html', context)


def detalhe_proposicao(request, id_proposicao):
    """Exibe detalhes de uma proposição"""
    proposicao = get_object_or_404(Proposicao, id_proposicao=id_proposicao)
    votacoes = proposicao.votacoes.all()
    
    context = {
        'proposicao': proposicao,
        'votacoes': votacoes,
    }
    return render(request, 'legislative_monitor/proposicao_detail.html', context)


def listar_votacoes(request):
    """Lista todas as votações"""
    votacoes = Votacao.objects.all()
    
    paginator = Paginator(votacoes, 20)
    page = request.GET.get('page')
    votacoes_page = paginator.get_page(page)
    
    context = {
        'votacoes': votacoes_page,
    }
    return render(request, 'legislative_monitor/votacoes_list.html', context)


def detalhe_votacao(request, id_votacao):
    """Exibe detalhes de uma votação"""
    votacao = get_object_or_404(Votacao, id_votacao=id_votacao)
    votos = votacao.votos.select_related('deputado').all()
    
    context = {
        'votacao': votacao,
        'votos': votos,
    }
    return render(request, 'legislative_monitor/votacao_detail.html', context)

