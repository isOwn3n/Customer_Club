from django.contrib.auth.models import User, Permission
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """A serializer for user."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
        ]
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "is_staff": {
                "read_only": True,
            },
            "is_superuser": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
            },
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    user_id = serializers.IntegerField(required=False)

class ChangePasswordByAdminSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    user_id = serializers.IntegerField(required=False)


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
