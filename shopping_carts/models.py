import uuid

from django.db import models

from users.models import User


class ShoppingCart(models.Model):
    class Meta:
        db_table = 'shopping_carts'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
