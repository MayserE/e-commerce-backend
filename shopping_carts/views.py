from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from security.session_context import get_current_user
from shopping_carts.models import ShoppingCart, ShoppingCartProduct
from shopping_carts.serializers import GetCurrentShoppingCartSerializer, NewShoppingCartProductSerializer, \
    ShoppingCartProductSerializer, AddShoppingCartProductSerializer


class GetCurrentShoppingCartView(APIView):
    def get(self, request):
        user = get_current_user()
        if not user:
            return Response({"detail": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)
        shopping_cart = ShoppingCart.objects.filter(user=user).prefetch_related('shopping_cart_products').first()
        return Response({
            "currentShoppingCart": GetCurrentShoppingCartSerializer(shopping_cart).data if shopping_cart else None
        })


class AddShoppingCartProductView(APIView):
    def post(self, request):
        serializer = AddShoppingCartProductSerializer(data=request.data)
        if serializer.is_valid():
            new_shopping_cart_products = serializer.data['new_shopping_cart_products']
            user = get_current_user()
            if not user:
                return Response({"detail": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)
            try:
                shopping_cart = ShoppingCart.objects.get(user=user)
            except ShoppingCart.DoesNotExist:
                shopping_cart = ShoppingCart(
                    user=user,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                shopping_cart.save()
            created_shopping_cart_products = []
            for new_shopping_cart_product in new_shopping_cart_products:
                product = Product.objects.get(id=new_shopping_cart_product['product_id'])
                shopping_cart_product = ShoppingCartProduct(
                    shopping_cart=shopping_cart,
                    product=product,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    quantity=new_shopping_cart_product['quantity']
                )
                shopping_cart_product.save()
                created_shopping_cart_products.append(ShoppingCartProductSerializer(shopping_cart_product).data)

            return Response({
                'id': shopping_cart.id,
                'user_id': shopping_cart.user_id,
                'created_at': shopping_cart.created_at,
                'updated_at': shopping_cart.updated_at,
                'shopping_cart_products': created_shopping_cart_products,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
