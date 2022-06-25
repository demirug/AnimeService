import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from apps.movie.constants import AnimeType
from apps.movie.managers import AnimeManager
from shared.services.slugify import unique_slugify

ALLOWED_VIDEO_FORMATS = ['webm', 'mpg', 'ogg', 'mp4', 'mpeg']


class Tag(models.Model):
    """Tag model"""
    name = models.CharField(_("Name"), max_length=150, unique=True)
    display = models.BooleanField(_("Display"), default=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return f"#{self.name}"

    def get_absolute_url(self):
        return f"{reverse('movie:home')}?search=%23{self.name}"


class Style(models.Model):
    """Style model for Anime model customization"""
    name = models.CharField(_("Name"), unique=True, max_length=150)
    style = models.TextField(_("Style"), blank=True)
    background = models.ImageField(_("Background"), blank=True, null=True, upload_to="style/")

    def __str__(self):
        return self.name


class Anime(models.Model):
    """Anime object model"""
    name = models.CharField(_("Name"), max_length=150)
    lang = models.CharField(_("Language"), max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    type = models.CharField(_("Content type"), max_length=2, choices=AnimeType.choices, default=AnimeType.SERIAL)
    slug = models.SlugField(blank=True)
    poster = models.ImageField(_("Poster"), upload_to="posters/%Y/%m/%d/")
    style = models.ForeignKey(Style, null=True, blank=True, related_name="anime", on_delete=models.SET_NULL)
    tags = models.TextField(_("Tags"), blank=True)
    tag_list = models.ManyToManyField(Tag, blank=True, related_name="anime")
    rating = models.PositiveIntegerField(_("Rating"), default=0)

    objects = AnimeManager()

    class Meta:
        verbose_name = _("Anime")
        verbose_name_plural = _("Anime's")
        unique_together = [('slug', 'lang')]
        ordering = ['name']

    def __init__(self, *args, **kwargs):
        super(Anime, self).__init__(*args, **kwargs)
        self._tags = self.tags

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        """Creating unique slug for model if slug not set"""
        if not self.slug:
            unique_slugify(self, f"{self.name}")
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse("movie:detail", kwargs={"slug": self.slug})


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
        return _("%s | Season #%s") % (self.anime.name, self.number)

    def get_absolute_url(self):
        return reverse("movie:detail", kwargs={"slug": self.anime.slug, "season": self.number})


class Quality(models.Model):
    """Quality model"""
    name = models.CharField(_("Name"), max_length=15, unique=True)
    wight = models.SmallIntegerField(default=0)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Quality")
        verbose_name_plural = _("Quality")
        ordering = ['wight']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.default:
            Quality.objects.filter(default=True).update(default=False)
        super().save(*args, **kwargs)


class Episode(models.Model):
    """Episode model"""
    number = models.PositiveSmallIntegerField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")

    class Meta:
        verbose_name = _("Episode")
        verbose_name_plural = _("Episodes")
        unique_together = [('number', 'season')]
        ordering = ['number']

    def __str__(self):
        return _("Episode %s") % self.number

    def get_absolute_url(self):
        return f"{self.season.get_absolute_url()}?e={self.number}"


def anime_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/movie/files/anime_name/season_name/<filename>
    return 'movie/files/{0}/{1}/{2}/'.format(
        instance.episode.season.anime.name,
        instance.episode.season.name,
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

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension[1:]

    def __str__(self):
        return f"{self.episode}/{self.quality}"


class Review(models.Model):
    """Review model"""
    season: Season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(_("Review"))

    datetime = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return _("Review #%s") % self.pk


class Subscribe(models.Model):
    """User subscribe to anime model"""
    anime: Anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="subscribes")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="subscribes")

    class Meta:
        unique_together = [('anime', 'user')]


def anime_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/movie/season_images/anime_name/season_name/<filename>
    return 'movie/season_images/{0}/{1}/{2}/'.format(
        instance.season.anime.name,
        instance.season.name,
        filename)


class AnimeImage(models.Model):
    season: Season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField(upload_to=anime_image_path)
    wight = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = _("Anime Image")
        verbose_name_plural = _("Anime Images")
        ordering = ['wight']

    def __str__(self):
        return _("AnimeImage #%s") % self.pk


class Rating(models.Model):
    """Anime rating model"""
    val = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="ratings")
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="ratings")

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        unique_together = [('user', 'anime')]


class MovieSettings(SingletonModel):
    """Model of Movie settings"""
    movie_per_page = models.PositiveSmallIntegerField(_("Movie per page"),
                                                      help_text=_("How many movies will be shown per page"),
                                                      validators=[MinValueValidator(1)],
                                                      default=10)

    paginator_pages_show = models.PositiveSmallIntegerField(_("Paginator pages show"),
                                                            help_text=_("How many additional pages will be shown in paginator"),
                                                            validators=[MinValueValidator(1)],
                                                            default=3)

    max_reviews_per_season = models.PositiveSmallIntegerField(_("Reviews per season"),
                                                              help_text=_("How many reviews can a user send on an season"),
                                                              validators=[MinValueValidator(1)],
                                                              default=2)

    min_review_length = models.PositiveSmallIntegerField(_("Min Review length"),
                                                      help_text=_("Minimum length of review text"),
                                                      validators=[MinValueValidator(1)],
                                                      default=20)

    max_review_length = models.PositiveSmallIntegerField(_("Maximum Review length"),
                                                      help_text=_("Maximum length of review text"),
                                                      validators=[MinValueValidator(1)],
                                                      default=500)

    min_rating_val = models.PositiveSmallIntegerField(_("Minimum rating value"),
                                                      validators=[MinValueValidator(1)],
                                                      default=1)

    max_rating_val = models.PositiveSmallIntegerField(_("Maximum rating value"),
                                                      validators=[MinValueValidator(1)],
                                                      default=5)

    class Meta:
        verbose_name = _("Movie Configuration")

    def __str__(self):
        return "Movie Configuration"
