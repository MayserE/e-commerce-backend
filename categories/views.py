from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.serializers import CreateCategorySerializer
from security.permissions import IsAdminUser


class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = CreateCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(CreateCategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
