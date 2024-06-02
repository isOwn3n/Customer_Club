from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "permissions": (
                    list(user.get_all_permissions()) if not user.is_superuser else []
                ),
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
            }
        )
