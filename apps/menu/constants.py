from django.db import models
from django.utils.translation import gettext_lazy as _


class TargetType(models.TextChoices):
    """Выбор типа ссылки меню"""
    BLANK = 'BL', _('_blank')
    SELF = 'SE', _('_self')


class PositionType(models.TextChoices):
    """Выбор расположения элемента меню на сайте"""
    FOOTER = 'FO', _('footer')
    HEADER = 'HE', _('header')
