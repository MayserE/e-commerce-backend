import uuid

from django.db import models

from orders.models import Order


class PaymentMethod(models.TextChoices):
    QR = 'QR',
    CREDIT_CAR = 'CREDIT_CAR',
    DEBIT_CART = 'DEBIT_CART',







class Payment(models.Model):
    class Meta:
        db_table = 'payments'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)

