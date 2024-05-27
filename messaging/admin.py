from django.contrib import admin
from . import models


admin.site.register(models.Action)
admin.site.register(models.SendLog)


@admin.register(models.BuiltInMessage)
class BuiltInMessageAdmin(admin.ModelAdmin):
    exclude = ("deleted_at",)
