from datetime import datetime

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User, UserRole, UserStatus


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'role', 'status']

    def create(self, validated_data):
        user = User(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            name=validated_data['name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            document_type=validated_data['document_type'],
            document_number=validated_data['document_number'],
            birthdate=validated_data['birthdate']
        )
        user.save()
        return user
