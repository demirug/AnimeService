from django.urls import path
import django.contrib.auth.views as auth_views
from apps.account.views import ValidateEmailView

urlpatterns = [
    path("verify/<str:username>/<str:token>/", ValidateEmailView.as_view(), name="verify"),
    path("login/", auth_views.LoginView.as_view(template_name="account/login.jinja"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]
