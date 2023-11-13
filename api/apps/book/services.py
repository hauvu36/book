import typing

from django.db.models import Q, QuerySet

from apps.book.models import Book
from apps.core.utils import parse_datetime
from apps.book.exceptions import PublishDateException


class BookService(object):
    @classmethod
    def get_book_by_id(cls, book_id: int) -> typing.Optional[Book]:
        return Book.objects.filter(id=book_id).first()

    @classmethod
    def get_list_book(cls, author: str = None, publish_date: str = None) -> QuerySet:
        query = Q()
        if author:
            query = query & Q(author=author)
        if publish_date:
            publish_date = parse_datetime(publish_date)
            if not publish_date:
                raise PublishDateException()
            query = query & Q(publish_date=publish_date)
        return Book.objects.filter(query).order_by("-created")
