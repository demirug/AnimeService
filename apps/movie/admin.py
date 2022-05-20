from django.contrib import admin

from apps.movie.models import EpisodeFile, Episode, Quality, Season, Anime


class EpisodeFileInline(admin.TabularInline):
    model = EpisodeFile
    extra = 1


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    inlines = [
        EpisodeFileInline,
    ]


admin.site.register(Quality)
admin.site.register(Season)
admin.site.register(Anime)
