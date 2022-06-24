from django.db import models


class TargetType(models.TextChoices):
    """Select type of element"""
    BLANK = 'BL', '_blank'
    SELF = 'SE', '_self'


class PositionType(models.TextChoices):
    """Select position of element"""
    FOOTER = 'FO', 'footer'
    HEADER = 'HE', 'header'
