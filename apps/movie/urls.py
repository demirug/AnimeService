from django.urls import path
from apps.movie.views import *

urlpatterns = [
    path("", AnimeListView.as_view(), name="home"),

    path("view/<slug:slug>/", AnimeDetailView.as_view(), name="detail"),
    path("view/<slug:slug>/<int:season>/", AnimeDetailView.as_view(), name="detail"),
    path("review/<slug:slug>/<int:season>/", ReviewCreateUpdateView.as_view(), name="review"),
    path("subscribe/<slug:slug>/", SubscribeView.as_view(), name="subscribe"),
]
