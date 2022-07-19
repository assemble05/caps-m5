import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.utils import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=55, unique=True)
    username = models.CharField(unique=False, null=True, max_length=35)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    updated_at = models.DateTimeField(auto_now=True)

    is_provider = models.BooleanField(default=True)
    description = models.CharField(max_length=255, null=True)

    address = models.OneToOneField(
        "adresses.Address", on_delete=models.CASCADE, null=True, related_name="user"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()
