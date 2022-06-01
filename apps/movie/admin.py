from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .forms import AnimeForm
from .models import EpisodeFile, Episode, Quality, Season, Anime, Review, Tag


class EpisodeFileInline(admin.TabularInline):
    model = EpisodeFile
    extra = 1


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    inlines = [
        EpisodeFileInline,
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ['verified', 'datetime']
    readonly_fields = ['datetime', 'user', 'season_link']

    def season_link(self, instance):
        """Displays redirect button to season"""
        return format_html(f'<a target="_blank" href="{instance.season.get_absolute_url()}">View</a>')


@admin.register(Quality)
class SortableBookAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'wight']


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):

    form = AnimeForm

    def save_model(self, request, obj: Anime, form, change):
        """If tags has been changed. Set to m2m rel new tags relation"""
        if obj._tags != obj.tags:
            obj.tag_list.clear()

            tags = set(form.cleaned_data['tags'].split(" "))

            for tag_name in tags:
                if tag_name != "":
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    obj.tag_list.add(tag)
            form.cleaned_data['tag_list'] = obj.tag_list.all()
            obj.tags = " ".join(tags)

        super().save_model(request, obj, form, change)


admin.site.register(Season)
admin.site.register(Tag)
