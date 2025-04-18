import uuid

from django.db import models

from categories.models import Category


class Product(models.Model):
    class Meta:
        db_table = 'products'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    detail = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)


class ProductImage(models.Model):
    class Meta:
        db_table = 'product_images'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    url = models.TextField()
