from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from solo.admin import SingletonModelAdmin

from .forms import AnimeForm, EpisodeForm, SeasonForm, MovieSettingsForm, EpisodeFileForm
from .models import EpisodeFile, Episode, Quality, Season, Anime, Review, Tag, Style, AnimeImage, \
    MovieSettings


class EpisodeFileInline(admin.TabularInline):
    model = EpisodeFile
    form = EpisodeFileForm
    extra = 1


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    form = EpisodeForm
    autocomplete_fields = ('season',)
    list_display = ['season', 'number']
    search_fields = ['season__anime__name']
    inlines = [
        EpisodeFileInline,
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ['verified', 'datetime']
    readonly_fields = ['datetime', 'user', 'season_link', 'text']
    fields = ['text', 'datetime', 'user', 'season_link', 'verified']

    def has_add_permission(self, request):
        return False

    def season_link(self, instance):
        """Displays redirect button to season"""
        return format_html(f'<a target="_blank" href="{instance.season.get_absolute_url()}">View</a>')


@admin.register(Quality)
class SortableBookAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'wight']


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    form = AnimeForm
    search_fields = ('name',)
    autocomplete_fields = ('style',)
    readonly_fields = ('rating',)
    list_display = ['name', 'type', 'lang']
    list_filter = ('type', 'lang')

    def save_model(self, request, obj: Anime, form, change):
        """If tags has been changed. Set to m2m rel new tags relation"""

        if not obj.pk:
            obj.save()

        if obj._tags != obj.tags:
            obj.tag_list.clear()

            tags = set(form.cleaned_data['tags'].lower().split(" "))

            for tag_name in tags:
                if tag_name != "":
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    obj.tag_list.add(tag)
            form.cleaned_data['tag_list'] = obj.tag_list.all()
            obj.tags = " ".join(tags)

        super().save_model(request, obj, form, change)


class AnimeImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = AnimeImage
    extra = 1


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    form = SeasonForm
    inlines = [AnimeImageInline]
    search_fields = ('anime__name',)
    autocomplete_fields = ('anime',)


@admin.register(MovieSettings)
class MovieSettingAdmin(TranslationAdmin, SingletonModelAdmin):
    form = MovieSettingsForm


admin.site.register(Tag)
