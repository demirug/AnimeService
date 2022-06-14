from django.urls import path, include

from api.v1.account.views import CurrentUserView
from api.v1.movie.views import EpisodeRetrieveAPIView, AnimeRetrieveApiView, AnimeRandomApiView

urlpatterns = [
    path('v1/', include([
        path('episode/<slug:slug>/<int:season>/<int:episode>/', EpisodeRetrieveAPIView.as_view(), name='episode'),
        path("anime/", include([
            path("random/", AnimeRandomApiView.as_view(), name='random'),
            path("random/<int:pk>/", AnimeRandomApiView.as_view(), name='random'),
            path("view/<slug:slug>/", AnimeRetrieveApiView.as_view(), name='anime'),
        ])),
        path('user/', CurrentUserView.as_view(), name="user"),
    ])),
    path('api-auth/', include('rest_framework.urls')),
]
