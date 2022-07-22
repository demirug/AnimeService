from django.urls import path, include
from apps.account.views import *

urlpatterns = [
    path("verify/<str:username>/<str:token>/", ValidateEmailView.as_view(), name="verify"),
    path("login/", AccountLoginView.as_view(), name="login"),
    path("register/", AccountRegisterView.as_view(), name="register"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),

    path("profile/", include([
        path("", AccountProfileView.as_view(), name="profile"),
        path("subscribes/", AccountSubscribersView.as_view(), name="subscribes"),
        path("change_email/<str:email>/<str:token>/", AccountEmailChangeView.as_view(), name="change_email"),
        path("changepass/", AccountChangePasswordView.as_view(), name="password_change"),
    ])),

    path("reset/", include([
        path("", AccountResetView.as_view(), name="reset"),
        path("<str:email>/<str:token>/", AccountResetConfirmView.as_view(), name="reset_confirm"),
    ])),
]
