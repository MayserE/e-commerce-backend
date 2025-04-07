import uuid

from django.db import models

from branch_offices.models import BranchOffice
from products.models import Product


class BranchOfficeProduct(models.Model):
    class Meta:
        db_table = 'branch_office_products'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    stock = models.PositiveIntegerField()
