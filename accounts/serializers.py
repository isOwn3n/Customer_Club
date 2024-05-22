from rest_framework import serializers
from . import models


class CustomerSerializer(serializers.ModelSerializer):
    """A serializes for customers"""

    class Meta:
        model = models.Customer
        fields = (
            "id",
            "firstname",
            "lastname",
            "phone_number",
            "member_of",
            "points",
            "birthday",
            "wedding_date",
        )
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        customer = models.Customer.objects.create_customer(**validated_data)
        return customer
