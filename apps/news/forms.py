from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.translation import gettext_lazy as _

from apps.news.models import News


class NewsForm(forms.ModelForm):
    description = forms.CharField(label=_("Description"), max_length=500, widget=CKEditorUploadingWidget())
    content = forms.CharField(label=_("Content"), widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'
