from modeltranslation.translator import register, TranslationOptions
from .models import MovieSettings


@register(MovieSettings)
class MovieSettingsTranslationOptions(TranslationOptions):
    fields = ('new_episode_email_title', 'new_episode_email',)
