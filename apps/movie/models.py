from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from shared.services.slugify import unique_slugify

ALLOWED_VIDEO_FORMATS = ['webm', 'mpg', 'ogg', 'mp4', 'mpeg']


class Anime(models.Model):
    """Anime object model"""
    name = models.CharField(_("Name"), max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    poster = models.ImageField(_("Poster"), upload_to="posters/%Y/%m/%d/")

    class Meta:
        verbose_name = _("Anime")
        verbose_name_plural = _("Anime's")
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        """Creating unique slug for model if slug not setted"""
        if not self.slug:
            unique_slugify(self, f"{self.name}")
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})


class Season(models.Model):
    """Season model"""
    name = models.CharField(_("Name"), max_length=150)
    description = models.TextField(_("Description"))
    number = models.PositiveSmallIntegerField()
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="seasons")

    class Meta:
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")
        unique_together = [('number', 'anime')]
        ordering = ['number']

    def __str__(self):
        return self.name


class Quality(models.Model):
    """Quality model"""
    name = models.CharField(_("Name"), max_length=15, blank=True)
    height = models.PositiveSmallIntegerField(_("Height"))
    wight = models.PositiveSmallIntegerField(_("Wight"))

    def save(self, *args, **kwargs):
        """If name not setted generate name"""
        if not self.name:
            self.name = f"{self.wight}x{self.height}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Quality")
        verbose_name_plural = _("Quality")
        unique_together = [('height', 'wight')]


class Episode(models.Model):
    """Episode model"""
    name = models.CharField(_("Name"), max_length=150)
    description = models.TextField(_("Description"))
    number = models.PositiveSmallIntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")

    class Meta:
        verbose_name = _("Episode")
        verbose_name_plural = _("Episodes")
        unique_together = [('number', 'season')]
        ordering = ['number']

    def __str__(self):
        return self.name


def anime_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/movie/files/anime_name/season_name/episode_name/<filename>
    return 'movie/files/{0}/{1}/{2}/{3}/'.format(
                            instance.episode.season.anime.name,
                            instance.episode.season.name,
                            instance.episode.name,
                            filename)


class EpisodeFile(models.Model):
    """Episode File model, unique constraint quality and episode"""
    file = models.FileField(upload_to=anime_path, validators=[FileExtensionValidator(ALLOWED_VIDEO_FORMATS)])
    quality = models.ForeignKey(Quality, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="files")

    class Meta:
        verbose_name = _("Episode File")
        verbose_name_plural = _("Episode Files")
        unique_together = [('quality', 'episode')]

    def __str__(self):
        return f"{self.episode}/{self.quality}"
