from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db import models
from .models import Deputado, Proposicao, Votacao, Discurso, TipoProposicao


def listar_deputados(request):
    """Lista todos os deputados"""
    from .models import Partido
    
    deputados = Deputado.objects.select_related('sigla_partido', 'uf_representacao', 'sexo').all()
    
    # Filtros
    partido_sigla = request.GET.get('partido')
    uf_sigla = request.GET.get('uf')
    sexo_sigla = request.GET.get('sexo')
    busca = request.GET.get('q')
    
    if partido_sigla:
        deputados = deputados.filter(sigla_partido__sigla=partido_sigla)
    if uf_sigla:
        deputados = deputados.filter(uf_representacao__sigla=uf_sigla)
    if sexo_sigla:
        deputados = deputados.filter(sexo__sigla=sexo_sigla)
    if busca:
        deputados = deputados.filter(
            models.Q(nome__icontains=busca) |
            models.Q(nome_civil__icontains=busca)
        )
    
    paginator = Paginator(deputados, 20)
    page = request.GET.get('page')
    deputados_page = paginator.get_page(page)
    
    # Obter listas para filtros
    partidos = Partido.objects.all().order_by('sigla')
    from .models import Estado, Sexo
    ufs = Estado.objects.all().order_by('sigla')
    sexos = Sexo.objects.all().order_by('sigla')
    
    context = {
        'deputados': deputados_page,
        'partidos': partidos,
        'ufs': ufs,
        'sexos': sexos,
    }
    return render(request, 'legislative_monitor/deputados_list.html', context)


def detalhe_deputado(request, id_deputado):
    """Exibe detalhes de um deputado"""
    deputado = get_object_or_404(Deputado, id_deputado=id_deputado)
    proposicoes = deputado.proposicoes.select_related('tipo').all()[:10]
    discursos = deputado.discursos.all()[:10]
    
    context = {
        'deputado': deputado,
        'proposicoes': proposicoes,
        'discursos': discursos,
    }
    return render(request, 'legislative_monitor/deputado_detail.html', context)


def listar_proposicoes(request):
    """Lista todas as proposições"""
    proposicoes = Proposicao.objects.select_related('tipo', 'autor').all()
    
    # Filtros
    tipo_cod = request.GET.get('tipo')  # Agora usa código do TipoProposicao
    tipo_sigla = request.GET.get('tipo_sigla')  # Filtro por sigla
    situacao = request.GET.get('situacao')
    ano = request.GET.get('ano')
    busca = request.GET.get('q')  # Busca na ementa
    
    if tipo_cod:
        proposicoes = proposicoes.filter(tipo__cod=tipo_cod)
    if tipo_sigla:
        proposicoes = proposicoes.filter(tipo__sigla=tipo_sigla)
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
        # 'tipos': Proposicao.TIPO_CHOICES,  # Removido - usar tipos_disponiveis
        'situacoes': Proposicao.SITUACAO_CHOICES,
        'anos_disponiveis': Proposicao.objects.values_list('ano', flat=True).distinct().order_by('-ano')[:10],
    }
    return render(request, 'legislative_monitor/proposicoes_list.html', context)


