import uuid

from django.db import models

from products.models import Product
from shopping_carts.models import ShoppingCart


class ShoppingCartProduct(models.Model):
    class Meta:
        db_table = 'shopping_cart_products'
        constraints = [
            models.UniqueConstraint(fields=['shopping_cart', 'product'], name='unique_cart_product')
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    quantity = models.PositiveIntegerField()

