from modeltranslation.translator import register, TranslationOptions
from .models import AccountSettings


@register(AccountSettings)
class AccountSettingsTranslationOptions(TranslationOptions):
    fields = ('change_email_title', 'change_email', 'registered_email_title', 'registered_email', 'reset_email_title', 'reset_email')
