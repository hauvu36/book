from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, mixins
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


from apps.core.utils import get_mime_type
from apps.book.api import serializers
from apps.book.services import BookService
from apps.book.exceptions import FileEmptyException, BookDoesNotExistException, FileImageException


class UpdateAPIView(mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    """
    Concrete view for updating a model instance.
    """

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.BookSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permission() for permission in (AllowAny,)]
        return super().get_permissions()

    def get_queryset(self):
        author = self.request.query_params.get("author", None)
        publish_date = self.request.query_params.get("publish_date", None)
        return BookService.get_list_book(author=author, publish_date=publish_date)

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: openapi.Response("response description", serializers.BookSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        query_serializer=serializers.BookQuerySerializer,
        responses={status.HTTP_200_OK: openapi.Response("response description", serializers.BookSerializer)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookUpdateDeleteDetailView(mixins.RetrieveModelMixin,
                                 UpdateAPIView,
                                 mixins.DestroyModelMixin):
    serializer_class = serializers.BookSerializer

    def get_permissions(self):
        if self.request.method in "GET":
            return [permission() for permission in (AllowAny,)]
        return super().get_permissions()

    def get_object(self):
        book = BookService.get_book_by_id(self.kwargs.get("book_id", None))
        if not book:
            raise BookDoesNotExistException()
        return book

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Response("response description", serializers.BookSerializer)},
    )
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: openapi.Response("response description", serializers.BookSerializer)},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="delete_book",
        operation_id="delete_book",
    )
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BookUploadCoverImageView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        request_body=serializers.BookUploadImageBodySerializer,
        responses={
            status.HTTP_200_OK: openapi.Response("response description", serializers.BookSerializer)})
    def patch(self, request, *args, **kwargs):
        book_id = self.kwargs.get("book_id", None)
        file = request.FILES.get("file", None)
        if not file:
            raise FileEmptyException()
        type_file: str = get_mime_type(file.name)
        if "image" not in type_file:
            raise FileImageException()
        book = BookService.get_book_by_id(book_id=book_id)
        if not book:
            raise BookDoesNotExistException()
        book.cover.save(file.name, file, save=True)
        return Response(status=status.HTTP_200_OK, data=serializers.BookUploadImageSerializer(book).data)
