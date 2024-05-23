from django.contrib import admin
from . import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ("deleted_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(deleted_at__isnull=True, member_of__deleted_at__isnull=True)


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    exclude = ("deleted_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(deleted_at__isnull=True)
