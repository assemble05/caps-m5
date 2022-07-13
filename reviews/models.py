from django.db import models
import uuid

# Create your models here.
class Review(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False
       )
    stars = models.PositiveIntegerField()
    description = models.CharField(max_length=255, null=True)