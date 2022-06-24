from modeltranslation.translator import register, TranslationOptions
from .models import TextPage


@register(TextPage)
class TextPageTranslationOptions(TranslationOptions):
    fields = ('name', 'content')
