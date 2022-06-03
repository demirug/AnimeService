from django import forms

from apps.movie.models import Review, Anime, Episode, Season


class ReviewForm(forms.ModelForm):

    text = forms.CharField(label="Text", widget=forms.Textarea(attrs={"class": "form-control"}))

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