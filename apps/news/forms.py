from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.news.models import News
from shared.mixins.translate import TranslateFormWidgetMixin


class NewsForm(TranslateFormWidgetMixin, forms.ModelForm):

    def get_widgets(self) -> dict:
        return {"description": CKEditorUploadingWidget(), "content": CKEditorUploadingWidget()}

    class Meta:
        model = News
        fields = '__all__'
