from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.account.views import CurrentUserView
from api.v1.movie.views import *

router = DefaultRouter()
router.register('anime', AnimeViewSet, basename='anime')
router.register('season', SeasonRetrieveViewSet, basename='season')
router.register('episode', EpisodeRetrieveViewSet, basename='episode')

router.register('random', AnimeRandomViewSet, basename='random')
router.register('review', ReviewCreateViewSet, basename='review')
router.register('subscribe', SubscribeCreateDeleteViewSet, basename='subscribe')
router.register('rating', RatingCreateUpdateViewSet, basename='rating')

urlpatterns = [
    path("movie/", include(router.urls)),
    path('user/', CurrentUserView.as_view(), name="user"),
]
