from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.test import TestCase
from django.db.models import QuerySet

from apps.book.models import Book
from apps.users.models import User
from apps.core.utils import get_utc_now


class BookModelTest(TestCase):
    def test_book_creation(self):
        book = Book.objects.create(
            title="Don Quixote",
            author="Miguel de Cervantes",
            publish_date=get_utc_now(),
            ISBN="123456",
            price=100,
        )
        self.assertTrue(isinstance(book, Book))
        self.assertEqual(book.__str__(), book.title)

    def test_book_get_detail(self):
        self.test_book_creation()
        book = Book.objects.filter(title="Don Quixote").first()
        self.assertTrue(isinstance(book, Book))
        self.assertEqual(book.__str__(), book.title)

    def test_book_get_list(self):
        self.test_book_creation()
        queryset = Book.objects.filter(title="Don Quixote")
        self.assertTrue(isinstance(queryset, QuerySet))

    def test_book_update(self):
        self.test_book_creation()
        book = Book.objects.filter(title="Don Quixote").first()
        book.title = "Lord of the Rings"
        book.author = "J.R.R. Tolkien"
        book.save()
        self.assertEqual("Lord of the Rings", book.title)
        self.assertEqual("J.R.R. Tolkien", book.author)

    def test_book_deletion(self):
        self.test_book_creation()
        book = Book.objects.filter(title="Don Quixote").first()
        book.delete()
        self.assertEqual(False, Book.objects.filter(title="Don Quixote").exists())


class BookViewTest(APITestCase):
    urlpatterns = [
        path("v1/", include("config.api")),
    ]

    def setUp(self):
        self.user = User.objects.create_user(
            username="test1",
            email="test1@gmail.com",
            password="123456x@X",
            first_name="Unit",
            last_name="Test 1",
        )

        self.client = APIClient()
        url = reverse("custom_login")
        resp = self.client.post(
            url, {"email": "test1@gmail.com", "password": "123456x@X"}, format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in resp.data)
        self.token = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_book_create(self):
        url = reverse("book_list_create")
        data = {
            "title": "Lord of the Rings",
            "author": "J.R.R. Tolkien",
            "publish_date": "14-11-2023",  # MM-DD-YY
            "ISBN": "123321",
            "price": 200
        }
        response = self.client.post(url, data=data, format="json")
        self.book_id = response.data["id"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_update(self):
        self.test_book_create()
        url = reverse("book_update_delete_detail", kwargs={"book_id": self.book_id})
        data = {
            "title": "Don Quixote",
            "author": "Miguel de Cervantes",
            "publish_date": "13-11-2023",  # MM-DD-YY
            "ISBN": "123456",
            "price": 100
        }
        response = self.client.patch(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_get_list(self):
        self.test_book_create()
        url = reverse("book_list_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_get_detail(self):
        self.test_book_create()
        url = reverse("book_update_delete_detail", kwargs={"book_id": self.book_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_delete(self):
        self.test_book_create()
        url = reverse("book_update_delete_detail", kwargs={"book_id": self.book_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
