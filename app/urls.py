from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.account.urls import urlpatterns as auth_urls
from apps.movie.urls import urlpatterns as movie_urls

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += auth_urls
urlpatterns += movie_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
