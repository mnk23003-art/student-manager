from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Search...',
        'class': 'form-control',
        'autofocus': True,
    }))
