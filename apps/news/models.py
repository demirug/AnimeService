from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from shared.services.slugify import unique_slugify


class News(models.Model):
    """News model"""
    name = models.CharField(_("Name"), max_length=150)
    slug = models.SlugField("Slug", blank=True, unique=True)
    description = models.CharField(_("Short description"), max_length=500)
    content = models.TextField(_("Content"))
    date = models.DateTimeField(_("Date"), auto_now_add=True)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ['-date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("news", kwargs={"slug": self.slug})

    def save(self, **kwargs):
        """Creating unique slug for model if slug not set"""
        if not self.slug:
            unique_slugify(self, self.name)
        super().save(**kwargs)


class NewsSettings(SingletonModel):
    """Model of News settings"""
    news_per_page = models.PositiveSmallIntegerField(_("News per page"),
                                                     help_text=_("How many news will be shown per page"),
                                                     validators=[MinValueValidator(1)],
                                                     default=10)
    paginator_pages_show = models.PositiveSmallIntegerField(_("Paginator pages show"),
                                                            help_text=_("How many additional pages will be shown in paginator"),
                                                            validators=[MinValueValidator(1)],
                                                            default=3)

    class Meta:
        verbose_name = _("News Configuration")

    def __str__(self):
        return "News Configuration"
