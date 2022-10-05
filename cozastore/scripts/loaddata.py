from store.models import Product, Category
import csv
from django.conf import settings

settings.configure()


""""Use this script to populate the database with Product objects """

def run():
    with open('products.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        # Product.objects.all().delete()
        for row in reader:
            print(row)
            category, _ = Category.objects.get_or_create(name=row[5])
            product = Product(name=row[0],
                        slug=row[1],
                        price=row[2],
                        discount_price=row[3],
                        description=row[4],
                        category=category,
                        color_or_version=row[6],
                        tags=row[7],
                        )
            product.save()