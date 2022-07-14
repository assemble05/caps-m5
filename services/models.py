import uuid

from django.db import models


# Create your models here.
class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    id_provider = models.CharField(max_length=255, null=True)

    address = models.OneToOneField(
        "adresses.Address", on_delete=models.CASCADE, null=True
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        related_name="services",
        null=True,
    )
    candidates = models.ManyToManyField("users.User", related_name="candidacies")
