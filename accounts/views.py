from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import serializers
from . import models


class CustomerViewSet(ModelViewSet):
    queryset = models.Customer.objects.filter(
        deleted_at__isnull=True,
        member_of__deleted_at__isnull=True,
    )
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return serializers.CustomerSerializer
        return serializers.CustomerGetSerializer

    def create_customer(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(f"DATA: {request.data}")
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=201)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Customer.DoesNotExist:
            raise NotFound("Customer not found.")


class GroupViewSet(ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.filter(deleted_at__isnull=True)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def delete_using_update():

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Customer.DoesNotExist:
            raise NotFound("Customer not found.")


# @api_view(["POST"])
# def create_customer(request):
#     serializer = serializers.CustomerSerializer("ali", "ezati", "all", 10)

#     return Response("OK", 200)
