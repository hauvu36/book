from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status

from apps.users.api import serializers


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Response("response description", serializers.UserSerializer)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=serializers.UserSerializer,
        responses={status.HTTP_200_OK: openapi.Response("response description", serializers.UserSerializer)},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
