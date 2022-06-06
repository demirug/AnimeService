from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.textpage.models import TextPage


class TextPageAdminForm(forms.ModelForm):
    """Form for TextPage"""
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = TextPage
        fields = '__all__'
