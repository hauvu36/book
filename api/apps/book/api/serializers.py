from datetime import date

from rest_framework import serializers

from apps.book.models import Book
from apps.core.utils import parse_datetime
from apps.book.exceptions import PublishDateException


class PublishDateField(serializers.Serializer):
    def to_internal_value(self, publish_date: str) -> date:
        publish_date = parse_datetime(publish_date)
        if not publish_date:
            raise PublishDateException()
        return publish_date

    def to_representation(self, data):
        if not data:
            return None
        elif isinstance(data, str):
            return data
        else:
            return data.strftime("%m-%d-%Y")


class BookSerializer(serializers.ModelSerializer):
    publish_date = PublishDateField(required=True, help_text="The format should be mm-dd-yy")

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "publish_date",
            "ISBN",
            "price",
            "cover_image"
        )
        read_only_fields = (
            "cover_image",
        )


class BookUploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "publish_date",
            "ISBN",
            "price",
            "cover_image",
        )
        read_only_fields = (
            "title",
            "author",
            "publish_date",
            "ISBN",
            "price",
            "cover_image"
        )


class BookQuerySerializer(serializers.Serializer):
    author = serializers.CharField(required=False)
    publish_date = serializers.CharField(required=False)


class BookUploadImageBodySerializer(serializers.Serializer):
    file = serializers.ImageField(required=True, allow_empty_file=False)
