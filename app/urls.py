from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from apps.helper.views import FeedbackFAQView
from apps.news.views import *
from apps.textpage.views import TextPageDetailView

urlpatterns = [
    path('api/', include(('api.urls', 'api'))),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(r'^rosetta/', include('rosetta.urls'))
]

    path("", NewsListView.as_view(), name="home"),
    path("news/<slug:slug>/", NewsDetailView.as_view(), name="news"),

    path("helper/", FeedbackFAQView.as_view(), name="helper"),
    path("anime/", include(("apps.movie.urls", "movie"))),
    path("", include(("apps.account.urls", "account"))),
    path("page/<slug:slug>/", TextPageDetailView.as_view(), name="textpage"),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
