from django.db import models
from django.utils.translation import get_language


class AnimeManager(models.Manager):

    def get_lang_queryset(self):
        return self.get_queryset().filter(lang=get_language())