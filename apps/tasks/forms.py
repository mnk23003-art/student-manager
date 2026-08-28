from django import forms
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'subject', 'deadline', 'priority', 'status', 'estimated_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'estimated_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
        }
    
    def __init__(self, *args, user=None, semester=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and semester:
            self.fields['subject'].queryset = self.fields['subject'].queryset.filter(user=user, semester=semester)


class QuickTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'subject', 'deadline', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, user=None, semester=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and semester:
            self.fields['subject'].queryset = self.fields['subject'].queryset.filter(user=user, semester=semester)
