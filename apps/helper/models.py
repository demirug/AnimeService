from django.db import models
from django.utils.translation import gettext_lazy as _


class FAQ(models.Model):
    """Model for Answer presets"""
    question = models.CharField(_("Question"), max_length=300)
    answer = models.TextField(_("Answer"))

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")

    def __str__(self):
        return self.question


class Feedback(models.Model):
    """Model for Questions"""
    question = models.TextField(_("Question"))
    email = models.EmailField(_("Email"))
    answer = models.TextField(_("Answer"), blank=True, null=True)
    answered = models.BooleanField(_("Answered"), default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")
        ordering = ['answered']

    def __str__(self):
        return f"Question #{self.pk}"

