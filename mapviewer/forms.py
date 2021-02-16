from django import forms
from .models import *


class MapUploadForm(forms.ModelForm):
    class Meta:
        model = Map
        fields = ['name', 'extension', 'picture', 'uploader']