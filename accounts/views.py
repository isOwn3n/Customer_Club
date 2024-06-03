from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from .models import User

from django.contrib.auth.models import User
from . import serializers

from customer_club import permissions


class MeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = serializers.MeSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user
        if str(user) == "AnonymousUser":
            return Response(
                {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = serializers.MeSerializer(user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsSuperUser]
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all().order_by("id")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_staffuser(**serializer.validated_data)  # type: ignore
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
