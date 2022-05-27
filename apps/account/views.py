from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as generator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from django.views.generic import TemplateView


class ValidateEmailView(TemplateView):
    """View check if username and token correct to validate user email"""

    template_name = "account/verified.jinja"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect("/")

        user = get_object_or_404(get_user_model(), username=kwargs.get("username"))
        token = kwargs.get("token")

        if user.is_active:
            return redirect("/")

        if generator.check_token(user, token):
            user.is_active = True
            user.save()

            return super().dispatch(request, *args, **kwargs)
        raise Http404("Incorrect user token")
