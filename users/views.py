from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from security.session_context import get_current_user
from users.serializers import RegisterClientSerializer, GetAuthenticatedUserSerializer


class RegisterClientView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterClientSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(RegisterClientSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAuthenticatedUserView(APIView):

    def get(self, request):
        user = get_current_user()
        if not user:
            return Response({"detail": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(GetAuthenticatedUserSerializer(user).data, status=status.HTTP_200_OK)
