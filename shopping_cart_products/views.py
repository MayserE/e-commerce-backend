from datetime import datetime

from django.db.models import Sum, Min, Max
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from shopping_cart_products.models import ShoppingCartProduct
from shopping_cart_products.serializers import AddProductToShoppingCartSerializer, ShoppingCartProductSerializer, \
    UpdateQuantitySerializer
from shopping_carts.models import ShoppingCart


class AddProductToShoppingCartView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddProductToShoppingCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        guest_cart_id = serializer.validated_data.get('guest_cart_id')
        product = get_object_or_404(Product, id=product_id)

        cart = None

        if request.user and request.user.is_authenticated:
            cart, _ = ShoppingCart.objects.get_or_create(
                user=request.user,
                defaults={'created_at': datetime.now(), 'updated_at': datetime.now()}
            )

            if guest_cart_id:
                guest_cart = ShoppingCart.objects.filter(id=guest_cart_id, user__isnull=True).first()
                if guest_cart:
                    self._merge_carts(guest_cart, cart)
                    guest_cart.delete()

        else:
            if guest_cart_id:
                cart = ShoppingCart.objects.filter(id=guest_cart_id, user__isnull=True).first()
                if not cart:
                    cart = ShoppingCart.objects.create(
                        id=guest_cart_id,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
            else:
                return Response({'detail': 'Guest-Cart-Id is required for unauthenticated users.'},
                                status=status.HTTP_400_BAD_REQUEST)

        cart_product = ShoppingCartProduct.objects.filter(shopping_cart=cart, product=product).first()
        if cart_product:
            cart_product.quantity += quantity
            cart_product.updated_at = datetime.now()
            cart_product.save()
        else:
            cart_product = ShoppingCartProduct.objects.create(
                shopping_cart=cart,
                product=product,
                quantity=quantity,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

        return Response(ShoppingCartProductSerializer(cart_product).data, status=status.HTTP_200_OK)

    def _merge_carts(self, guest_cart, user_cart):
        guest_items = ShoppingCartProduct.objects.filter(shopping_cart=guest_cart)

        for guest_item in guest_items:
            existing = ShoppingCartProduct.objects.filter(
                shopping_cart=user_cart,
                product=guest_item.product
            ).first()

            if existing:
                existing.quantity += guest_item.quantity
                existing.updated_at = datetime.now()
                existing.save()
            else:
                ShoppingCartProduct.objects.create(
                    shopping_cart=user_cart,
                    product=guest_item.product,
                    quantity=guest_item.quantity,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )


class GetProductFromShoppingCartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        guest_cart_id = request.headers.get('Guest-Cart-Id')
        cart = None

        if request.user and request.user.is_authenticated:
            cart = ShoppingCart.objects.filter(user=request.user).first()
        elif guest_cart_id:
            cart = ShoppingCart.objects.filter(id=guest_cart_id, user__isnull=True).first()

        if not cart:
            return Response([], status=status.HTTP_200_OK)

        grouped_items = (
            ShoppingCartProduct.objects
            .filter(shopping_cart=cart)
            .values('product')
            .annotate(
                quantity=Sum('quantity'),
                created_at=Min('created_at'),
                updated_at=Max('updated_at')
            )
        )

        result = []
        for item in grouped_items:
            product_id = item['product']
            instance = ShoppingCartProduct.objects.filter(shopping_cart=cart, product_id=product_id).first()
            if instance:
                instance.quantity = item['quantity']
                instance.created_at = item['created_at']
                instance.updated_at = item['updated_at']
                result.append(instance)

        serializer = ShoppingCartProductSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BaseCartActionView(APIView):
    permission_classes = [AllowAny]

    def get_cart(self, request):
        guest_cart_id = request.headers.get('Guest-Cart-Id')
        if request.user and request.user.is_authenticated:
            return ShoppingCart.objects.filter(user=request.user).first()
        elif guest_cart_id:
            return ShoppingCart.objects.filter(id=guest_cart_id, user__isnull=True).first()
        return None

    def get_cart_product(self, cart, product_id):
        product = get_object_or_404(Product, id=product_id)
        return ShoppingCartProduct.objects.filter(shopping_cart=cart, product=product).first()


class IncreaseTheQuantityOfProductView(BaseCartActionView):
    def patch(self, request, product_id):
        cart = self.get_cart(request)
        if not cart:
            return Response({'detail': 'Carrito de compras no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        cart_product = self.get_cart_product(cart, product_id)
        if not cart_product:
            return Response({'detail': 'El producto no está en el carrito'}, status=status.HTTP_404_NOT_FOUND)

        cart_product.quantity += 1
        cart_product.updated_at = datetime.now()
        cart_product.save()

        return Response(ShoppingCartProductSerializer(cart_product).data, status=status.HTTP_200_OK)


class ClearShoppingCartView(BaseCartActionView):
    def delete(self, request):
        cart = self.get_cart(request)
        if not cart:
            return Response({'detail': 'Carrito no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        ShoppingCartProduct.objects.filter(shopping_cart=cart).delete()
        cart.updated_at = datetime.now()
        cart.save()

        return Response({'detail': 'No hay artículos en su carrito de compras.'}, status=status.HTTP_204_NO_CONTENT)


class UpdateQuantityOfProductView(BaseCartActionView):
    def patch(self, request, product_id):
        serializer = UpdateQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_quantity = serializer.validated_data['quantity']

        cart = self.get_cart(request)
        if not cart:
            return Response({'detail': 'Carrito no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        cart_product = self.get_cart_product(cart, product_id)
        if not cart_product:
            return Response({'detail': 'Producto no encontrado en el carrito'}, status=status.HTTP_404_NOT_FOUND)

        if new_quantity <= 0:
            cart_product.delete()
            cart.updated_at = datetime.now()
            cart.save()
            return Response({'detail': 'Producto eliminado del carrito'}, status=status.HTTP_204_NO_CONTENT)

        cart_product.quantity = new_quantity
        cart_product.updated_at = datetime.now()
        cart_product.save()

        return Response(ShoppingCartProductSerializer(cart_product).data, status=status.HTTP_200_OK)


class DecreaseTheQuantityOfProductView(BaseCartActionView):
    def patch(self, request, product_id):
        cart = self.get_cart(request)
        if not cart:
            return Response({'detail': 'Carrito no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        cart_product = self.get_cart_product(cart, product_id)
        if not cart_product:
            return Response({'detail': 'Producto no encontrado en el carrito'}, status=status.HTTP_404_NOT_FOUND)

        if cart_product.quantity == 1:
            cart_product.delete()
            cart.updated_at = datetime.now()
            cart.save()
            return Response({'detail': 'Producto eliminado del carrito'}, status=status.HTTP_204_NO_CONTENT)

        cart_product.quantity -= 1
        cart_product.updated_at = datetime.now()
        cart_product.save()

        return Response(ShoppingCartProductSerializer(cart_product).data, status=status.HTTP_200_OK)


class RemoveProductFromShoppingCartView(BaseCartActionView):
    def delete(self, request, product_id):
        cart = self.get_cart(request)
        if not cart:
            return Response({'detail': 'Carrito de compras no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        cart_product = self.get_cart_product(cart, product_id)
        if not cart_product:
            return Response({'detail': 'Producto no encontrado en el carrito'}, status=status.HTTP_404_NOT_FOUND)

        cart_product.delete()
        return Response({'detail': 'Producto eliminado correctamente del carrito'}, status=status.HTTP_200_OK)


