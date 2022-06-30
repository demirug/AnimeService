from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.templatetags.static import static

from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

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
        unique=True,
        verbose_name=_('Email'),
        max_length=255,
    )

    avatar = models.ImageField(_('Avatar'), upload_to="account/%Y/%m/%d", blank=True)
    lang = models.CharField(_("Language"), max_length=10, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
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

    def get_avatar(self):
        """If user avatar not exists return default avatar"""
        if self.avatar:
            return self.avatar.url
        return static("account/images/default_avatar.png")


class AccountSettings(SingletonModel):
    """Account settings"""
    min_password_len = models.PositiveIntegerField(help_text=_("Minimum password length of user account"), default=8)
    max_password_len = models.PositiveIntegerField(help_text=_("Maximum password length of user account"), default=64)

    def __str__(self):
        return "User Configuration"

    class Meta:
        verbose_name = "User Configuration"
