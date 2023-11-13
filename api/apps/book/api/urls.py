from django.urls import path

from apps.book.api.views import BookListCreateView, BookUpdateDeleteDetailView, BookUploadCoverImageView

urlpatterns = [
    path("", BookListCreateView.as_view(), name="book_list_create"),
    path("<int:book_id>/", BookUpdateDeleteDetailView.as_view(), name="book_update_delete_detail"),
    path("cover-image/<int:book_id>/", BookUploadCoverImageView.as_view(), name="book_upload_cover_image"),
]
