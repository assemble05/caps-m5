from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from users.utils import CustomUserManager

class User(AbstractUser):
      id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False
       )
      email = models.EmailField(max_length=255, unique=True)
      username = models.CharField(unique=False, null=True, max_length=255)
      first_name= models.CharField(max_length=50)
      last_name= models.CharField(max_length=50)
      updated_at = models.DateTimeField(auto_now=True)
      
      is_provider =  models.BooleanField()
      description = models.CharField(max_length=255, null=True)

      address = models.OneToOneField('adresses.Address', on_delete = models.CASCADE)

      USERNAME_FIELD = "email"
      REQUIRED_FIELDS =["first_name", "last_name"]
      objects = CustomUserManager()