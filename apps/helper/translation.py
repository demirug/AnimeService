from modeltranslation.translator import register, TranslationOptions
from .models import FAQ, HelperSettings


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')


@register(HelperSettings)
class HelperSettingsTranslationOptions(TranslationOptions):
    fields = ('feedback_email_title', 'feedback_email')
