from django.contrib.auth.models import User, Permission
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }


class MeSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "permissions",
            "is_superuser",
            "is_staff",
        ]

    def get_permissions(self, obj):
        user_permissions = obj.user_permissions.all()
        group_permissions = Permission.objects.filter(group__user=obj)
        permissions = (user_permissions | group_permissions).distinct()
        return permissions.values_list("codename", flat=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_superuser:
            representation.pop("permissions")
        return representation
