from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.translation import gettext_lazy as _

from apps.movie.models import Review, Anime, Episode


class ReviewForm(forms.ModelForm):

    text = forms.CharField(label="", widget=CKEditorUploadingWidget(config_name='no-elements'))

    class Meta:
        model = Review
        fields = ['text']


class AnimeForm(forms.ModelForm):

    class Meta:
        model = Anime
        exclude = ['tag_list']


class EpisodeForm(forms.ModelForm):

    class Meta:
        model = Episode
        fields = "__all__"
        labels = {
            "season": _("Anime")
        }