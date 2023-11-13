from django.urls import include, path

urlpatterns = [
    path("", include("apps.users_auth.api.urls")),
    path("book/", include("apps.book.api.urls")),
]
