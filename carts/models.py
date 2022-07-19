from django.db import models

from core.models import TimeStampedModel

# Create your models here.

class Cart(TimeStampedModel):
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product_option = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)
    quantity       = models.IntegerField(default=1)

    class Meta:
        db_table = 'carts'