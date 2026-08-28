from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import CalendarEvent
from .forms import CalendarEventForm


@login_required
def calendar_view(request):
    semester = request.active_semester

    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    view_mode = request.GET.get('mode', 'month')

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    events = CalendarEvent.objects.filter(
        user=request.user,
        date__gte=first_day,
        date__lte=last_day,
    )
    if semester:
        events = events.filter(semester=semester)

    from apps.schedule.models import ScheduleItem
    schedule_items = ScheduleItem.objects.filter(user=request.user, semester=semester) if semester else ScheduleItem.objects.none()

    from apps.tasks.models import Task
    tasks = Task.objects.filter(
        user=request.user, semester=semester,
        deadline__date__gte=first_day, deadline__date__lte=last_day,
        status__in=['todo', 'in_progress']
    ) if semester else Task.objects.none()

    from apps.exams.models import Exam
    exams = Exam.objects.filter(
        user=request.user, semester=semester,
        date__gte=first_day, date__lte=last_day
    ) if semester else Exam.objects.none()

    cal_days = []
    current = first_day - timedelta(days=first_day.weekday())
    while current <= last_day + timedelta(days=6):
        day_events = events.filter(date=current)
        day_tasks = tasks.filter(deadline__date=current)
        day_exams = exams.filter(date=current)
        cal_days.append({
            'date': current,
            'is_current_month': first_day.month == current.month,
            'is_today': current == timezone.now().date(),
            'events': day_events,
            'tasks': day_tasks,
            'exams': day_exams,
        })
        current += timedelta(days=1)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    month_name = first_day.strftime('%B %Y')

    context = {
        'calendar_days': cal_days,
        'year': year,
        'month': month,
        'month_name': month_name,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'view_mode': view_mode,
        'semester': semester,
        'events': events,
        'today': timezone.now().date(),
    }
    return render(request, 'calendar/calendar.html', context)


@login_required
def event_create(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')

    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.semester = semester
            event.save()
            messages.success(request, 'Event created!')
            return redirect('calendar:view')
    else:
        form = CalendarEventForm()
        if request.GET.get('date'):
            form.fields['date'].initial = request.GET.get('date')
    return render(request, 'calendar/event_form.html', {'form': form, 'action': 'Create'})


@login_required
def event_update(request, pk):
    event = get_object_or_404(CalendarEvent, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CalendarEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated!')
            return redirect('calendar:view')
    else:
        form = CalendarEventForm(instance=event)
    return render(request, 'calendar/event_form.html', {'form': form, 'action': 'Update'})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(CalendarEvent, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted!')
        return redirect('calendar:view')
    return render(request, 'calendar/event_confirm_delete.html', {'event': event})
