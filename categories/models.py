import uuid

from django.db import models


class Category(models.Model):
    class Meta:
        db_table = 'categories'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=128, unique=True)
    image_url = models.TextField(null=True, blank=True)
