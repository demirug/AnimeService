from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

from django.utils.translation import gettext_lazy as _

from apps.account.managers import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("User with that nickname already exists"),
        },
    )

    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=255,
    )

    avatar = models.ImageField(_('Avatar'), upload_to="account/%Y/%m/%d", blank=True)

    is_active = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
