import uuid

from django.db import models

from products.models import Product
from users.models import User


class ShoppingCart(models.Model):
    class Meta:
        db_table = 'shopping_carts'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class ShoppingCartProduct(models.Model):
    class Meta:
        db_table = 'shopping_cart_products'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shopping_cart = models.ForeignKey(ShoppingCart, related_name='shopping_cart_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    quantity = models.PositiveIntegerField()
