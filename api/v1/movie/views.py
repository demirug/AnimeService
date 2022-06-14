from rest_framework.generics import RetrieveAPIView, get_object_or_404
from django.db.models import Count, Q
from api.v1.movie.serializers import EpisodeSerializer, AnimeSerializer, AnimeRandomSerializer
from apps.movie.models import Episode, Anime


class AnimeRetrieveApiView(RetrieveAPIView):
    """RetrieveAPIView for Anime model"""
    serializer_class = AnimeSerializer
    queryset = Anime.objects.all()
    lookup_field = 'slug'


class EpisodeRetrieveAPIView(RetrieveAPIView):
    """RetrieveAPIView for Episode model"""
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.prefetch_related('files__quality').all()

    def get_object(self):
        """Getting Episode object from params"""
        obj = get_object_or_404(self.queryset, number=self.kwargs['episode'],
                                season__number=self.kwargs['season'],
                                season__anime__slug=self.kwargs['slug'])
        return obj


class AnimeRandomApiView(RetrieveAPIView):
    """Return a random anime by accepting ignore pk param"""
    serializer_class = AnimeRandomSerializer
    queryset = Anime.objects.all()

    def get_object(self):
        if 'slug' in self.kwargs:
            random_object = self.queryset.annotate(seasons_cnt=Count("seasons")) \
                .filter(~Q(slug=self.kwargs['slug']) & Q(seasons_cnt__gt=0)).order_by("?")
        else:
            random_object = self.queryset.annotate(seasons_cnt=Count("seasons")) \
                .filter(seasons_cnt__gt=0).order_by("?")[0]
        return random_object
