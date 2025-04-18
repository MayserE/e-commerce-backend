from datetime import datetime

from rest_framework import serializers

from shopping_carts.models import ShoppingCart
from users.models import User
from users.serializers import UserSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class CreateShoppingCartSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        shopping_cart = ShoppingCart(
            user=user,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        shopping_cart.save()
        return shopping_cart
