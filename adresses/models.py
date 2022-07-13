from django.db import models

# Create your models here.
class Address(models.Model):
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.PositiveIntegerField()
    complementet = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=12)

