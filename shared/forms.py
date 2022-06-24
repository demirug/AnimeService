from django import forms
from django.utils.translation import get_language

from app import settings


class LanguageForm(forms.Form):

    def __init__(self, *args, **kwargs):
        print(get_language())
        kwargs.update(initial={
            'language': get_language()
        })

        super().__init__(*args, **kwargs)

    language = forms.ChoiceField(label="", choices=settings.LANGUAGES, widget=forms.Select(attrs={'onchange': 'this.form.submit()'}))