from django.db import models

from core.models import TimeStampeModel

# Create your models here.

class User(TimeStampeModel):
    korean_name  = models.CharField(max_length=100)
    email        = models.EmailField(max_length=100, unique=True)
    password     = models.CharField(max_length=400)
    address      = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'