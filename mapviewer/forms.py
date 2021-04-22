import re

from django import forms


class SearchForm(forms.Form):
    text = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Search...', 'autocomplete': 'off', 'type': 'search', 'id': 'searchbartext'}), required=False)

    def clean(self, *args):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        text = re.sub("[^a-zA-Z0-9 \"]", "", text)
        text = text.split(" ")
        cleaned_data["text"] = text
