import uuid

from django.db import models


class BranchOfficeStatus(models.TextChoices):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class BranchOffice(models.Model):
    class Meta:
        db_table = 'branch_offices'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    location = models.TextField()
    status = models.CharField(max_length=32, choices=BranchOfficeStatus.choices)
