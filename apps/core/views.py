from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.subjects.models import Subject
from apps.tasks.models import Task
from apps.grades.models import Grade
from apps.notes.models import Note
from apps.exams.models import Exam
from .import_export import (
    export_tasks_to_csv, export_tasks_to_xlsx,
    export_grades_to_csv, export_grades_to_xlsx, export_grades_to_pdf,
    export_attendance_to_csv, export_schedule_to_csv,
    import_tasks_from_csv, import_grades_from_csv,
)


@login_required
def global_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    user = request.user

    if query:
        subjects = Subject.objects.filter(user=user, name__icontains=query)[:5]
        tasks = Task.objects.filter(user=user, title__icontains=query)[:5]
        grades = Grade.objects.filter(user=user, title__icontains=query)[:5]
        notes = Note.objects.filter(user=user).filter(Q(title__icontains=query) | Q(content__icontains=query))[:5]
        exams = Exam.objects.filter(user=user, title__icontains=query)[:5]

        for s in subjects:
            results.append({'type': 'subject', 'title': s.name, 'url': f'/subjects/{s.pk}/', 'icon': 'book'})
        for t in tasks:
            results.append({'type': 'task', 'title': t.title, 'url': f'/tasks/{t.pk}/', 'icon': 'check-square'})
        for g in grades:
            results.append({'type': 'grade', 'title': g.title, 'url': '/grades/', 'icon': 'award'})
        for n in notes:
            results.append({'type': 'note', 'title': n.title, 'url': f'/notes/{n.pk}/', 'icon': 'file-text'})
        for e in exams:
            results.append({'type': 'exam', 'title': e.title, 'url': f'/exams/{e.pk}/', 'icon': 'clipboard'})

    if request.headers.get('HX-Request'):
        return render(request, 'core/search_results.html', {'results': results, 'query': query})

    return render(request, 'core/search.html', {'results': results, 'query': query})


@login_required
def export_view(request):
    semester = request.active_semester
    export_type = request.GET.get('type', '')
    file_format = request.GET.get('format', 'csv')

    if not semester:
        messages.warning(request, 'No active semester.')
        return redirect('dashboard:index')

    if export_type == 'tasks':
        from apps.tasks.models import Task
        queryset = Task.objects.filter(user=request.user, semester=semester)
        if file_format == 'xlsx':
            return export_tasks_to_xlsx(queryset)
        return export_tasks_to_csv(queryset)
    elif export_type == 'grades':
        from apps.grades.models import Grade
        queryset = Grade.objects.filter(user=request.user, semester=semester)
        if file_format == 'xlsx':
            return export_grades_to_xlsx(queryset)
        elif file_format == 'pdf':
            return export_grades_to_pdf(queryset, request.user)
        return export_grades_to_csv(queryset)
    elif export_type == 'attendance':
        from apps.attendance.models import Attendance
        queryset = Attendance.objects.filter(user=request.user, semester=semester)
        return export_attendance_to_csv(queryset)
    elif export_type == 'schedule':
        from apps.schedule.models import ScheduleItem
        queryset = ScheduleItem.objects.filter(user=request.user, semester=semester)
        return export_schedule_to_csv(queryset)

    return redirect('dashboard:index')


@login_required
def import_view(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'No active semester.')
        return redirect('dashboard:index')

    if request.method == 'POST':
        import_type = request.POST.get('import_type', '')
        file = request.FILES.get('file')

        if not file:
            messages.error(request, 'Please select a file.')
            return redirect('core:import_view')

        # Validate file type
        if not file.name.endswith('.csv'):
            messages.error(request, 'Only CSV files are allowed.')
            return redirect('core:import_view')

        # Validate file size (max 2MB)
        if file.size > 2 * 1024 * 1024:
            messages.error(request, 'File too large. Maximum size is 2MB.')
            return redirect('core:import_view')

        # Validate import type
        if import_type not in ('tasks', 'grades'):
            messages.error(request, 'Invalid import type.')
            return redirect('core:import_view')

        try:
            content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            messages.error(request, 'File encoding error. Please use UTF-8.')
            return redirect('core:import_view')

        if import_type == 'tasks':
            imported, errors = import_tasks_from_csv(content, request.user, semester)
        elif import_type == 'grades':
            imported, errors = import_grades_from_csv(content, request.user, semester)

        if imported > 0:
            messages.success(request, f'Successfully imported {imported} {import_type}.')
        if errors:
            for error in errors[:5]:
                messages.warning(request, error)

        return redirect('dashboard:index')

    return render(request, 'core/import_export.html')


@login_required
def backup_list(request):
    from .backup import list_backups, get_backup_size_display
    backups = list_backups()
    for b in backups:
        b['size_display'] = get_backup_size_display(b['size'])
    return render(request, 'core/backup_list.html', {'backups': backups})


@login_required
def backup_create(request):
    if request.method == 'POST':
        from .backup import create_backup
        metadata = create_backup()
        messages.success(request, f'Backup created: {metadata["filename"]}')
    return redirect('core:backup_list')


@login_required
def backup_restore(request, filename):
    if request.method == 'POST':
        from .backup import restore_backup
        try:
            restore_backup(filename)
            messages.success(request, 'Backup restored successfully! Please log in again.')
            return redirect('accounts:login')
        except ValueError as e:
            messages.error(request, str(e))
        except FileNotFoundError:
            messages.error(request, 'Backup file not found.')
    return redirect('core:backup_list')


@login_required
def backup_delete(request, filename):
    if request.method == 'POST':
        from .backup import delete_backup
        try:
            if delete_backup(filename):
                messages.success(request, 'Backup deleted.')
            else:
                messages.error(request, 'Backup not found.')
        except ValueError as e:
            messages.error(request, str(e))
    return redirect('core:backup_list')