def detalhe_proposicao(request, id_proposicao):
    """Exibe detalhes de uma proposição"""
    proposicao = get_object_or_404(
        Proposicao.objects.select_related('tipo', 'autor'),
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


# Views para TipoProposicao
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q


class TipoProposicaoListView(ListView):
    """View para listar todos os tipos de proposição"""
    model = TipoProposicao
    template_name = 'legislative_monitor/tipos_proposicao_list.html'
    context_object_name = 'tipos'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = TipoProposicao.objects.all()
        
        # Filtro por sigla
        sigla = self.request.GET.get('sigla')
        if sigla:
            queryset = queryset.filter(sigla__icontains=sigla)
        
        # Filtro por nome
        nome = self.request.GET.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        
        # Busca geral
        busca = self.request.GET.get('q')
        if busca:
            queryset = queryset.filter(
                Q(sigla__icontains=busca) |
                Q(nome__icontains=busca) |
                Q(descricao__icontains=busca)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas
        context['total_tipos'] = TipoProposicao.objects.count()
        context['tipos_com_descricao'] = TipoProposicao.objects.exclude(descricao='').count()
        context['tipos_sem_descricao'] = TipoProposicao.objects.filter(descricao='').count()
        
        # Top siglas
        context['top_siglas'] = TipoProposicao.objects.values('sigla').annotate(
            total=Count('id')
        ).order_by('-total')[:10]
        
        # Parâmetros de busca
        context['sigla_filter'] = self.request.GET.get('sigla', '')
        context['nome_filter'] = self.request.GET.get('nome', '')
        context['search_query'] = self.request.GET.get('q', '')
        
        return context


class TipoProposicaoDetailView(DetailView):
    """View para exibir detalhes de um tipo de proposição"""
    model = TipoProposicao
    template_name = 'legislative_monitor/tipo_proposicao_detail.html'
    context_object_name = 'tipo'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscar outros tipos com a mesma sigla
        context['tipos_mesma_sigla'] = TipoProposicao.objects.filter(
            sigla=self.object.sigla
        ).exclude(id=self.object.id)
        
        # Proposições deste tipo (se houver relacionamento)
        # context['proposicoes'] = self.object.proposicoes.all()[:10]
        # context['total_proposicoes'] = self.object.proposicoes.count()
        
        return context



def listar_partidos(request):
    """Lista todos os partidos"""
    from .models import Partido
    from django.db.models import Count
    
    partidos = Partido.objects.annotate(
        total_deputados=Count('deputados')
    ).order_by('-total_deputados')
    
    # Filtros
    situacao = request.GET.get('situacao')
    busca = request.GET.get('q')
    
    if situacao:
        partidos = partidos.filter(status_situacao=situacao)
    if busca:
        partidos = partidos.filter(
            models.Q(sigla__icontains=busca) | 
            models.Q(nome__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(partidos, 20)
    page = request.GET.get('page')
    partidos_page = paginator.get_page(page)
    
    # Estatísticas
    total_partidos = Partido.objects.count()
    partidos_ativos = Partido.objects.filter(status_situacao='Ativo').count()
    
    context = {
        'partidos': partidos_page,
        'total_partidos': total_partidos,
        'partidos_ativos': partidos_ativos,
        'situacoes': Partido.objects.values_list('status_situacao', flat=True).distinct(),
    }
    return render(request, 'legislative_monitor/partidos_list.html', context)


def detalhe_partido(request, sigla):
    """Exibe detalhes de um partido"""
    from .models import Partido
    from django.db.models import Count, Q
    
    partido = get_object_or_404(Partido, sigla=sigla)
    
    # Deputados do partido
    deputados = partido.deputados.select_related(
        'uf_representacao', 'sexo'
    ).all()
    
    # Proposições dos deputados do partido
    proposicoes = Proposicao.objects.filter(
        autor__sigla_partido=partido
    ).select_related('tipo', 'autor')[:10]
    
    # Estatísticas
    total_deputados = deputados.count()
    
    # Distribuição por UF
    deputados_por_uf = deputados.values('uf_representacao__sigla').annotate(
        total=Count('id')
    ).order_by('-total')[:10]
    
    # Distribuição por sexo
    deputados_por_sexo = deputados.values('sexo__nome').annotate(
        total=Count('id')
    ).order_by('-total')
    
    context = {
        'partido': partido,
        'deputados': deputados[:20],  # Primeiros 20 para exibição
        'total_deputados': total_deputados,
        'proposicoes': proposicoes,
        'deputados_por_uf': deputados_por_uf,
        'deputados_por_sexo': deputados_por_sexo,
    }
    return render(request, 'legislative_monitor/partido_detail.html', context)
