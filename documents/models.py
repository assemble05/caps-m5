import uuid

from django.db import models


# Create your models here.
class Documents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField(max_length=25)
    rg = models.CharField(max_length=8)
    is_driverLicense = models.CharField(max_length=35)
    driveType = models.CharField(max_length=105)
    
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, null=True
    )