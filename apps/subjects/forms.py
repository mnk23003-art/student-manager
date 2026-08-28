from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'room', 'credits', 'hours', 'color', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.TextInput(attrs={'class': 'form-control'}),
            'room': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
