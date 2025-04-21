from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from orders.serializers import GenerateOrderSerializer, OrderListSerializer


class GenerateOrderView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = GenerateOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    def get(self, request, order_id):
        order = Order.objects.filter(id=order_id, user=request.user).first()
        if not order:
            return Response({"error": "Orden no encontrada."}, status=404)

        return Response({
            "id": order.id,
            "products": products,
            "totalAmount": order.total_amount,
            "createdAt": order.created_at
        })
