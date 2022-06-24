from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.textpage.models import TextPage
from shared.mixins.translate import TranslateFormWidgetMixin


class TextPageAdminForm(TranslateFormWidgetMixin, forms.ModelForm):
    """Form for TextPage"""

    def get_widgets(self) -> dict:
        return {"content": CKEditorUploadingWidget()}

    class Meta:
        model = TextPage
        fields = '__all__'
