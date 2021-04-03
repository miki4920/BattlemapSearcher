from django import forms
from .models import Tag


class SearchForm(forms.Form):
    choices = list(Tag.objects.all())
    choices = [(choice.name, choice.name.capitalize()) for choice in choices]
    choices = sorted(choices)
    tag = forms.CharField(widget=forms.Select(choices=choices))