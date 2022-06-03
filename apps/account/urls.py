from django.urls import path
import django.contrib.auth.views as auth_views
from apps.account.views import ValidateEmailView, AccountRegisterView

urlpatterns = [
    path("verify/<str:username>/<str:token>/", ValidateEmailView.as_view(), name="verify"),

    path("changepass/", auth_views.PasswordChangeView.as_view(template_name="account/password_change.jinja"),
         name='password_change'),
    path("changepass/done/", auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.jinja"),
         name='password_change_done'),

    path("login/", auth_views.LoginView.as_view(template_name="account/login.jinja"), name="login"),
    path("register/", AccountRegisterView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]
