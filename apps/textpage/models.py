from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class TextPage(models.Model):
    """Модель текстовых страниц"""
    name = models.CharField(verbose_name=_("Name"), max_length=150)
    slug = models.SlugField("Slug", unique=True)
    content = models.TextField(verbose_name=_("Content"))
    draft = models.BooleanField(verbose_name=_("Draft"), default=False)

    created_at = models.DateTimeField(_("Creation date"), auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _("Text page")
        verbose_name_plural = _("Text pages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("textpage", kwargs={"slug": self.slug})