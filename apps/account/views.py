from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator as generator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django_jinja.views.generic import CreateView, UpdateView

from .forms import UserCreationForm, AccountUpdateForm


class AccountProfileView(LoginRequiredMixin, UpdateView):
    """Change user profile view"""
    model = get_user_model()
    template_name = "account/profile.jinja"
    success_url = reverse_lazy('profile')
    form_class = AccountUpdateForm

    def get_object(self, queryset=None):
        return self.request.user


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
