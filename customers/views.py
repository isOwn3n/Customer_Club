from rest_framework import mixins, viewsets
from rest_framework.viewsets import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import serializers
from . import models


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.filter(deleted_at__isnull=True)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return serializers.CustomerSerializer
        return serializers.CustomerGetSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.save()
            instance.member_of.clear()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Customer.DoesNotExist:
            raise NotFound("Customer not found.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        try:
            existing_customer = models.Customer.objects.get(phone_number=phone_number)
            if existing_customer.deleted_at is not None:
                existing_customer.deleted_at = None
                existing_customer.firstname = serializer.validated_data.get("firstname")
                existing_customer.lastname = serializer.validated_data.get("lastname")
                existing_customer.birthday = serializer.validated_data.get("birthday")
                existing_customer.wedding_date = serializer.validated_data.get(
                    "wedding_date"
                )
                existing_customer.points = serializer.validated_data.get("points")
                existing_customer.save()
                existing_customer.member_of.add(1)
                existing_customer.member_of.add(
                    *serializer.validated_data.get("member_of")
                )
                serializer = serializers.CustomerGetSerializer(existing_customer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                {"message": "Customer already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except models.Customer.DoesNotExist:
            # Create a new customer if no existing customer is found
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomerRestoreViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Customer.objects.filter(deleted_at__isnull=False)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return serializers.CustomerSerializer
        return serializers.CustomerGetSerializer

    def create(self, request, *args, **kwargs): ...

    def destroy(self, request, *args, **kwargs):
        try:
            initial_group = models.Group.objects.get(pk=1)
            instance = self.get_object()
            instance.deleted_at = None
            instance.member_of.add(initial_group)
            instance.save()
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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Customer.DoesNotExist:
            raise NotFound("Customer not found.")


class CustomerCountViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Customer.objects.filter(deleted_at__isnull=True)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response(
            {"count": models.Customer.objects.count()}, status=status.HTTP_200_OK
        )
