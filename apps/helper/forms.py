from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from apps.helper.models import Feedback, FAQ, HelperSettings
from shared.mixins.translate import TranslateFormWidgetMixin


class HelperSettingsForm(TranslateFormWidgetMixin, forms.ModelForm):

    def get_widgets(self) -> dict:
        return {"feedback_email": CKEditorUploadingWidget()}

    class Meta:
        model = HelperSettings
        fields = "__all__"


class FAQForm(TranslateFormWidgetMixin, forms.ModelForm):

    def get_widgets(self) -> dict:
        return {"answer": CKEditorUploadingWidget()}

    class Meta:
        model = FAQ
        fields = "__all__"


class FeedbackAdminForm(forms.ModelForm):
    """Feedback for admin panel"""
    question = forms.CharField()

    email = forms.EmailField()

    answer = forms.CharField(label=_("Answer"), widget=CKEditorUploadingWidget(config_name='no-elements'))

    class Meta:
        model = Feedback
        fields = ['question', 'email', 'answer']


class AuthorizeFeedbackForm(forms.ModelForm):
    """Feedback form for authorized users"""
    question = forms.CharField(label="", widget=CKEditorUploadingWidget(config_name='no-elements'))

    def clean_question(self):
        question = self.cleaned_data['question']

        if len(strip_tags(question)) < 20:
            raise ValidationError(_("Minimum length of question 20 chars"))
        return question

    class Meta:
        model = Feedback
        fields = ['question']


class UnAuthorizeFeedbackForm(forms.ModelForm):
    """Feedback form for unauthorized users"""
    question = forms.CharField(label="", widget=CKEditorUploadingWidget(config_name='no-elements'))
    email = forms.EmailField(label="",
                             widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Email")}))

    class Meta:
        model = Feedback
        fields = ['email', 'question']
