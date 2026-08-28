from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance
from .forms import AttendanceForm
from .services import calculate_attendance_stats, calculate_subject_attendance


@login_required
def attendance_list(request):
    semester = request.active_semester
    attendances = Attendance.objects.filter(user=request.user, semester=semester) if semester else Attendance.objects.none()

    subject_filter = request.GET.get('subject', '')
    if subject_filter:
        attendances = attendances.filter(subject_id=subject_filter)

    from apps.subjects.models import Subject
    subjects = Subject.objects.filter(user=request.user, semester=semester) if semester else Subject.objects.none()

    stats = calculate_attendance_stats(request.user, semester) if semester else None
    subject_stats = calculate_subject_attendance(request.user, semester) if semester else []

    context = {
        'attendances': attendances,
        'subjects': subjects,
        'semester': semester,
        'stats': stats,
        'subject_stats': subject_stats,
    }
    return render(request, 'attendance/attendance_list.html', context)


@login_required
def attendance_create(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')

    if request.method == 'POST':
        form = AttendanceForm(request.POST, user=request.user, semester=semester)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.semester = semester
            attendance.save()
            messages.success(request, 'Attendance recorded!')
            return redirect('attendance:list')
    else:
        form = AttendanceForm(user=request.user, semester=semester)
    return render(request, 'attendance/attendance_form.html', {'form': form, 'action': 'Create'})


@login_required
def attendance_update(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk, user=request.user)
    semester = attendance.semester

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance, user=request.user, semester=semester)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance updated!')
            return redirect('attendance:list')
    else:
        form = AttendanceForm(instance=attendance, user=request.user, semester=semester)
    return render(request, 'attendance/attendance_form.html', {'form': form, 'action': 'Update'})


@login_required
def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk, user=request.user)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance record deleted!')
        return redirect('attendance:list')
    return render(request, 'attendance/attendance_confirm_delete.html', {'attendance': attendance})
