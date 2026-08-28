from django import forms
from .models import ScheduleItem


class ScheduleItemForm(forms.ModelForm):
    class Meta:
        model = ScheduleItem
        fields = ['subject', 'day_of_week', 'start_time', 'end_time', 'lesson_type', 'teacher', 'room', 'notes']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'lesson_type': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.TextInput(attrs={'class': 'form-control'}),
            'room': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def __init__(self, *args, user=None, semester=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and semester:
            self.fields['subject'].queryset = self.fields['subject'].queryset.filter(user=user, semester=semester)
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned_data
    
    def clean_end_time(self):
        start = self.cleaned_data.get('start_time')
        end = self.cleaned_data.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError('End time must be after start time.')
        return end
