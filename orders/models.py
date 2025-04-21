import uuid

from django.db import models
from django.db.models import TextField

from branch_office_products.models import BranchOfficeProduct
from users.models import User


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING',
    EXECUTED = 'EXECUTED',


class Order(models.Model):
    class Meta:
        db_table = 'orders'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=OrderStatus.choices)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cancellation_reason = TextField(null=True, blank=True)


class OrderBranchOfficeProduct(models.Model):
    class Meta:
        db_table = 'order_branch_office_products'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    branch_office_product = models.ForeignKey(BranchOfficeProduct, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
