from django.urls import path
from apps.movie.views import AnimeListView, AnimeDetailView

urlpatterns = [
    path("", AnimeListView.as_view(), name="home"),
    path("/<slug:name>/", AnimeDetailView.as_view(), name="detail"),
]
