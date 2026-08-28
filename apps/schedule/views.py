from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ScheduleItem
from .forms import ScheduleItemForm


@login_required
def schedule_view(request):
    semester = request.active_semester
    items = ScheduleItem.objects.filter(user=request.user, semester=semester) if semester else ScheduleItem.objects.none()
    
    days = {}
    for day_num, day_name in ScheduleItem.DAY_CHOICES:
        days[day_num] = {
            'name': day_name,
            'items': items.filter(day_of_week=day_num).order_by('start_time'),
        }
    
    return render(request, 'schedule/schedule.html', {
        'days': days,
        'semester': semester,
        'day_choices': ScheduleItem.DAY_CHOICES,
    })


@login_required
def schedule_item_create(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')
    
    if request.method == 'POST':
        form = ScheduleItemForm(request.POST, user=request.user, semester=semester)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.semester = semester
            
            if item.has_conflict():
                conflicts = item.get_conflicting_items()
                conflict_list = ', '.join([f"{c.subject.name} ({c.start_time}-{c.end_time})" for c in conflicts])
                messages.error(request, f'Schedule conflict detected with: {conflict_list}')
                return render(request, 'schedule/schedule_form.html', {'form': form, 'action': 'Create'})
            
            item.save()
            messages.success(request, 'Schedule item created!')
            return redirect('schedule:view')
    else:
        form = ScheduleItemForm(user=request.user, semester=semester)
    return render(request, 'schedule/schedule_form.html', {'form': form, 'action': 'Create'})


@login_required
def schedule_item_update(request, pk):
    item = get_object_or_404(ScheduleItem, pk=pk, user=request.user)
    semester = item.semester
    
    if request.method == 'POST':
        form = ScheduleItemForm(request.POST, instance=item, user=request.user, semester=semester)
        if form.is_valid():
            updated_item = form.save(commit=False)
            updated_item.user = request.user
            
            if updated_item.has_conflict():
                conflicts = updated_item.get_conflicting_items()
                conflict_list = ', '.join([f"{c.subject.name} ({c.start_time}-{c.end_time})" for c in conflicts])
                messages.error(request, f'Schedule conflict detected with: {conflict_list}')
                return render(request, 'schedule/schedule_form.html', {'form': form, 'action': 'Update'})
            
            updated_item.save()
            messages.success(request, 'Schedule item updated!')
            return redirect('schedule:view')
    else:
        form = ScheduleItemForm(instance=item, user=request.user, semester=semester)
    return render(request, 'schedule/schedule_form.html', {'form': form, 'action': 'Update'})


@login_required
def schedule_item_delete(request, pk):
    item = get_object_or_404(ScheduleItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Schedule item deleted!')
        return redirect('schedule:view')
    return render(request, 'schedule/schedule_confirm_delete.html', {'item': item})


@login_required
def schedule_check_conflicts(request):
    semester = request.active_semester
    if not semester:
        return render(request, 'schedule/conflicts.html', {'conflicts': []})
    
    items = ScheduleItem.objects.filter(user=request.user, semester=semester)
    conflicts = []
    
    for item in items:
        conflicting = item.get_conflicting_items()
        if conflicting.exists():
            conflicts.append({
                'item': item,
                'conflicts': conflicting,
            })
    
    return render(request, 'schedule/conflicts.html', {'conflicts': conflicts})
