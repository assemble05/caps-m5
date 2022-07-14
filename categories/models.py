import uuid

from django.db import models


# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    providers = models.ManyToManyField("users.User", related_name="categories")
