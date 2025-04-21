from datetime import datetime

from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer
from security.session_context import get_current_user
from shopping_carts.models import ShoppingCart, ShoppingCartProduct


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    shopping_cart_id = serializers.UUIDField(source='shopping_cart.id')
    product = ProductSerializer()

    class Meta:
        model = ShoppingCartProduct
        fields = ['id', 'shopping_cart_id', 'product', 'created_at', 'updated_at', 'quantity']


class GetCurrentShoppingCartSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id')
    shopping_cart_products = ShoppingCartProductSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ['id', 'user_id', 'created_at', 'updated_at', 'shopping_cart_products']


class NewShoppingCartProductSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class AddShoppingCartProductSerializer(serializers.Serializer):
    new_shopping_cart_products = NewShoppingCartProductSerializer(many=True)
