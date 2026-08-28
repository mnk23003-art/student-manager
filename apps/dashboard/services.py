from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum


def get_dashboard_data(user, semester):
    data = {}
    
    if not semester:
        data['has_semester'] = False
        return data
    
    data['has_semester'] = True
    today = timezone.now().date()
    now = timezone.now()
    
    from apps.schedule.models import ScheduleItem
    weekday = today.weekday()
    data['today_classes'] = ScheduleItem.objects.filter(
        user=user, semester=semester, day_of_week=weekday
    ).order_by('start_time')
    
    from apps.tasks.models import Task
    data['overdue_tasks'] = Task.objects.filter(
        user=user, semester=semester,
        deadline__lt=now,
        status__in=['todo', 'in_progress']
    ).order_by('deadline')[:5]
    
    data['upcoming_tasks'] = Task.objects.filter(
        user=user, semester=semester,
        deadline__gte=now,
        status__in=['todo', 'in_progress']
    ).order_by('deadline')[:5]
    
    from apps.exams.models import Exam
    data['upcoming_exams'] = Exam.objects.filter(
        user=user, semester=semester,
        date__gte=today
    ).order_by('date')[:3]
    
    from apps.grades.services import calculate_average_grade, calculate_gpa
    data['avg_grade'] = calculate_average_grade(user, semester)
    
    from apps.attendance.services import calculate_attendance_stats
    data['attendance_stats'] = calculate_attendance_stats(user, semester)
    
    data['semester_progress'] = semester.get_progress()
    data['semester_days_left'] = semester.days_left()
    
    workload_minutes = Task.objects.filter(
        user=user, semester=semester,
        deadline__date=today,
        estimated_time__isnull=False,
        status__in=['todo', 'in_progress']
    ).aggregate(total=Sum('estimated_time'))['total'] or 0
    
    hours = workload_minutes // 60
    mins = workload_minutes % 60
    data['today_workload'] = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
    
    from apps.productivity.models import FocusSession
    today_focus = FocusSession.objects.filter(
        user=user, start_time__date=today, completed=True
    ).aggregate(total=Sum('duration'))['total'] or 0
    
    focus_mins = today_focus // 60
    data['today_focus'] = f"{focus_mins}m"
    
    total_tasks = Task.objects.filter(user=user, semester=semester).count()
    completed_tasks = Task.objects.filter(user=user, semester=semester, status='completed').count()
    data['task_completion_rate'] = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
    
    return data
