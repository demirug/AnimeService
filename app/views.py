from django.shortcuts import render

from django.utils.translation import gettext_lazy as _


# Error 400
def bad_request_view(request, exception=None):
    return render(request, 'error.jinja', context={'error_code': 400, 'error_message': _('Bad request')})


# Error 403
def permission_denied_view(request, exception=None):
    return render(request, 'error.jinja', context={'error_code': 403, 'error_message': _('Permission denied')})


# Error 404
def not_found_view(request, exception=None):
    return render(request, 'error.jinja', context={'error_code': 404, 'error_message': _('The page cant be found')})


# Error 500
def server_error_view(request):
    return render(request, 'error.jinja', context={'error_code': 500, 'error_message': _('Server error')})