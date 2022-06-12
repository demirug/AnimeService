from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html

from apps.textpage.forms import TextPageAdminForm
from apps.textpage.models import TextPage


@admin.register(TextPage)
class TextPageAdmin(ModelAdmin):
    form = TextPageAdminForm
    search_fields = ('name',)
    list_display = ['name', 'draft', 'created_at']
    readonly_fields = ['page_link']

    def page_link(self, instance):
        """Displays redirect page button if not draft"""
        if instance.pk is None or instance.draft:
            return "-"
        return format_html(f'<a target="_blank" class="btn btn-primary" href="{instance.get_absolute_url()}">View</a>')