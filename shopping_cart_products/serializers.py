from rest_framework import serializers

from products.serializers import ProductSerializer
from shopping_cart_products.models import ShoppingCartProduct
from shopping_carts.models import ShoppingCart
from shopping_carts.serializers import ShoppingCartSerializer


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    shopping_cart = ShoppingCartSerializer(read_only=True)

    class Meta:
        model = ShoppingCartProduct
        fields = ['id','shopping_cart', 'product', 'quantity', 'created_at', 'updated_at']


class AddProductToShoppingCartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    guest_cart_id = serializers.UUIDField(required=False)


class GetProductFromShoppingCartSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    name = serializers.CharField()
    price = serializers.CharField()
    quantity = serializers.IntegerField()

    class Meta:
        model = ShoppingCartProduct
        fields = ['product_id', 'name', 'price', 'quantity']

class CreateShoppingCartProductSerializer(serializers.Serializer):
    product = ProductSerializer(read_only=True)
    shopping_cart = ShoppingCartSerializer(read_only=True)
    shopping_cart_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = ShoppingCartProduct
        fields = ['product', 'shopping_cart', 'quantity', 'created_at', 'updated_at']

        def create(self, validated_data):
            try:
                shopping_car = ShoppingCartProduct.objects.get(id=validated_data['shopping_cart_id'])
            except ShoppingCart.DoesNotExist:
                pass

            shopping_car_product = ShoppingCartProduct(
                shopping_cart = shopping_car,
                product = validated_data['product'],
                quantity = validated_data['quantity'],
                created_at = validated_data['created_at'],
                updated_at = validated_data['updated_at']
            )
            shopping_car_product.save()
            return shopping_car_product

class UpdateQuantitySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)