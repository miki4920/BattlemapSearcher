from django import forms
from .models import *


class HotelForm(forms.ModelForm):
    class Meta:
        model = Map
        fields = ['name', 'extension', 'picture', 'uploader', 'width', 'height', 'square_width', 'square_height', 'tags']