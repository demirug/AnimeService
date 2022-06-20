from django.urls import path
from apps.movie.views import *

urlpatterns = [
    path("", AnimeListView.as_view(), name="home"),
    path("<slug:slug>/", AnimeDetailView.as_view(), name="detail"),
    path("<slug:slug>/<int:season>/", AnimeDetailView.as_view(), name="detail"),
]
