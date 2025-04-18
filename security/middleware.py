import uuid

import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from security.session_context import set_current_user, clear_current_user
from users.models import User


class JwtMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            header = request.META.get("HTTP_AUTHORIZATION")
            if not header or not header.startswith("Bearer "):
                return

            token = header.split("Bearer ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            user_uuid = uuid.UUID(user_id)
            user = User.objects.get(id=user_uuid)

            set_current_user(user)

        except Exception as e:
            print(f"Middleware error: {e}")
            clear_current_user()
