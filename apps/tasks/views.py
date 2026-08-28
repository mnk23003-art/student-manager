from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Sum
from .models import Task
from .forms import TaskForm, QuickTaskForm


@login_required
def task_list(request):
    semester = request.active_semester
    tasks = Task.objects.filter(user=request.user, semester=semester) if semester else Task.objects.none()
    
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    subject_filter = request.GET.get('subject', '')
    quick_filter = request.GET.get('filter', '')
    search = request.GET.get('q', '')
    
    if search:
        tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if subject_filter:
        tasks = tasks.filter(subject_id=subject_filter)
    
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)
    week_end = today + timezone.timedelta(days=7)
    
    if quick_filter == 'today':
        tasks = tasks.filter(deadline__date=today)
    elif quick_filter == 'tomorrow':
        tasks = tasks.filter(deadline__date=tomorrow)
    elif quick_filter == 'week':
        tasks = tasks.filter(deadline__date__lte=week_end, deadline__date__gte=today)
    elif quick_filter == 'overdue':
        tasks = tasks.filter(deadline__lt=timezone.now(), status__in=['todo', 'in_progress'])
    elif quick_filter == 'completed':
        tasks = tasks.filter(status='completed')
    
    from apps.subjects.models import Subject
    subjects = Subject.objects.filter(user=request.user, semester=semester) if semester else Subject.objects.none()
    
    stats = {
        'total': Task.objects.filter(user=request.user, semester=semester).count() if semester else 0,
        'todo': Task.objects.filter(user=request.user, semester=semester, status='todo').count() if semester else 0,
        'in_progress': Task.objects.filter(user=request.user, semester=semester, status='in_progress').count() if semester else 0,
        'completed': Task.objects.filter(user=request.user, semester=semester, status='completed').count() if semester else 0,
        'overdue': Task.objects.filter(user=request.user, semester=semester, deadline__lt=timezone.now(), status__in=['todo', 'in_progress']).count() if semester else 0,
    }
    
    context = {
        'tasks': tasks,
        'subjects': subjects,
        'stats': stats,
        'current_status': status_filter,
        'current_priority': priority_filter,
        'current_subject': subject_filter,
        'current_filter': quick_filter,
        'search_query': search,
        'semester': semester,
    }
    
    if request.headers.get('HX-Request'):
        return render(request, 'tasks/task_list_partial.html', context)
    
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user, semester=semester)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.semester = semester
            task.save()
            messages.success(request, 'Task created!')
            
            if request.headers.get('HX-Request'):
                return redirect('tasks:list')
            return redirect('tasks:detail', pk=task.pk)
    else:
        form = TaskForm(user=request.user, semester=semester)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    semester = task.semester
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user, semester=semester)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated!')
            return redirect('tasks:detail', pk=task.pk)
    else:
        form = TaskForm(instance=task, user=request.user, semester=semester)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted!')
        return redirect('tasks:list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.complete()
        if request.headers.get('HX-Request'):
            return render(request, 'tasks/task_item_partial.html', {'task': task})
        messages.success(request, f'Task "{task.title}" completed!')
    return redirect('tasks:list')


@login_required
def task_toggle_status(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        if task.status == 'completed':
            task.status = 'todo'
            task.completed_at = None
        else:
            task.status = 'completed'
            task.completed_at = timezone.now()
        task.save()
        
        if request.headers.get('HX-Request'):
            return render(request, 'tasks/task_item_partial.html', {'task': task})
    return redirect('tasks:list')


@login_required
def quick_task_create(request):
    semester = request.active_semester
    if request.method == 'POST' and semester:
        form = QuickTaskForm(request.POST, user=request.user, semester=semester)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.semester = semester
            task.save()
            return JsonResponse({'success': True, 'task_id': task.pk, 'task_title': task.title})
    return JsonResponse({'success': False, 'errors': form.errors if form else {}})


@login_required
def task_workload(request):
    semester = request.active_semester
    if not semester:
        return JsonResponse({'today': 0, 'week': 0})
    
    today = timezone.now().date()
    week_end = today + timezone.timedelta(days=7)
    
    today_minutes = Task.objects.filter(
        user=request.user, semester=semester,
        deadline__date=today, estimated_time__isnull=False,
        status__in=['todo', 'in_progress']
    ).aggregate(total=Sum('estimated_time'))['total'] or 0
    
    week_minutes = Task.objects.filter(
        user=request.user, semester=semester,
        deadline__date__lte=week_end, deadline__date__gte=today,
        estimated_time__isnull=False,
        status__in=['todo', 'in_progress']
    ).aggregate(total=Sum('estimated_time'))['total'] or 0
    
    return JsonResponse({
        'today': f"{today_minutes // 60}h {today_minutes % 60}m",
        'week': f"{week_minutes // 60}h {week_minutes % 60}m",
    })
