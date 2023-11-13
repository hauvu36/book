from model_utils.models import TimeStampedModel
from django.db import models

from django.conf import settings


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Book(TimeStampedModel):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publish_date = models.DateField()
    ISBN = models.CharField(max_length=50)
    price = models.FloatField(max_length=25, help_text="dollar unit")
    cover = models.ImageField(verbose_name="Book cover", upload_to=upload_to, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def cover_image(self):
        return f"{settings.BASE_URL}{self.cover.url}" if self.cover else None
