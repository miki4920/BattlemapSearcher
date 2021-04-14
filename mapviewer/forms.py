import re

from django import forms
from django.core.exceptions import ValidationError


class SearchForm(forms.Form):
    text = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Search...', 'autocomplete': 'off'}))

    def clean(self, *args):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")

