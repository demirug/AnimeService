from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


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
    lang = models.CharField(_("Language"), max_length=10, default=settings.LANGUAGE_CODE)
    answer = models.TextField(_("Answer"), blank=True)
    answered = models.BooleanField(_("Answered"), default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")
        ordering = ['answered']

    def __str__(self):
        return _("Feedback #%s") % self.pk


class HelperSettings(SingletonModel):

    """Account settings"""
    min_feedback_len = models.PositiveIntegerField(help_text=_("Minimum length of feedback text"), default=20)
    max_feedback_len = models.PositiveIntegerField(help_text=_("Maximum length of feedback text"), default=500)
    feedback_email_title = models.CharField(_("Title of email"), max_length=50,
                                               default="Answer on question")
    feedback_email = models.TextField(_("Feedback email"), default="<h4>Given answer to your question</h4><br><p>Your "
                                                                   "question:</p><span>"
                                                                   "{question}</span><br><p>Answer:</p><span>"
                                                                   "{answer}</span><p>With love AnimeService "
                                                                   "team</p>")

    def __str__(self):
        return "Helper Configuration"

    class Meta:
        verbose_name = "Helper Configuration"
