from django.core.handlers.wsgi import WSGIRequest
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import get_language


class LanguageUpdateMiddleware(MiddlewareMixin):
    """Set changed language to user model"""

    def process_request(self, request: WSGIRequest):
        if request.user.is_authenticated:
            lang_code = get_language()
            if request.user.lang != lang_code:
                request.user.lang = lang_code
                request.user.save()
