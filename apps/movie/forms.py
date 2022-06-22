from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.movie.models import Review, Anime, Episode


class ReviewForm(forms.ModelForm):

    text = forms.CharField(label="", widget=CKEditorUploadingWidget(config_name='review'))

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
            "season": "Anime"
        }