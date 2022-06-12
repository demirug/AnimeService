from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator as generator
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext_lazy as _

from django.views.generic import TemplateView, RedirectView, ListView, FormView
from django_jinja.views.generic import CreateView, UpdateView

from shared.mixins.breadcrumbs import BreadCrumbsMixin
from .forms import UserCreationForm, AccountUpdateForm, UserPasswordChangeForm
from ..movie.models import Subscribe


class AccountChangePasswordView(LoginRequiredMixin, BreadCrumbsMixin, FormView):
    form_class = UserPasswordChangeForm
    template_name = "account/change_password.jinja"

    def get_breadcrumbs(self):
        return [("Anime", reverse("home")), ("Profile", reverse("profile")), ("Change password",)]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, _("Password has been changed"))
        return redirect(reverse("profile"))


class AccountProfileView(LoginRequiredMixin, UpdateView):
    """Change user profile view"""
    model = get_user_model()
    template_name = "account/profile.jinja"
    success_url = reverse_lazy('profile')
    form_class = AccountUpdateForm

    def get_breadcrumbs(self):
        return [("Anime", reverse("home")), ("Profile",)]

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class AccountSubscribersView(LoginRequiredMixin, BreadCrumbsMixin, ListView):
    """Display all user subscribers"""
    model = Subscribe
    template_name = "account/subscribers.jinja"

    def get_queryset(self):
        return self.request.user.subscribes.select_related("anime").all()

    def get_breadcrumbs(self):
        return [("Anime", reverse("home")), ("Profile", reverse("profile")), ("Subscribes",)]

    def post(self, request: WSGIRequest, *args, **kwargs):
        if "slug" in request.POST:
            get_object_or_404(Subscribe, user=self.request.user, anime__slug=request.POST["slug"]).delete()
        return redirect(reverse("subscribes"))


class AccountRegisterView(CreateView):
    """Register user account view"""
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "account/register.jinja"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        return render(self.request, "account/registered.jinja", context={"user": user})


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


class AccountEmailChangeView(LoginRequiredMixin, RedirectView):
    """Change user email View"""
    url = reverse_lazy("profile")

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        _email = kwargs['email']
        _hash = kwargs['hash']

        # Check if given hash valid

        check_hash = salted_hmac(
            self.request.user.pk,
            f"{self.request.user.email}{_email}",
            secret=settings.SECRET_KEY,
            algorithm='sha1'
        ).hexdigest()[::2]

        if _hash != check_hash:
            raise Http404("Incorrect hash=")

        messages.success(self.request, _('Email has been changed success'))
        user.email = _email
        user.save()

        return super().dispatch(request, *args, **kwargs)
