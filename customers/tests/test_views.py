import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from mixer.backend.django import mixer
from customers.models import Customer, Group
from customers.serializers import CustomerSerializer, GroupSerializer
# from customers.views import CustomerViewSet, GroupViewSet


@pytest.mark.django_db
class TestCustomerViews:
    def test_customer_list(self):
        client = APIClient()
        url = reverse("customer-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_customer_create(self):
        client = APIClient()
        url = reverse("customer-list")
        data = {
            "firstname": "Is",
            "lastname": "Ownen",
            "phone_number": "09123456789",
            "points": 100,
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.count() == 1
        assert Customer.objects.get().firstname == "Is"


@pytest.mark.django_db
class TestGroupViews:
    def test_group_list(self):
        client = APIClient()
        url = reverse("group-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCustomerSerializer:
    def test_customer_serializer(self):
        customer = mixer.blend(Customer)
        serializer = CustomerSerializer(instance=customer)
        assert serializer.data


@pytest.mark.django_db
class TestGroupSerializer:
    def test_group_serializer(self):
        group = mixer.blend(Group)
        serializer = GroupSerializer(instance=group)
        assert serializer.data
