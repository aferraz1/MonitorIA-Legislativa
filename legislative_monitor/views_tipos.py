from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from .models import TipoProposicao


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
        
        # Se houver integração com Proposicao, descomentar:
        # context['proposicoes'] = self.object.proposicoes.all()[:10]
        # context['total_proposicoes'] = self.object.proposicoes.count()
        
        return context
