from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject
from .forms import SubjectForm


@login_required
def subject_list(request):
    semester = request.active_semester
    subjects = Subject.objects.filter(user=request.user, semester=semester) if semester else Subject.objects.none()
    return render(request, 'subjects/subject_list.html', {'subjects': subjects, 'semester': semester})


@login_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    from apps.tasks.models import Task
    from apps.grades.models import Grade
    from apps.notes.models import Note
    
    tasks = Task.objects.filter(user=request.user, subject=subject).order_by('-created_at')[:10]
    grades = Grade.objects.filter(user=request.user, subject=subject).order_by('-date')[:10]
    notes = Note.objects.filter(user=request.user, subject=subject).order_by('-created_at')[:5]
    
    context = {
        'subject': subject,
        'tasks': tasks,
        'grades': grades,
        'notes': notes,
        'avg_grade': subject.get_average_grade(),
        'attendance_pct': subject.get_attendance_percentage(),
        'overdue_count': subject.get_overdue_tasks_count(),
    }
    return render(request, 'subjects/subject_detail.html', context)


@login_required
def subject_create(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.semester = semester
            subject.save()
            messages.success(request, f'Subject "{subject.name}" created!')
            return redirect('subjects:detail', pk=subject.pk)
    else:
        form = SubjectForm()
    return render(request, 'subjects/subject_form.html', {'form': form, 'action': 'Create'})


@login_required
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, f'Subject "{subject.name}" updated!')
            return redirect('subjects:detail', pk=subject.pk)
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'subjects/subject_form.html', {'form': form, 'action': 'Update'})


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk, user=request.user)
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f'Subject "{name}" deleted!')
        return redirect('subjects:list')
    return render(request, 'subjects/subject_confirm_delete.html', {'subject': subject})
