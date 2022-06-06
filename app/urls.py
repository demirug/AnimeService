from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.account.urls import urlpatterns as auth_urls
from apps.movie.urls import urlpatterns as movie_urls

urlpatterns = [
    path('api/', include(('api.urls', 'api'))),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += auth_urls
urlpatterns += movie_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
