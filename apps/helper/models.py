from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class DefaultAnswer(models.Model):
    """Model for Answer presets"""
    slug = models.SlugField(_("Slug"))
    question = models.CharField(_("Question"), max_length=300)
    answer = models.TextField(_("Answer"))

    class Meta:
        verbose_name = _("Default answer")
        verbose_name_plural = _("Default answers")

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse("helper:detail", kwargs={"slug": self.slug})


class Question(models.Model):
    """Model for Questions"""
    question = models.TextField(_("Question"))
    email = models.EmailField(_("Email"))
    answer = models.TextField(_("Answer"), blank=True, null=True)
    answered = models.BooleanField(_("Answered"), default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['answered']

    def __str__(self):
        return f"Question #{self.pk}"

