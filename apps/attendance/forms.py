from django import forms
from django.utils import timezone
from .models import Attendance


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['subject', 'date', 'status', 'notes']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, user=None, semester=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and semester:
            self.fields['subject'].queryset = self.fields['subject'].queryset.filter(user=user, semester=semester)


class BulkAttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), initial=timezone.now)

    def __init__(self, *args, user=None, semester=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and semester:
            from apps.subjects.models import Subject
            subjects = Subject.objects.filter(user=user, semester=semester)
            for subject in subjects:
                self.fields[f'subject_{subject.pk}'] = forms.ChoiceField(
                    choices=Attendance.STATUS_CHOICES,
                    initial='present',
                    label=subject.name,
                    widget=forms.Select(attrs={'class': 'form-select'})
                )
