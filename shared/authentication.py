import uuid
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings

from users.models import User  # <-- usa directamente tu modelo real

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            user_uuid = uuid.UUID(user_id)
            print("🔐 user_id del token:", user_id)
            print("🔍 Consultando User con UUID:", user_uuid)
        except Exception:
            raise Exception("Token inválido: no se pudo extraer el UUID")

        try:
            user = User.objects.get(id=user_uuid)
            print("✅ Usuario encontrado:", user.email)
        except User.DoesNotExist:
            print("❌ No se encontró usuario con UUID:", user_uuid)
            raise Exception("Usuario no encontrado con el ID dado")

        return user
