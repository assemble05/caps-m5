from django.db import models

# Create your models here.
class Review(models.Model):
    stars = models.PositiveIntegerField()
    description = models.CharField(max_length=255, null=True)