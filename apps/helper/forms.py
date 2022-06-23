from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from apps.helper.models import Question


class AdminQuestionForm(forms.ModelForm):
    """Question for admin panel"""
    question = forms.CharField()

    email = forms.EmailField()

    answer = forms.CharField(label="", widget=CKEditorUploadingWidget(config_name='question'))

    class Meta:
        model = Question
        fields = ['question', 'email', 'answer']


class AuthorizeQuestionForm(forms.ModelForm):
    """Question form for authorized users"""
    question = forms.CharField(label="", widget=CKEditorUploadingWidget(config_name='question'))

    def clean_question(self):
        question = self.cleaned_data['question']

        if len(strip_tags(question)) < 20:
            raise ValidationError(_("Minimum length of question 20 chars"))
        return question

    class Meta:
        model = Question
        fields = ['question']


class UnAuthorizeQuestionForm(forms.ModelForm):
    """Question form for unauthorized users"""
    question = forms.CharField(label="", widget=CKEditorUploadingWidget(config_name='question'))
    email = forms.EmailField(label="",
                             widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Email")}))

    class Meta:
        model = Question
        fields = ['email', 'question']
