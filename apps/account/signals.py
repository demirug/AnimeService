from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator as generator
from django.urls import reverse

from apps.account.models import User, AccountSettings
from shared.services.email import send_email
from shared.services.translation import get_field_data_by_lang


@receiver(post_save, sender=User)
def account_handler(sender, instance: User, **kwargs):
    """Sending welcome email on user register with token to verify account"""
    if kwargs.get("created", False) and not instance.is_active:
        settings: AccountSettings = AccountSettings.get_solo()
        token = generator.make_token(instance)
        title = get_field_data_by_lang(settings, instance.lang, "registered_email_title")
        context = get_field_data_by_lang(settings, instance.lang, "registered_email")\
            .format(name=instance.username,
                    url="{domain}{path}".format(domain=Site.objects.get_current().domain,
                                                path=reverse("account:verify", kwargs={"username": instance.username, "token": token})
                                                )
                    )
        send_email(instance.email, title, context)


