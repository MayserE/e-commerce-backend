from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from users.models import UserStatus, User


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Credenciales inválidas.')

        if not check_password(password, user.password):
            raise serializers.ValidationError('Credenciales inválidos.')

        if user.status != UserStatus.ACTIVE:
            raise serializers.ValidationError('El usuario no está habilitado para iniciar sesión')

        token = AccessToken()
        token['user_id'] = str(user.id)
        expires_at = timezone.now() + token.lifetime

        return {
            "accessToken": str(token),
            "accessTokenExpiresAt": expires_at.isoformat()
        }
