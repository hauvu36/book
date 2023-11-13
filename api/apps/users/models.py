from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        name = f"{self.first_name} {self.last_name}"
        if not name.strip():
            name = self.username
        return name

    def save(self, *args, **kwargs):
        self.first_name = str(self.first_name).strip()
        self.last_name = str(self.last_name).strip()
        return super().save(*args, **kwargs)
