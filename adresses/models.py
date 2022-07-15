import uuid

from django.db import models


# Create your models here.
class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=25)
    state = models.CharField(max_length=35)
    city = models.CharField(max_length=35)
    street = models.CharField(max_length=105)
    number = models.PositiveIntegerField()
    complement = models.CharField(max_length=255, null=True)
    zip_code = models.CharField(max_length=15)
