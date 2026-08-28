from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Note
from .forms import NoteForm


@login_required
def note_list(request):
    semester = request.active_semester
    notes = Note.objects.filter(user=request.user, semester=semester) if semester else Note.objects.none()
    
    search = request.GET.get('q', '')
    subject_filter = request.GET.get('subject', '')
    tag_filter = request.GET.get('tag', '')
    
    if search:
        notes = notes.filter(Q(title__icontains=search) | Q(content__icontains=search))
    if subject_filter:
        notes = notes.filter(subject_id=subject_filter)
    if tag_filter:
        notes = notes.filter(tags__icontains=tag_filter)
    
    from apps.subjects.models import Subject
    subjects = Subject.objects.filter(user=request.user, semester=semester) if semester else Subject.objects.none()
    
    all_tags = set()
    for note in Note.objects.filter(user=request.user, semester=semester):
        all_tags.update(note.get_tags_list())
    
    context = {
        'notes': notes,
        'subjects': subjects,
        'all_tags': sorted(all_tags),
        'search_query': search,
        'semester': semester,
    }
    return render(request, 'notes/note_list.html', context)


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def note_create(request):
    semester = request.active_semester
    if not semester:
        messages.warning(request, 'Please create a semester first.')
        return redirect('semesters:create')
    
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user, semester=semester)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.semester = semester
            note.save()
            messages.success(request, 'Note created!')
            return redirect('notes:detail', pk=note.pk)
    else:
        form = NoteForm(user=request.user, semester=semester)
    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Create'})


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    semester = note.semester
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note, user=request.user, semester=semester)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated!')
            return redirect('notes:detail', pk=note.pk)
    else:
        form = NoteForm(instance=note, user=request.user, semester=semester)
    return render(request, 'notes/note_form.html', {'form': form, 'action': 'Update'})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted!')
        return redirect('notes:list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})