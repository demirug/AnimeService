from django.db import models
from django.utils.translation import gettext_lazy as _


class AnimeType(models.TextChoices):
    """Select type of anime"""
    FILM = 'FI', _('Film')
    SERIAL = 'SE', _('Serial')
