from datetime import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shopping_carts.models import ShoppingCart
from shopping_carts.serializers import CreateShoppingCartSerializer


class GetOrCreateShoppingCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart, created = ShoppingCart.objects.get_or_create(
            user=user,
            defaults={
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        )
        serializer = CreateShoppingCartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
