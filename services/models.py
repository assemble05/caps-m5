from django.db import models

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField()
    is_active =  models.BooleanField(default=True)
    is_delete =  models.BooleanField(default=False)
    id_proveder = models.CharField(max_length=255, null=True)

    address = models.OneToOneField('adresses.Address', on_delete = models.CASCADE)