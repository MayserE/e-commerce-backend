import uuid

from django.db import models


class UserStatus(models.TextChoices):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class UserRole(models.TextChoices):
    ADMIN = 'ADMIN'
    BRANCH_OFFICE_MEMBER = 'BRANCH_OFFICE_MEMBER'
    CLIENT = 'CLIENT'


class UserDocumentType(models.TextChoices):
    CI = 'CI'
    NIT = 'NIT'
    FOREIGN_PASSPORT = 'FOREIGN_PASSPORT'


class User(models.Model):
    class Meta:
        db_table = 'users'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.EmailField(unique=True)
    password = models.TextField()
    role = models.CharField(max_length=32, choices=UserRole.choices)
    status = models.CharField(max_length=32, choices=UserStatus.choices)
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    document_type = models.CharField(max_length=16, choices=UserDocumentType.choices)
    document_number = models.CharField(max_length=32)
    birthdate = models.DateField()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
