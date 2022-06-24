from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from solo.admin import SingletonModelAdmin

from apps.news.forms import NewsForm
from apps.news.models import News, NewsSettings


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    form = NewsForm


admin.site.register(NewsSettings, SingletonModelAdmin)
