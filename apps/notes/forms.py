from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'subject', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'comma-separated tags'}),
        }
    
    def __init__(self, *args, user=None, semester=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and semester:
            self.fields['subject'].queryset = self.fields['subject'].queryset.filter(user=user, semester=semester)