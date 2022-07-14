from django.core.handlers.wsgi import WSGIRequest
from django.utils.http import url_has_allowed_host_and_scheme


def __allowed_url(url: str, request: WSGIRequest) -> bool:
    """
    Return is given url allowed

    :param url: url path
    :param request: WSGI request
    :return: is url allowed
    """
    return url and url_has_allowed_host_and_scheme(
        url=url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    )


def get_next_url(request: WSGIRequest, default: str = "/") -> str:
    """
    Return next url.

    :param request: WSGI request
    :param default: default redirect url (if next or HTTP_REFERER not given)
    :return: url path
    """
    next_url = request.POST.get('next', request.GET.get('next'))

    if not __allowed_url(next_url, request):
        next_url = request.META.get('HTTP_REFERER')
        if not __allowed_url(next_url, request):
            next_url = default

    return next_url
