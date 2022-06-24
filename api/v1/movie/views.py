from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.mixins import ListRetrieveViewSet, RetrieveViewSet
from api.v1.movie.serializers import *
from apps.movie.filters import AnimeFilter
from apps.movie.models import Episode, Anime, Season, Subscribe


# movide/anime/
# movie/anime/<anime_slug>/
# movie/season/<season_pk>/
# movie/episode/<episode_pk>/
# movie/random/<ignore_anime_slug>/

# movie/subscribe/
# movie/subscribe/<anime_pk>/

# movie/rating/<anime_pk>/
# movie/rating/

# movie/review/


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
            raise Http404(_("Recommended Anime not found"))
        return random_object.order_by("?").first()

    def list(self, request, *args, **kwargs):
        """ If no argument not given return object without filter"""
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


class ReviewCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    """CreateViewSet for Review model"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscribeCreateDeleteViewSet(GenericViewSet):
    """Create/Delete viewset for Subscribe"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscribeSerializer

    def retrieve(self, request, *args, **kwargs):
        """Returns if the player is subscribed to the anime"""
        instance = get_object_or_404(Subscribe, user=self.request.user, anime_id=self.kwargs['pk'])
        return Response({'subscribe': instance is not None})

    def create(self, request, *args, **kwargs):
        """Changed subscribe status and returned it"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)

        obj, created = Subscribe.objects.get_or_create(
            anime=serializer.validated_data['anime'],
            user=request.user,
            defaults={'anime': serializer.validated_data['anime'], 'user': request.user}
        )

        if not created:
            obj.delete()
        return Response({'subscribe': created}, status=status.HTTP_200_OK)


class RatingCreateUpdateViewSet(GenericViewSet):
    """Create/Update viewset for Rating"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RatingSerializer

    def retrieve(self, request, *args, **kwargs):
        """Returns if the player is subscribed to the anime"""
        instance = get_object_or_404(Rating, user=self.request.user, anime_id=self.kwargs['pk'])
        return Response({'rating': instance.val})

    def create(self, request, *args, **kwargs):
        """Updated subscribe status and returned it"""
        serializer: RatingSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj, created = Rating.objects.update_or_create(
            anime=serializer.validated_data['anime'],
            user=request.user,
            defaults={'val': serializer.validated_data['val']}
        )

        return Response({"status": "Okay"}, status=status.HTTP_200_OK)
