from django.urls import path, include

from api.v1.account.views import CurrentUserView
from api.v1.movie.views import EpisodeRetrieveAPIView, AnimeRetrieveApiView

urlpatterns = [
    path('v1/', include([
        path('episode/<slug:slug>/<int:season>/<int:episode>/', EpisodeRetrieveAPIView.as_view(), name='episode'),
        path('anime/<slug:slug>/', AnimeRetrieveApiView.as_view(), name='anime'),
        path('user/', CurrentUserView.as_view(), name="user"),
    ])),
    path('api-auth/', include('rest_framework.urls')),
]
