import re

from django import forms


class SearchForm(forms.Form):
    text = forms.CharField(label="", help_text="", widget=forms.TextInput(attrs={'placeholder': 'Search...', 'autocomplete': 'off', 'type': 'search', 'id': 'searchbartext'}), required=False)
    page = forms.CharField(label="", help_text="", widget=forms.HiddenInput(attrs={'id': 'page_id', 'value': '1'}))

    def clean(self, *args):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        text = re.sub("[^a-zA-Z0-9 \"]", "", text)
        text = text.lower()
        text = text.split(" ")
        cleaned_data["text"] = text
        page = cleaned_data.get("page")
        if isinstance(page, str) and page.isdigit():
            cleaned_data["page"] = int(page)
        else:
            cleaned_data["page"] = 1

