from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Equipe, Tarefa, Comentario


@login_required
def index(request):
    """Dashboard de tarefas"""
    minhas_tarefas = Tarefa.objects.filter(responsavel=request.user)
    tarefas_equipe = Tarefa.objects.filter(equipe__membros=request.user)
    
    context = {
        'minhas_tarefas': minhas_tarefas[:10],
        'tarefas_equipe': tarefas_equipe[:10],
    }
    return render(request, 'task_management/index.html', context)


@login_required
def listar_tarefas(request):
    """Lista todas as tarefas"""
    tarefas = Tarefa.objects.filter(equipe__membros=request.user)
    
    # Filtros
    status = request.GET.get('status')
    prioridade = request.GET.get('prioridade')
    equipe_id = request.GET.get('equipe')
    
    if status:
        tarefas = tarefas.filter(status=status)
    if prioridade:
        tarefas = tarefas.filter(prioridade=prioridade)
    if equipe_id:
        tarefas = tarefas.filter(equipe_id=equipe_id)
    
    paginator = Paginator(tarefas, 20)
    page = request.GET.get('page')
    tarefas_page = paginator.get_page(page)
    
    context = {
        'tarefas': tarefas_page,
        'equipes': Equipe.objects.filter(membros=request.user),
    }
    return render(request, 'task_management/tarefas_list.html', context)


@login_required
def detalhe_tarefa(request, pk):
    """Exibe detalhes de uma tarefa"""
    tarefa = get_object_or_404(Tarefa, pk=pk)
    comentarios = tarefa.comentarios.all()
    anexos = tarefa.anexos.all()
    
    context = {
        'tarefa': tarefa,
        'comentarios': comentarios,
        'anexos': anexos,
    }
    return render(request, 'task_management/tarefa_detail.html', context)


@login_required
def minhas_equipes(request):
    """Lista equipes do usuário"""
    equipes = Equipe.objects.filter(membros=request.user)
    
    context = {
        'equipes': equipes,
    }
    return render(request, 'task_management/minhas_equipes.html', context)


@login_required
def detalhe_equipe(request, pk):
    """Exibe detalhes de uma equipe"""
    equipe = get_object_or_404(Equipe, pk=pk, membros=request.user)
    tarefas = equipe.tarefas.all()[:20]
    
    context = {
        'equipe': equipe,
        'tarefas': tarefas,
    }
    return render(request, 'task_management/equipe_detail.html', context)

