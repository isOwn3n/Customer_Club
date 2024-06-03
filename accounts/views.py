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


class ChangePasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")  # type: ignore
            new_password = serializer.validated_data.get("new_password")  # type: ignore

            if not user.check_password(old_password):
                return Response(
                    {"detail": "Old password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()
            return Response(
                {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordByAdminViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ChangePasswordByAdminSerializer
    permission_classes = [permissions.IsSuperUser]

    def create(self, request):
        serializer = serializers.ChangePasswordByAdminSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get("user_id")  # type: ignore
            if user_id == request.user.id:
                return Response(
                    {"detail": "You can change your password by this method!"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            try:
                user = User.objects.get(id=user_id)
                if user.is_superuser:
                    return Response(
                        {"detail": "You can`t change this user`s password!"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
                user.set_password(serializer.validated_data.get("new_password"))  # type: ignore
                user.save()
                return Response(
                    {"message": "Password changed successfully"},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {"detail": "User Not Found!"}, status=status.HTTP_404_NOT_FOUND
                )
