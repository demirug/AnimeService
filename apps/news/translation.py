from modeltranslation.translator import register, TranslationOptions
from .models import News


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'content')
