from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from . import serializers


class MeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MeSerializer
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user
        if str(user) == "AnonymousUser":
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.MeSerializer(user)
        return Response(serializer.data)
