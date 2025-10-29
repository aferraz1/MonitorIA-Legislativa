from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Noticia, Categoria, Tag


def index(request):
    """Página inicial do portal de notícias"""
    noticias_destaque = Noticia.objects.filter(
        status='PUBLICADA',
        destaque=True
    ).order_by('-data_publicacao')[:3]
    
    noticias_recentes = Noticia.objects.filter(
        status='PUBLICADA'
    ).order_by('-data_publicacao')[:10]
    
    categorias = Categoria.objects.all()
    
    context = {
        'noticias_destaque': noticias_destaque,
        'noticias_recentes': noticias_recentes,
        'categorias': categorias,
    }
    return render(request, 'news_portal/index.html', context)


def listar_noticias(request):
    """Lista todas as notícias publicadas"""
    noticias = Noticia.objects.filter(status='PUBLICADA').order_by('-data_publicacao')
    
    # Filtros
    categoria_slug = request.GET.get('categoria')
    tag_slug = request.GET.get('tag')
    busca = request.GET.get('q')
    
    if categoria_slug:
        noticias = noticias.filter(categoria__slug=categoria_slug)
    if tag_slug:
        noticias = noticias.filter(tags__slug=tag_slug)
    if busca:
        noticias = noticias.filter(
            Q(titulo__icontains=busca) |
            Q(conteudo__icontains=busca) |
            Q(resumo__icontains=busca)
        )
    
    paginator = Paginator(noticias, 12)
    page = request.GET.get('page')
    noticias_page = paginator.get_page(page)
    
    context = {
        'noticias': noticias_page,
        'categorias': Categoria.objects.all(),
    }
    return render(request, 'news_portal/noticias_list.html', context)


def detalhe_noticia(request, slug):
    """Exibe detalhes de uma notícia"""
    noticia = get_object_or_404(Noticia, slug=slug, status='PUBLICADA')
    
    # Incrementa visualizações
    noticia.visualizacoes += 1
    noticia.save(update_fields=['visualizacoes'])
    
    # Notícias relacionadas
    noticias_relacionadas = Noticia.objects.filter(
        status='PUBLICADA',
        categoria=noticia.categoria
    ).exclude(id=noticia.id)[:4]
    
    context = {
        'noticia': noticia,
        'noticias_relacionadas': noticias_relacionadas,
    }
    return render(request, 'news_portal/noticia_detail.html', context)


def noticias_por_categoria(request, slug):
    """Lista notícias de uma categoria específica"""
    categoria = get_object_or_404(Categoria, slug=slug)
    noticias = Noticia.objects.filter(
        status='PUBLICADA',
        categoria=categoria
    ).order_by('-data_publicacao')
    
    paginator = Paginator(noticias, 12)
    page = request.GET.get('page')
    noticias_page = paginator.get_page(page)
    
    context = {
        'categoria': categoria,
        'noticias': noticias_page,
        'categorias': Categoria.objects.all(),
    }
    return render(request, 'news_portal/categoria.html', context)

