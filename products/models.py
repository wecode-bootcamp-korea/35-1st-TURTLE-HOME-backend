from django.db import models

from core.models import TimeStampeModel

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name      = models.CharField(max_length=50)
    image_url = models.CharField(max_length=500)
    category  = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class Size(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'sizes'

class Product(TimeStampeModel):
    name         = models.CharField(max_length=100)
    number       = models.CharField(max_length=100)
    description  = models.CharField(max_length=200)
    image_url    = models.CharField(max_length=500)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

class ProductOption(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.ForeignKey('Size', on_delete=models.CASCADE)
    price   = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'products_options'