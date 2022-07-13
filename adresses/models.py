from django.db import models
import uuid

# Create your models here.
class Address(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False
       )
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.PositiveIntegerField()
    complementet = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=12)
