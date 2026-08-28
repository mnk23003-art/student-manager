from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Semester


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name', 'academic_year', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2026/2027'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and end <= start:
            raise forms.ValidationError(_('End date must be after start date.'))
        return cleaned_data
