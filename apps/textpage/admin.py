from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.textpage.forms import TextPageAdminForm
from apps.textpage.models import TextPage


@admin.register(TextPage)
class TextPageAdmin(ModelAdmin):
    form = TextPageAdminForm
    search_fields = ('name',)
    list_display = ['name', 'draft', 'created_at']
