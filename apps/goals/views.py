from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Goal
from .forms import GoalForm


@login_required
def goal_list(request):
    semester = request.active_semester
    goals = Goal.objects.filter(user=request.user, semester=semester) if semester else Goal.objects.none()

    status_filter = request.GET.get('status', '')
    if status_filter:
        goals = goals.filter(status=status_filter)

    context = {
        'goals': goals,
        'semester': semester,
        'completed_count': goals.filter(status='completed').count(),
        'in_progress_count': goals.filter(status='in_progress').count(),
    }
    return render(request, 'goals/goal_list.html', context)


@login_required
def goal_detail(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    return render(request, 'goals/goal_detail.html', {'goal': goal})


@login_required
def goal_create(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')

    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.semester = semester
            goal.save()
            messages.success(request, 'Goal created!')
            return redirect('goals:detail', pk=goal.pk)
    else:
        form = GoalForm()
    return render(request, 'goals/goal_form.html', {'form': form, 'action': 'Create'})


@login_required
def goal_update(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Goal updated!')
            return redirect('goals:detail', pk=goal.pk)
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/goal_form.html', {'form': form, 'action': 'Update'})


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted!')
        return redirect('goals:list')
    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})


@login_required
def goal_update_progress(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            progress = int(data.get('progress', 0))
            progress = max(0, min(100, progress))
            goal.progress = progress
            if progress == 100:
                goal.status = 'completed'
            elif progress > 0:
                goal.status = 'in_progress'
            goal.save()
            return JsonResponse({'success': True, 'progress': goal.progress, 'status': goal.status})
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'success': False}, status=400)
    return JsonResponse({'success': False}, status=405)
