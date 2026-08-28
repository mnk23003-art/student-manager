from django import forms
from .models import Grade


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['subject', 'title', 'grade_type', 'score', 'max_score', 'weight', 'date', 'comment']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'grade_type': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, user=None, semester=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and semester:
            self.fields['subject'].queryset = self.fields['subject'].queryset.filter(user=user, semester=semester)

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score < 0:
            raise forms.ValidationError('Score cannot be negative.')
        return score

    def clean_max_score(self):
        max_score = self.cleaned_data.get('max_score')
        if max_score <= 0:
            raise forms.ValidationError('Max score must be greater than 0.')
        return max_score

    def clean(self):
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        max_score = cleaned_data.get('max_score')
        if score is not None and max_score is not None and score > max_score:
            raise forms.ValidationError('Score cannot exceed max score.')
        weight = cleaned_data.get('weight')
        if weight is not None and (weight < 0 or weight > 100):
            raise forms.ValidationError('Weight must be between 0 and 100.')
        return cleaned_data


class GradePredictionForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-select'}))
    desired_average = forms.DecimalField(
        max_digits=5, decimal_places=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        label='Desired Final Average'
    )

    def __init__(self, *args, user=None, semester=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and semester:
            from apps.subjects.models import Subject
            self.fields['subject'].queryset = Subject.objects.filter(user=user, semester=semester)
