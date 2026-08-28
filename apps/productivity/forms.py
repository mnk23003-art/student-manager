from django import forms
from .models import PomodoroSettings


class PomodoroSettingsForm(forms.ModelForm):
    class Meta:
        model = PomodoroSettings
        fields = ['focus_duration', 'short_break', 'long_break', 'sessions_before_long']
        widgets = {
            'focus_duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'short_break': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'long_break': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'sessions_before_long': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
