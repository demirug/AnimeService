from rest_framework.generics import RetrieveAPIView, get_object_or_404

from api.v1.movie.serializers import EpisodeSerializer, AnimeSerializer
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
