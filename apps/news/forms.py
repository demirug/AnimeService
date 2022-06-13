from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.news.models import News


class NewsForm(forms.ModelForm):
    description = forms.CharField(label="short_description", max_length=500, widget=CKEditorUploadingWidget())
    content = forms.CharField(label="content", widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'
