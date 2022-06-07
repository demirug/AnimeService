import django_filters

from apps.movie.models import Anime, Tag


class AnimeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label='Search', method='name_tag_filter')

    def name_tag_filter(self, queryset, name, value):
        """Filter search by name & tags"""
        data = value.split(' ')

        tags = [tag.lower()[1:] for tag in data if tag.startswith('#')]
        search = ' '.join([text for text in data if not text.startswith('#')])

        if tags:
            tags_objects = Tag.objects.filter(name__in=tags)
            # If given tag not found return empty results
            if tags_objects.count() != len(tags):
                return Anime.objects.none()

            anime_pk = tags_objects.filter(anime__name__icontains=search).values_list('anime__pk', flat=True)
            return queryset.filter(pk__in=anime_pk)

        return queryset.filter(name__icontains=search)

    class Meta:
        model = Anime
        fields = ['search']
