from django import forms
from .models import Exam


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'title', 'date', 'time', 'location', 'description', 'notes']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, user=None, semester=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and semester:
            self.fields['subject'].queryset = self.fields['subject'].queryset.filter(user=user, semester=semester)
