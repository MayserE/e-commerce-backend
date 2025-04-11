from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from shared.session_context import get_current_user

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_current_user()
        if not user:
            return Response({"detail": "Usuario no autenticado"}, status=401)

        return Response({
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "last_name": user.last_name,
            "role": user.role,
            "status": user.status
        })