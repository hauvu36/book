from django.urls import path

from apps.users_auth.api.views import (
    CustomLoginView,
    CustomPasswordChangeView,
    CustomRegisterView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path("auth/registration/", CustomRegisterView.as_view(), name="custom_register"),
    path("auth/login/", CustomLoginView.as_view(), name="custom_login"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="custom_refresh"),
    path("auth/password/change/", CustomPasswordChangeView.as_view(), name="password_change"),
]
