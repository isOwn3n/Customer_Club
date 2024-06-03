from rest_framework import mixins, viewsets
from rest_framework.viewsets import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import serializers
from . import models
from customer_club import permissions


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.filter(deleted_at__isnull=True)
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return serializers.CustomerSerializer
        return serializers.CustomerGetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = models.Customer.objects.create_customer(**serializer.validated_data)  # type: ignore
        serializer = serializers.CustomerGetSerializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomerRestoreViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Customer.objects.filter(deleted_at__isnull=False)
    authentication_classes = (JWTAuthentication,)
    # permission_classes = (permissions.IsSuperUser,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return serializers.CustomerSerializer
        return serializers.CustomerGetSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.restore()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Customer.DoesNotExist:
            raise NotFound("Customer not found.")


class GroupRestoreViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.filter(deleted_at__isnull=True)
    authentication_classes = (JWTAuthentication,)
    # permission_classes = (permissions.IsSuperUser,)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = None
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Customer.DoesNotExist:
            raise NotFound("Customer not found.")


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.filter(deleted_at__isnull=True)
    authentication_classes = (JWTAuthentication,)
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ValidationError as e:
            return Response(
                {"detail": str(e.message)}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerCountViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """This is a view to get all customers count on root url
    and count of customers in each group with adding group id at the end of url"""

    queryset = models.Customer.objects.filter(deleted_at__isnull=True)
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.CustomerCountSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, pk=None, *args, **kwargs):
        group = models.Group.objects.get(pk=pk)
        customer_count = group.customer_set.count()  # type: ignore
        return Response({"count": customer_count}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return Response(
            {"count": models.Customer.objects.count()}, status=status.HTTP_200_OK
        )
