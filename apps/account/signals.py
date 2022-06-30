from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator as generator

from apps.account.models import User
from shared.services.email import send_template_email


@receiver(post_save, sender=User)
def account_handler(sender, instance: User, **kwargs):
    """Sending welcome email on user register with token to verify account"""
    if kwargs.get("created", False) and not instance.is_active:
        send_template_email(instance.email, _("Welcome to %s") % settings.SITE_NAME, "email/registered.jinja",
                            context={"name": instance.username, "token": generator.make_token(instance)})

