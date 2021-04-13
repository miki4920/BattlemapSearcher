from django import forms


class SearchForm(forms.Form):
    text = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Search...', 'autocomplete': 'off'}))