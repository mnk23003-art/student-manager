from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .services import get_dashboard_data


@login_required
def dashboard_view(request):
    semester = request.active_semester
    data = get_dashboard_data(request.user, semester)
    
    hour = timezone.now().hour
    if hour < 12:
        greeting = _('Доброе утро')
    elif hour < 18:
        greeting = _('Добрый день')
    else:
        greeting = _('Добрый вечер')
    
    # Chart data for grades over time
    chart_data = {}
    if semester:
        from apps.grades.models import Grade
        from django.db.models import Avg
        from datetime import timedelta
        
        today = timezone.now().date()
        months = []
        avg_scores = []
        for i in range(5, -1, -1):
            month_start = today.replace(day=1) - timedelta(days=30 * i)
            month_end = (month_start + timedelta(days=32)).replace(day=1)
            month_grades = Grade.objects.filter(
                user=request.user, semester=semester,
                date__gte=month_start, date__lt=month_end
            )
            avg = month_grades.aggregate(avg=Avg('score'))['avg']
            months.append(month_start.strftime('%b'))
            avg_scores.append(round(avg, 1) if avg else 0)
        
        chart_data['months'] = months
        chart_data['avg_scores'] = avg_scores
        
        # Task completion chart
        from apps.tasks.models import Task
        task_stats = {'completed': 0, 'in_progress': 0, 'todo': 0}
        tasks = Task.objects.filter(user=request.user, semester=semester)
        for status, count in tasks.values_list('status').distinct():
            if status in task_stats:
                task_stats[status] = tasks.filter(status=status).count()
        
        chart_data['task_completed'] = task_stats['completed']
        chart_data['task_in_progress'] = task_stats['in_progress']
        chart_data['task_todo'] = task_stats['todo']
        
        # Attendance chart by subject
        from apps.attendance.models import Attendance
        from apps.subjects.models import Subject
        attendance_by_subject = []
        subjects = Subject.objects.filter(user=request.user, semester=semester)
        for subject in subjects:
            total = Attendance.objects.filter(user=request.user, semester=semester, schedule_item__subject=subject).count()
            present = Attendance.objects.filter(user=request.user, semester=semester, schedule_item__subject=subject, is_present=True).count()
            pct = round(present / total * 100) if total > 0 else 0
            attendance_by_subject.append({'name': subject.name[:12], 'percentage': pct, 'color': subject.color})
        
        chart_data['attendance_by_subject'] = attendance_by_subject
    
    context = {
        **data,
        'greeting': greeting,
        'user': request.user,
        'semester': semester,
        'chart_data': chart_data,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def dashboard_redirect(request):
    return redirect('dashboard:index')
