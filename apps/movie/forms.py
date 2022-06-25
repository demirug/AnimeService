from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from apps.movie.constants import AnimeType
from apps.movie.models import Review, Anime, Episode, Season


class ReviewForm(forms.ModelForm):
    text = forms.CharField(label="", widget=CKEditorUploadingWidget(config_name='no-elements'))

    class Meta:
        model = Review
        fields = ['text']


class AnimeForm(forms.ModelForm):
    """Form for Anime model"""
    def clean_type(self):
        """Block changing type of Anime to Film if it contains more than 1 season and more than 1 episode"""
        type = self.cleaned_data['type']
        if self.instance and "type" in self.changed_data:
            if type == AnimeType.FILM:
                seasons: QuerySet = self.instance.seasons.all()
                if seasons.count() > 1:
                    raise ValidationError(
                        _("To change type to film, please remove all anime seasons and episodes except one"))
                season: Season = seasons.first()
                if seasons and season.episodes.count() > 1:
                    raise ValidationError(
                        _("To change type to film, please remove all anime seasons and episodes except one"))
        return type

    class Meta:
        model = Anime
        exclude = ['tag_list']


class SeasonForm(forms.ModelForm):
    """Form for Season model"""
    def clean(self):
        """Block creating seasons if 1 season exists in FILM Anime"""
        if self.instance.pk is None:
            if self.cleaned_data['anime'].seasons.count() >= 1:
                raise ValidationError(_("Can't add more season to Anime with 'FILM' type"))

        return super(SeasonForm, self).clean()

    class Meta:
        model = Season
        fields = '__all__'


class EpisodeForm(forms.ModelForm):
    """Form for Episode model"""
    def clean(self):

        if self.instance.pk is None:
            if self.cleaned_data['season'].episodes.count() >= 1:
                raise ValidationError(_("Can't add more episodes to Anime with 'FILM' type"))

        return super().clean()

    class Meta:
        model = Episode
        fields = "__all__"
        labels = {"season": _("Anime")}
