from datetime import datetime
from decimal import Decimal

from rest_framework import serializers

from orders.models import Order
from shopping_carts.models import ShoppingCart, ShoppingCartProduct


class GenerateOrderSerializer(serializers.Serializer):
    def create(self, validated_data):
        user = self.context['request'].user

        cart = ShoppingCart.objects.filter(user=user).first()
        if not cart:
            raise serializers.ValidationError("El carrito no existe.")

        cart_products = ShoppingCartProduct.objects.filter(shopping_cart=cart)
        if not cart_products.exists():
            raise serializers.ValidationError("El carrito está vacío.")

        total = Decimal("0.00")
        product_list = []

        for item in cart_products:
            product = item.product
            quantity = item.quantity
            price = product.price
            total += price * quantity

            product_list.append({
                "id": str(product.id),
                "name": product.name,
                "detail": product.detail,
                "price": str(price),
                "quantity": quantity
            })

        order = Order.objects.create(
            user=user,
            status="PENDING",
            total_amount=total,
            cancellation_reason="",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        order.product_list = product_list  # Atributo temporal solo para la respuesta
        order.created_at_display = order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        self.instance = order
        return order

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "products": getattr(instance, 'product_list', []),
            "total_amount": instance.total_amount,
            "created_at": getattr(instance, 'created_at_display', instance.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        }


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "total_amount", "status", "created_at"]


class OrderDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "products", "total_amount", "created_at"]

    def get_products(self, obj):
        return getattr(obj, 'product_list', [])
