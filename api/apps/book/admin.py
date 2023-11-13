from django.contrib import admin

from apps.book.models import Book


@admin.register(Book)
class MessageTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
    )
