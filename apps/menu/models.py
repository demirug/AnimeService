from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import TargetType, PositionType


class Element(models.Model):
    """Model for menu items"""

    name = models.CharField(_("Name"), max_length=150)

    url = models.CharField(_("URL"),
                           max_length=200,
                           help_text=_('Example: https://google.com/ or /testPage/'),
                           validators=[URLValidator]
                           )
    target = models.CharField(_("Url type"), max_length=2, choices=TargetType.choices, default=TargetType.SELF)
    position = models.CharField(_("Position"), max_length=2, choices=PositionType.choices)
    enabled = models.BooleanField(_("Enabled"), default=True)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['weight']
        verbose_name = _("Element")
        verbose_name_plural = _("Elements")
