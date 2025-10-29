from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Deputado, Proposicao, Votacao, Discurso, TipoProposicao


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
    proposicoes = deputado.proposicoes.select_related('tipo_proposicao').all()[:10]
    discursos = deputado.discursos.all()[:10]
    
    context = {
        'deputado': deputado,
        'proposicoes': proposicoes,
        'discursos': discursos,
    }
    return render(request, 'legislative_monitor/deputado_detail.html', context)


def listar_proposicoes(request):
    """Lista todas as proposições"""
    proposicoes = Proposicao.objects.select_related('tipo_proposicao', 'autor').all()
    
    # Filtros
    tipo_cod = request.GET.get('tipo')  # Agora usa código do TipoProposicao
    tipo_sigla = request.GET.get('tipo_sigla')  # Filtro por sigla
    situacao = request.GET.get('situacao')
    ano = request.GET.get('ano')
    busca = request.GET.get('q')  # Busca na ementa
    
    if tipo_cod:
        proposicoes = proposicoes.filter(tipo_proposicao__cod=tipo_cod)
    if tipo_sigla:
        proposicoes = proposicoes.filter(tipo_proposicao__sigla=tipo_sigla)
    if situacao:
        proposicoes = proposicoes.filter(situacao=situacao)
    if ano:
        proposicoes = proposicoes.filter(ano=ano)
    if busca:
        proposicoes = proposicoes.filter(ementa__icontains=busca)
    
    paginator = Paginator(proposicoes, 20)
    page = request.GET.get('page')
    proposicoes_page = paginator.get_page(page)
    
    # Buscar tipos disponíveis (siglas mais comuns)
    tipos_disponiveis = TipoProposicao.objects.filter(
        sigla__in=['PL', 'PEC', 'PLP', 'PDC', 'PRC', 'MPV']
    ).order_by('sigla')
    
    context = {
        'proposicoes': proposicoes_page,
        'tipos_disponiveis': tipos_disponiveis,
        'tipos': Proposicao.TIPO_CHOICES,  # Manter para compatibilidade
        'situacoes': Proposicao.SITUACAO_CHOICES,
        'anos_disponiveis': Proposicao.objects.values_list('ano', flat=True).distinct().order_by('-ano')[:10],
    }
    return render(request, 'legislative_monitor/proposicoes_list.html', context)


def detalhe_proposicao(request, id_proposicao):
    """Exibe detalhes de uma proposição"""
    proposicao = get_object_or_404(
        Proposicao.objects.select_related('tipo_proposicao', 'autor'),
        id_proposicao=id_proposicao
    )
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

