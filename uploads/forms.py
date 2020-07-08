from django import forms

from .models import Photo,File


class PhotoForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', )
