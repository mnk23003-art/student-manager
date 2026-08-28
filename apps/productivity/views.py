from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta
from .models import FocusSession, PomodoroSettings
from .forms import PomodoroSettingsForm


@login_required
def productivity_view(request):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    today_sessions = FocusSession.objects.filter(
        user=request.user, start_time__date=today, completed=True
    )
    week_sessions = FocusSession.objects.filter(
        user=request.user, start_time__date__gte=week_start, completed=True
    )
    
    today_seconds = today_sessions.aggregate(total=Sum('duration'))['total'] or 0
    week_seconds = week_sessions.aggregate(total=Sum('duration'))['total'] or 0
    today_count = today_sessions.count()
    week_count = week_sessions.count()
    
    settings_obj, _ = PomodoroSettings.objects.get_or_create(user=request.user)
    
    context = {
        'today_focus': f"{today_seconds // 3600}h {(today_seconds % 3600) // 60}m" if today_seconds >= 3600 else f"{today_seconds // 60}m",
        'week_focus': f"{week_seconds // 3600}h {(week_seconds % 3600) // 60}m" if week_seconds >= 3600 else f"{week_seconds // 60}m",
        'today_sessions': today_count,
        'week_sessions': week_count,
        'settings': settings_obj,
        'recent_sessions': FocusSession.objects.filter(user=request.user)[:10],
    }
    return render(request, 'productivity/productivity.html', context)


@login_required
def start_focus_session(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        task_id = data.get('task_id')
        
        session = FocusSession.objects.create(
            user=request.user,
            task_id=task_id if task_id else None,
            start_time=timezone.now(),
        )
        return JsonResponse({
            'success': True,
            'session_id': session.pk,
            'start_time': session.start_time.isoformat(),
        })
    return JsonResponse({'success': False}, status=405)


@login_required
def stop_focus_session(request, pk):
    session = get_object_or_404(FocusSession, pk=pk, user=request.user)
    if request.method == 'POST':
        session.end_time = timezone.now()
        session.duration = int((session.end_time - session.start_time).total_seconds())
        session.completed = True
        session.save()
        return JsonResponse({
            'success': True,
            'duration': session.duration,
            'duration_display': session.get_duration_display(),
        })
    return JsonResponse({'success': False}, status=405)


@login_required
def pomodoro_settings(request):
    settings_obj, _ = PomodoroSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PomodoroSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pomodoro settings updated!')
            return redirect('productivity:view')
    else:
        form = PomodoroSettingsForm(instance=settings_obj)
    
    return render(request, 'productivity/pomodoro_settings.html', {'form': form})
