from rest_framework import serializers
from . import models


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }
        exclude = ("deleted_at",)


class CustomerGetSerializer(serializers.ModelSerializer):
    """A serializes for get customers data"""

    member_of = serializers.SerializerMethodField()

    class Meta:
        model = models.Customer
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }
        exclude = ("deleted_at",)

    def get_member_of(self, obj):
        return obj.member_of.values_list("group_persian_name", flat=True)


class CustomerSerializer(serializers.ModelSerializer):
    """A serializes for get customers data"""

    member_of = serializers.PrimaryKeyRelatedField(
        queryset=models.Group.objects.filter(deleted_at__isnull=True).exclude(pk=1),
        many=True,
    )

    class Meta:
        model = models.Customer
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }
        exclude = ("deleted_at",)

    def create(self, validated_data):
        if validated_data["points"] == None:
            validated_data["points"] = 0
        customer = models.Customer.objects.create_customer(**validated_data)  # type: ignore
        return customer


class CustomerCountSerializer(serializers.Serializer):
    """A serializer for get customers count."""

    count = serializers.IntegerField()
