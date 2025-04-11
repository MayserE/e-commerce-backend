from rest_framework.permissions import BasePermission

from users.models import UserRole


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'role')
            and request.user.role == UserRole.ADMIN
        )