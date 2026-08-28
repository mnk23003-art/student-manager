from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Semester
from .forms import SemesterForm


@login_required
def semester_list(request):
    semesters = Semester.objects.filter(user=request.user)
    active = semesters.filter(is_active=True).first()
    return render(request, 'semesters/semester_list.html', {
        'semesters': semesters,
        'active_semester': active,
    })


@login_required
def semester_create(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            semester = form.save(commit=False)
            semester.user = request.user
            if not Semester.objects.filter(user=request.user, is_active=True).exists():
                semester.is_active = True
            semester.save()
            messages.success(request, f'Semester "{semester.name}" created!')
            return redirect('semesters:list')
    else:
        form = SemesterForm()
    return render(request, 'semesters/semester_form.html', {'form': form, 'action': 'Create'})


@login_required
def semester_update(request, pk):
    semester = get_object_or_404(Semester, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            messages.success(request, f'Semester "{semester.name}" updated!')
            return redirect('semesters:list')
    else:
        form = SemesterForm(instance=semester)
    return render(request, 'semesters/semester_form.html', {'form': form, 'action': 'Update'})


@login_required
def semester_delete(request, pk):
    semester = get_object_or_404(Semester, pk=pk, user=request.user)
    if request.method == 'POST':
        name = semester.name
        semester.delete()
        messages.success(request, f'Semester "{name}" deleted!')
        return redirect('semesters:list')
    return render(request, 'semesters/semester_confirm_delete.html', {'semester': semester})


@login_required
def semester_set_active(request, pk):
    semester = get_object_or_404(Semester, pk=pk, user=request.user)
    Semester.objects.filter(user=request.user, is_active=True).update(is_active=False)
    semester.is_active = True
    semester.save()
    messages.success(request, f'"{semester.name}" is now active!')

    if request.headers.get('HX-Request'):
        return render(request, 'semesters/semester_list_partial.html', {
            'semesters': Semester.objects.filter(user=request.user),
            'active_semester': semester,
        })
    return redirect('semesters:list')
