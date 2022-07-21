import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zara.settings')
django.setup()

from products.models import Category, SubCategory, Size, Product, ProductOption

CSV_PATH_CATEGORIES     = './csv/category.csv'
CSV_PATH_SUBCATEGORIES  = './csv/subcategory.csv'
CSV_PATH_SIZES          = './csv/size.csv'
CSV_PATH_PRODUCTS       = './csv/product.csv'
CSV_PATH_PRODUCTOPTIONS = './csv/product_option.csv'


with open(CSV_PATH_CATEGORIES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Category.objects.create(
            name = row[0]
        )

with open(CSV_PATH_SUBCATEGORIES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        print(row)
        SubCategory.objects.create(
            category_id = row[0],
            name        = row[1],
            image_url   = row[2]
        )

with open(CSV_PATH_SIZES) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Size.objects.create(
            name = row[0]
        )
        
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        Product.objects.create(
            name            = row[0],
            number          = row[1],
            description     = row[2],
            image_url       = row[3],
            sub_category_id = row[4]
        )
        
with open(CSV_PATH_PRODUCTOPTIONS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        ProductOption.objects.create(
            product_id = row[0],
            size_id    = row[1],
            price      = row[2]
        )