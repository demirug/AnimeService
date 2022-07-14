from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator as generator
from django.contrib.sites.models import Site
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext_lazy as _, get_language
from django.views import View

from django.views.generic import TemplateView, RedirectView, ListView, FormView
from django.views.i18n import set_language
from django_jinja.views.generic import CreateView, UpdateView

from shared.mixins.breadcrumbs import BreadCrumbsMixin
from shared.services.email import send_email
from shared.services.next_url import get_next_url
from shared.services.translation import get_field_data_by_lang
from .forms import UserCreationForm, AccountUpdateForm, UserPasswordChangeForm, AccountResetForm, \
    AccountResetConfirmForm, AccountLoginForm
from .models import AccountSettings
from ..movie.models import Subscribe


def set_user_language(request):
    """Set changed language to user model"""
    response = set_language(request)
    if settings.LANGUAGE_COOKIE_NAME in response.cookies:
        lang_code = response.cookies[settings.LANGUAGE_COOKIE_NAME].coded_value
        if request.user.is_authenticated and request.user.lang != lang_code:
            request.user.lang = lang_code
            request.user.save()
    return response


class AccountLogoutView(View):
    """View for logout user"""
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(get_next_url(request))


class AccountLoginView(FormView):
    """View for login user"""
    form_class = AccountLoginForm
    template_name = "account/login.jinja"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(get_next_url(self.request, settings.LOGIN_REDIRECT_URL))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        # If remember me button pressed -> expiry session
        if not form.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(0)

        # Load language from user
        response = HttpResponseRedirect(redirect_to=self.request.GET.get('next') or settings.LOGIN_REDIRECT_URL)

        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME, form.get_user().lang,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )

        return response


class AccountChangePasswordView(LoginRequiredMixin, BreadCrumbsMixin, FormView):
    """View for changing user password"""
    form_class = UserPasswordChangeForm
    template_name = "account/change_password.jinja"

    def get_breadcrumbs(self):
        return [(_("Home"), reverse("home")), (_("Profile"), reverse("account:profile")), (_("Change password"),)]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, _("Password has been changed"))
        return redirect("account:profile")


class AccountProfileView(LoginRequiredMixin, BreadCrumbsMixin, UpdateView):
    """Change user profile view"""
    model = get_user_model()
    template_name = "account/profile.jinja"
    success_url = reverse_lazy('account:profile')
    form_class = AccountUpdateForm

    def get_breadcrumbs(self):
        return [(_("Home"), reverse("home")), (_("Profile"),)]

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
        return [(_("Home"), reverse("home")), (_("Profile"), reverse("account:profile")), (_("Subscribes"),)]

    def post(self, request: WSGIRequest, *args, **kwargs):
        if "slug" in request.POST:
            get_object_or_404(Subscribe, user=self.request.user, anime__slug=request.POST["slug"]).delete()
        return redirect(reverse("account:subscribes"))


class AccountRegisterView(BreadCrumbsMixin, CreateView):
    """Register user account view"""
    model = get_user_model()
    form_class = UserCreationForm
    template_name = "account/register.jinja"

    def get_breadcrumbs(self):
        return [(_("Authorization"), reverse("account:login")), (_("Register"),)]

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('movie:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.lang = get_language()
        user.save()

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
        raise Http404(_("Incorrect token"))


class AccountEmailChangeView(LoginRequiredMixin, RedirectView):
    """Change user email View"""
    url = reverse_lazy("account:profile")

    def get(self, request, *args, **kwargs):
        user = request.user

        _email = kwargs['email']
        _token = kwargs['token']

        # Check if given hash valid

        check_token = salted_hmac(
            self.request.user.pk,
            f"{self.request.user.email}{_email}",
            secret=settings.SECRET_KEY,
            algorithm='sha1'
        ).hexdigest()[::2]

        if _token != check_token:
            raise Http404(_("Incorrect token"))

        messages.success(self.request, _('Email has been changed success'))
        user.email = _email
        user.save()

        return super().get(request, *args, **kwargs)


class AccountResetView(BreadCrumbsMixin, FormView):
    """Account reset password view"""
    form_class = AccountResetForm
    template_name = "account/reset.jinja"

    def get_breadcrumbs(self):
        return [(_("Authorization"), reverse("account:login")), (_("Reset"),)]

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("movie:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Send email with generated reset token"""
        _email = form.cleaned_data['email']
        user = get_user_model().objects.filter(email=_email).first()
        if user:
            token = generator.make_token(user)

            url = '{domain}{path}'.format(domain=Site.objects.get_current().domain,
                                          path=reverse("account:reset_confirm", kwargs={"email": _email, "token": token}))

            obj: AccountSettings = AccountSettings.get_solo()
            title = get_field_data_by_lang(obj, get_language(), "reset_email_title")
            context = get_field_data_by_lang(obj, get_language(), "reset_email").format(url=url)

            send_email(_email, title, context)

        return render(self.request, "account/reset_sent.jinja", context={})


class AccountResetConfirmView(FormView):
    """Confirm account reset password"""
    form_class = AccountResetConfirmForm
    template_name = "account/reset_confirm.jinja"

    def dispatch(self, request, *args, **kwargs):
        """If user or token incorrect 404"""
        if self.request.user.is_authenticated:
            return redirect(reverse("movie:home"))
        self.user = get_object_or_404(get_user_model(), email=kwargs['email'])

        if not generator.check_token(self.user, kwargs['token']):
            raise Http404(_("Incorrect token"))

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.user})
        return kwargs

    def form_valid(self, form):
        """Set user password from form and login"""
        self.user.set_password(form.cleaned_data["password1"])
        self.user.save()

        login(self.request, self.user)

        messages.success(self.request, _("Password changed success"))
        return redirect("account:profile")
