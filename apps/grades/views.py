from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Grade
from .forms import GradeForm, GradePredictionForm
from .services import calculate_average_grade, calculate_weighted_average, calculate_gpa, calculate_subject_grades, predict_needed_grade


@login_required
def grade_list(request):
    semester = request.active_semester
    grades = Grade.objects.filter(user=request.user, semester=semester) if semester else Grade.objects.none()

    subject_filter = request.GET.get('subject', '')
    if subject_filter:
        grades = grades.filter(subject_id=subject_filter)

    from apps.subjects.models import Subject
    subjects = Subject.objects.filter(user=request.user, semester=semester) if semester else Subject.objects.none()

    user_settings = getattr(request.user, 'settings', None)
    grading_system = user_settings.grading_system if user_settings else 'percentage'

    context = {
        'grades': grades,
        'subjects': subjects,
        'semester': semester,
        'avg_grade': calculate_average_grade(request.user, semester) if semester else None,
        'weighted_avg': calculate_weighted_average(request.user, semester) if semester else None,
        'gpa': calculate_gpa(request.user, semester, grading_system) if semester else None,
        'subject_grades': calculate_subject_grades(request.user, semester) if semester else [],
        'grading_system': grading_system,
    }
    return render(request, 'grades/grade_list.html', context)


@login_required
def grade_create(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')

    if request.method == 'POST':
        form = GradeForm(request.POST, user=request.user, semester=semester)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.user = request.user
            grade.semester = semester
            grade.save()
            messages.success(request, 'Grade added!')
            return redirect('grades:list')
    else:
        form = GradeForm(user=request.user, semester=semester)
    return render(request, 'grades/grade_form.html', {'form': form, 'action': 'Create'})


@login_required
def grade_update(request, pk):
    grade = get_object_or_404(Grade, pk=pk, user=request.user)
    semester = grade.semester

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade, user=request.user, semester=semester)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade updated!')
            return redirect('grades:list')
    else:
        form = GradeForm(instance=grade, user=request.user, semester=semester)
    return render(request, 'grades/grade_form.html', {'form': form, 'action': 'Update'})


@login_required
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk, user=request.user)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade deleted!')
        return redirect('grades:list')
    return render(request, 'grades/grade_confirm_delete.html', {'grade': grade})


@login_required
def grade_prediction(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')

    result = None
    if request.method == 'POST':
        form = GradePredictionForm(request.POST, user=request.user, semester=semester)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            desired = form.cleaned_data['desired_average']
            result = predict_needed_grade(request.user, semester, subject, desired)
    else:
        form = GradePredictionForm(user=request.user, semester=semester)

    return render(request, 'grades/grade_prediction.html', {'form': form, 'result': result})
