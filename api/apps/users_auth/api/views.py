from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_auth.views import LoginView, PasswordChangeView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny

from apps.users.api.serializers import (
    ResponseChangePasswordSerializer,
    ResponseTokenSerializer,
    UserLoginBodySerializer,
    UserRegisterSerializer,
    UserSerializer,
    UserTokenRefreshSerializer,
)


class CustomRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    sensitive_post_parameters_m = method_decorator(sensitive_post_parameters("password1", "password2"))

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @classmethod
    def get_response_data(cls, user):
        if settings.ACCOUNT_EMAIL_VERIFICATION == settings.ACCOUNT_EMAIL_VERIFICATION_MANDATORY:
            return {"detail": _("Verification e-mail sent.")}
        return UserSerializer(user).data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None)
        return user

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response("response description", UserSerializer)},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        return Response(self.get_response_data(user), status=status.HTTP_201_CREATED)


class ResponseTokenView(object):
    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class().get_token(self.user)
        access = serializer.access_token
        expire = access.current_time + access.lifetime
        data = {
            "refresh": str(serializer),
            "access": str(access),
            "expire": int(expire.timestamp()),
        }
        return Response(data, status=status.HTTP_200_OK)


class CustomLoginView(ResponseTokenView, LoginView):
    @swagger_auto_schema(
        request_body=UserLoginBodySerializer,
        responses={status.HTTP_200_OK: openapi.Response("response description", ResponseTokenSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = UserTokenRefreshSerializer

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Response("response description", ResponseTokenSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Response("response description", ResponseChangePasswordSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

