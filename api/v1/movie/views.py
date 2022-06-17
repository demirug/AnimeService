from django.db.models import Count, Q
from django.http import Http404

from api.mixins import ListRetrieveViewSet, RetrieveViewSet
from api.v1.movie.serializers import *
from apps.movie.filters import AnimeFilter
from apps.movie.models import Episode, Anime, Season


# movide/anime/
# movie/anime/<anime_slug>/
# movie/season/<season_pk>/
# movie/episode/<episode_pk>/
# movie/random/<ignore_anime_slug>/

# movie/subscribe/<anime_slug>/
# movie/rating/<anime_slug>/<rating_star_pk>/
# movie/review/<season_pk>/<review>/


class AnimeViewSet(ListRetrieveViewSet):
    """
    ViewSet for all Anime objects
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    lookup_field = "slug"
    filterset_class = AnimeFilter


class AnimeRandomViewSet(ListRetrieveViewSet):
    """
    ViewSet return random Anime /random/<ignore_slug=None>
    If ignore_slug given anime with that slug will be ignored
    """
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    lookup_field = "slug"

    def get_object(self):
        random_object = self.queryset.annotate(seasons_cnt=Count("seasons")) \
            .filter(seasons_cnt__gt=0)
        # If ignore param given
        if 'slug' in self.kwargs:
            random_object = random_object.filter(~Q(slug=self.kwargs['slug']))

        if not random_object:
            raise Http404("Recommendation Anime not found")
        return random_object.order_by("?").first()

    def list(self, request, *args, **kwargs):
        """ If no argument not given return object without fulter"""
        # Yeah i know that is shit but it's working
        return super(AnimeRandomViewSet, self).retrieve(request, *args, **kwargs)


class SeasonRetrieveViewSet(RetrieveViewSet):
    """Retrieve viewset for Season model"""
    queryset = Season.objects.all()
    serializer_class = SeasonEpisodeSerializer


class EpisodeRetrieveViewSet(RetrieveViewSet):
    """Retrieve viewset for Episode model"""
    queryset = Episode.objects.prefetch_related('files__quality').all()
    serializer_class = EpisodeFileSerializer
