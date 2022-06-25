from modeltranslation.translator import register, TranslationOptions
from .models import Element


@register(Element)
class ElementTranslationOptions(TranslationOptions):
    fields = ('name',)
