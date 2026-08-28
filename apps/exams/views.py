from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Exam
from .forms import ExamForm


@login_required
def exam_list(request):
    semester = request.active_semester
    exams = Exam.objects.filter(user=request.user, semester=semester) if semester else Exam.objects.none()

    upcoming = exams.filter(date__gte=timezone.now().date())
    past = exams.filter(date__lt=timezone.now().date())

    context = {
        'exams': exams,
        'upcoming': upcoming,
        'past': past,
        'semester': semester,
    }
    return render(request, 'exams/exam_list.html', context)


@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk, user=request.user)
    return render(request, 'exams/exam_detail.html', {'exam': exam})


@login_required
def exam_create(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')

    if request.method == 'POST':
        form = ExamForm(request.POST, user=request.user, semester=semester)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user = request.user
            exam.semester = semester
            exam.save()
            messages.success(request, 'Exam added!')
            return redirect('exams:detail', pk=exam.pk)
    else:
        form = ExamForm(user=request.user, semester=semester)
    return render(request, 'exams/exam_form.html', {'form': form, 'action': 'Create'})


@login_required
def exam_update(request, pk):
    exam = get_object_or_404(Exam, pk=pk, user=request.user)
    semester = exam.semester

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam, user=request.user, semester=semester)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated!')
            return redirect('exams:detail', pk=exam.pk)
    else:
        form = ExamForm(instance=exam, user=request.user, semester=semester)
    return render(request, 'exams/exam_form.html', {'form': form, 'action': 'Update'})


@login_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk, user=request.user)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted!')
        return redirect('exams:list')
    return render(request, 'exams/exam_confirm_delete.html', {'exam': exam})
