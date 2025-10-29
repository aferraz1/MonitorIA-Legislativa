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
